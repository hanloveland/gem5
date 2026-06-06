# -*- coding: utf-8 -*-
# Option D entry point - per-core SimPoint stall-alignment for SE mode.
#
# Standalone; does NOT modify run-se.py / system/se.py.
#
# Flow (single gem5 instance):
#   Phase A  atomic fast-forward of all cores; each core suspended (frozen)
#            when it reaches its per-core SimPoint target instruction count.
#   Phase B  once all cores are aligned -> switch atomic CPUs to O3 (TunedCPU)
#            via m5.switchCpus (drains, atomic->timing, cache port takeover).
#   Phase C  warmup window per core (re-warm O3 structures) -> m5.stats.reset()
#   Phase D  measured interval per core -> per-core IPC -> m5.stats.dump()
#
# Required (built) gem5 patch: BaseCPU.py must export suspendContext /
# activateContext (added to cxx_exports). Rebuild gem5 before running.
#
# Example:
#   gem5.opt --outdir=OUT skylake_config/run-se-simpoint.py \
#     --str_numcores 4 --ramu_config <yaml> --ramu_output OUT/ram.yaml --ramu_cap 128 \
#     --spec_path <spec> --poly_path <poly> --run_path OUT/run \
#     --mix_bench 429.mcf:470.lbm:syr2k:fdtd-2d \
#     --simpoint_targets 23950000000,7950000000,1950000000,3950000000 \
#     --warmup_insts 50000000 --interval_insts 1000000000

import sys
import os
from os import environ

# Resolve config paths. When launched via the driver (run_multi_sim.py) the
# env vars are set; when launched standalone they are not, so self-locate from
# __file__ (gem5 sets scope["__file__"] = script path; see m5/main.py).
_HERE = os.path.dirname(os.path.abspath(__file__))          # .../skylake_config
_GEM5_ROOT = os.path.dirname(_HERE)                          # .../gem5
environ.setdefault("GEM5_CPU_CONFIG_PATH", _HERE)
environ.setdefault("GEM5_COMMON_CONFIG_PATH", os.path.join(_GEM5_ROOT, "configs"))

GEM5_CPU_SYSTEM_PATH = environ.get("GEM5_CPU_CONFIG_PATH") + "/system"
sys.path.append(GEM5_CPU_SYSTEM_PATH)
sys.path.append(environ.get("GEM5_CPU_CONFIG_PATH"))         # for `from system...`
import m5
from m5.objects import *
import argparse
from system.se_simpoint import SimpointSystem
from system.core import *
from options import *

# ---- arguments -------------------------------------------------------------
parser = argparse.ArgumentParser()
addOptions(parser)
# Option D specific arguments
parser.add_argument("--simpoint_targets", type=str, default="",
                    help="Comma-separated per-core fast-forward target insts "
                         "(= interval_id*interval - warmup), one per core.")
parser.add_argument("--warmup_insts",   type=str, default="0",
                    help="Per-core warmup insts on O3 after switch (0 = no warmup; decided default).")
parser.add_argument("--interval_insts", type=str, default="1000000000",
                    help="Per-core measured interval length (instructions).")
args = parser.parse_args()

np = int(args.str_numcores)

FF_TARGET = [int(x) for x in args.simpoint_targets.split(",") if x.strip() != ""]
WARMUP    = int(args.warmup_insts)
INTERVAL  = int(args.interval_insts)

if len(FF_TARGET) != np:
    print("ERROR: --simpoint_targets needs %d values (one per core), got %d"
          % (np, len(FF_TARGET)))
    sys.exit(1)


