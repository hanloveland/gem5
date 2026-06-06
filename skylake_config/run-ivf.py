# -*- coding: utf-8 -*-
# Run a single static SE binary (e.g. the FAISS IVF-Flat kernel) to completion
# in the skylake_config + Ramulator2 framework. Single core, NO fast-forward,
# NO CPU switch -- just instantiate and m5.simulate() until the program exits.
#
# Functional-first: defaults to AtomicSimpleCPU (fast, for bring-up); switch to
# --cpu_model timing / o3 for detailed timing once functionally verified.
# Data loading is INCLUDED in the run (no m5ops ROI yet -- see faiss_ivf README
# section 7); use --nq 1 for a quick first run.
#
# Example:
#   gem5.opt --outdir=OUT run-ivf.py \
#       --binary /abs/faiss_ivf/ivf_flat_gem5 \
#       --bin_options "/abs/faiss_ivf/gem5_ivf --nq 1 --nprobe 32 --k 10" \
#       --cpu_model atomic \
#       --ramu_config <yaml> --ramu_output OUT/ram.yaml --ramu_cap 128 \
#       --run_path OUT/run
import sys
import os
from os import environ

# Resolve config paths. When launched via a driver the env vars are set; when
# launched standalone (e.g. run_ivf_gem5.sh) they are not, so self-locate from
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
from system.se import MySystem
from system.core import *
from options import *

parser = argparse.ArgumentParser()
addOptions(parser)
parser.add_argument("--bin_options", type=str, default="",
                    help="Whitespace-separated argv passed to --binary "
                         "(e.g. '/abs/gem5_ivf --nq 1 --nprobe 32 --k 10').")
parser.add_argument("--cpu_model", type=str, default="atomic",
                    choices=["atomic", "timing", "o3"],
                    help="atomic=AtomicSimpleCPU (fast functional, default), "
                         "timing=TimingSimpleCPU, o3=TunedCPU (detailed).")
args = parser.parse_args()

CPU_MAP  = {"atomic": AtomicSimpleCPU, "timing": TimingSimpleCPU, "o3": TunedCPU}
MEM_MODE = {"atomic": "atomic",        "timing": "timing",        "o3": "timing"}

if args.binary == "":
    print("ERROR: --binary is required for run-ivf.py")
    sys.exit(1)


class IvfSystem(MySystem):
    # Single static binary, single core, run to completion.
    _CPUModel = CPU_MAP[args.cpu_model]
    _ramulator2_use = True
    if args.ramulator2_config_path == "":
        print("Not Exist Ramulator2 Configuration File!")
        exit(1)
    _ramulator2_config_path = args.ramulator2_config_path
    _ramulator2_output_path = args.ramulator2_output_path
    _num_process = 1
    if args.ramu_cap != None:
        _ramulator2_memory_capacity = int(args.ramu_cap.strip())
    if args.run_path != "":
        _run_path = args.run_path


system = IvfSystem()
# MySystem.__init__ hardcodes mem_mode='timing'; an AtomicSimpleCPU needs
# 'atomic'. Set it to match the chosen CPU model.
system.mem_mode = MEM_MODE[args.cpu_model]

opts = args.bin_options.split() if args.bin_options.strip() else []
print("Run IVF binary :", args.binary)
print("  options      :", opts)
print("  cpu_model    :", args.cpu_model, "(mem_mode=%s)" % system.mem_mode)
system.setTestBinary(args.binary, opts)

# Optional instruction cap (else run the program to its natural exit).
maxinsts = 0
if args.str_maxinsts not in (None, ""):
    maxinsts = int(args.str_maxinsts.strip())
if maxinsts > 0:
    system.cpu[0].max_insts_any_thread = maxinsts
    print("  max_insts    :", maxinsts)

root = Root(full_system=False, system=system)
m5.instantiate()

print("-" * 60)
print("[IVF] starting simulation (no FF, run-to-completion)...")
sys.stdout.flush()

start_tick = m5.curTick()
exit_event = m5.simulate()
end_tick = m5.curTick()
cause = exit_event.getCause()
m5.stats.dump()

cpu = system.cpu[0]
insts = cpu.totalInsts()
clock_period = float(cpu.clk_domain.clock[0]) / 1e-12   # ticks per cycle
ticks = end_tick - start_tick
cycles = ticks / int(clock_period) if clock_period > 0 else 0
ipc = insts / cycles if cycles > 0 else 0.0

print("-" * 60)
print("[IVF] done. cause: %s (code=%s)" % (cause, exit_event.getCode()))
print("  insts  = %d" % insts)
print("  cycles = %.0f" % cycles)
print("  ticks  = %d" % ticks)
print("  IPC    = %.4f" % ipc)
print("IVF_CSV:%s,%d,%.0f,%.6f" % (args.cpu_model, insts, cycles, ipc))

# A clean program exit reports "exiting with last active thread context".
if maxinsts == 0 and "last active thread context" not in cause:
    print("[IVF][WARN] unexpected exit cause:", cause)