# ---- system ----------------------------------------------------------------
class SimpointTestSystem(SimpointSystem):
    _DetailedCPUModel = TunedCPU
    _ramulator2_use = True
    if args.ramulator2_config_path == "":
        print("Not Exist Ramulator2 Configuration File!")
        exit(1)
    _ramulator2_config_path = args.ramulator2_config_path
    _ramulator2_output_path = args.ramulator2_output_path
    _num_process = np
    if args.ramu_cap != None:
        _ramulator2_memory_capacity = int(args.ramu_cap.strip())
    # Host DRAM capacity (gem5 address-range / backing size) is decoupled from
    # the Ramulator2 device-model capacity above. Default to ramu_cap when
    # --host_cap is not given (legacy behavior: host == ramulator).
    if args.host_cap != None:
        _host_memory_capacity = int(args.host_cap.strip())
    elif args.ramu_cap != None:
        _host_memory_capacity = int(args.ramu_cap.strip())
    if args.spec_path != "":
        _spec_cpu_path = args.spec_path
    if args.poly_path != "":
        _polybench_path = args.poly_path
    if args.run_path != "":
        _run_path = args.run_path


system = SimpointTestSystem()

# ---- workload dispatch (same options as run-se.py) -------------------------
if args.binary != "":
    print("Run Simple Binary File :", args.binary)
    system.setTestBinary(args.binary)
elif args.poly_bench != "":
    print("Run Polybenchmark :", args.poly_bench)
    system.setPolyBenchmark(args.poly_bench, np)
elif args.mibench != "":
    print("Run Mibench :", args.mibench)
    system.setMibench(args.mibench, np)
elif args.spec_bench != "":
    print("Run SPEC CPU 2006 Benchmark :", args.spec_bench)
    system.setSpecBenchmark(args.spec_bench_test, args.spec_bench, np)
elif args.mix_bench != "":
    print("Run Mix (SPEC CPU + Polybench) Benchmark :", args.mix_bench)
    system.setMixbench(args.mix_bench, np)
else:
    print("Not Supported Workload!!")
    exit(1)

# Bind the detailed (O3) CPUs to the same workload/isa now that the
# fast-forward CPUs' threads (and isa) exist.
system.finalizeSwitchCpus()

root = Root(full_system=False, system=system)
m5.instantiate()

num_cores = len(system.cpu)
print("=" * 60)
print("Option D: SimPoint stall-alignment")
print("  cores       : %d" % num_cores)
print("  FF targets  : %s" % FF_TARGET)
print("  warmup insts: %d" % WARMUP)
print("  interval    : %d" % INTERVAL)
print("=" * 60)


def core_ipc(cpu, start_tick, end_tick, n_insts):
    """Mirror run-se.py IPC computation. clk_domain.clock[0] -> period(ticks)."""
    clock_period = float(cpu.clk_domain.clock[0]) / 1e-12
    ticks = end_tick - start_tick
    cycles = ticks / clock_period if clock_period > 0 else 0
    ipc = n_insts / cycles if cycles > 0 else 0.0
    return ipc, cycles


# ===========================================================================
# Phase A: atomic fast-forward + per-core stall alignment
# ===========================================================================
for i, cpu in enumerate(system.cpu):
    tgt = max(1, FF_TARGET[i])
    cpu.scheduleInstStop(0, tgt, "ff_done_%d" % i)

paused = [False] * num_cores
while not all(paused):
    exit_event = m5.simulate()
    cause = exit_event.getCause()

    progressed = False
    for i, cpu in enumerate(system.cpu):
        if not paused[i] and cpu.totalInsts() >= max(1, FF_TARGET[i]):
            cpu.suspendContext(0)          # freeze this core; others keep FF
            paused[i] = True
            progressed = True
            print("[FF] core %d reached %d insts -> suspended"
                  % (i, cpu.totalInsts()))

    # A workload finished before reaching its target (target too large).
    if ("last active thread context" in cause) or ("exit" in cause.lower()):
        for i, cpu in enumerate(system.cpu):
            if not paused[i]:
                print("[FF][WARN] core %d ended before target (%d); pausing"
                      % (i, FF_TARGET[i]))
                try:
                    cpu.suspendContext(0)
                except Exception as e:
                    print("  suspend warn:", e)
                paused[i] = True
        break

    if not progressed:
        print("[FF][WARN] no core progressed; cause=%s -> stop FF" % cause)
        break

print("[ALIGN] all cores aligned at SimPoint targets")

# ===========================================================================
# Phase B: switch atomic -> O3 detailed
# ===========================================================================
# Reactivate the (suspended) atomic FF cores before the switch. m5.switchCpus
# internally drain()s; a SUSPENDED atomic CPU can make that drain spin/abort
# (empty event queue). An active atomic CPU sitting at an instruction boundary
# (its scheduleInstStop already fired) drains immediately and does NOT advance.
for i, cpu in enumerate(system.cpu):
    try:
        cpu.activateContext(0)
    except Exception as e:
        print("[SWITCH][warn] reactivate ff core %d: %s" % (i, e))
sys.stdout.flush()

system.switchToDetailed()
det = system.switch_cpus
for c in det:
    try:
        c.activateContext(0)               # O3 inherits Suspended -> activate
    except Exception as e:
        print("[SWITCH][warn] activateContext:", e)
print("[SWITCH] now running on detailed O3 CPUs (mem_mode=%s)"
      % str(system.mem_mode))

# ===========================================================================
# Phase C: warmup window (per core), then reset stats
# ===========================================================================
if WARMUP > 0:
    wbase = [c.totalInsts() for c in det]
    for i, c in enumerate(det):
        c.scheduleInstStop(0, WARMUP, "warm_done_%d" % i)
    warm = [False] * num_cores
    while not all(warm):
        m5.simulate()
        for i, c in enumerate(det):
            if not warm[i] and (c.totalInsts() - wbase[i]) >= WARMUP:
                warm[i] = True
    print("[WARMUP] all cores warmed (%d insts each)" % WARMUP)

m5.stats.reset()

# ===========================================================================
# Phase D: measured interval (per core), collect per-core IPC
# ===========================================================================
meas_start_tick = m5.curTick()
mbase = [c.totalInsts() for c in det]
done_tick = [0] * num_cores
meas_insts = [0] * num_cores            # insts each core ran in ITS window
measured = [False] * num_cores
for i, c in enumerate(det):
    c.scheduleInstStop(0, INTERVAL, "meas_done_%d" % i)

# Each core's IPC is measured over ITS OWN window [meas_start, its done_tick],
# during which it executes exactly INTERVAL insts. Faster cores finish early
# but KEEP running (not suspended) so contention persists for slower cores;
# we record their per-core insts/tick AT completion (not at the global end).
while not all(measured):
    exit_event = m5.simulate()
    cause = exit_event.getCause()
    for i, c in enumerate(det):
        if not measured[i] and (c.totalInsts() - mbase[i]) >= INTERVAL:
            measured[i] = True
            done_tick[i] = m5.curTick()
            meas_insts[i] = c.totalInsts() - mbase[i]    # ~INTERVAL
            print("[MEAS] core %d finished interval at tick %d (insts=%d)"
                  % (i, done_tick[i], meas_insts[i]))
    # Safety: if a workload exits before completing its interval, stop.
    if ("last active thread context" in cause) or ("exit" in cause.lower()):
        if not all(measured):
            print("[MEAS][WARN] a workload ended before interval complete:", cause)
            for i in range(num_cores):
                if not measured[i]:
                    done_tick[i] = m5.curTick()
                    meas_insts[i] = det[i].totalInsts() - mbase[i]
                    measured[i] = True
        break

m5.stats.dump()

print("-" * 60)
print("Option D results (per-core IPC over measured interval):")
ipcs = []
for i, c in enumerate(det):
    n_insts = meas_insts[i]
    ipc, cycles = core_ipc(c, meas_start_tick, done_tick[i], n_insts)
    ipcs.append(ipc)
    print("  core %d: IPC=%.4f  insts=%d  cycles=%.0f" % (i, ipc, n_insts, cycles))
print("IPC_CSV:" + ";".join("%.6f" % x for x in ipcs))
print("-" * 60)
