# -*- coding: utf-8 -*-
# Copyright (c) 2020 The Regents of the University of California
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met: redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer;
# redistributions in binary form must reproduce the above copyright
# notice, this list of conditions and the following disclaimer in the
# documentation and/or other materials provided with the distribution;
# neither the name of the copyright holders nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# Authors: Jason Lowe-Power, Trivikram Reddy

import sys 
from os import environ
GEM5_CPU_SYSTEM_PATH = environ.get("GEM5_CPU_CONFIG_PATH") + "/system"
sys.path.append(GEM5_CPU_SYSTEM_PATH)
# sys.path.append("/var/share/gem5_test/gem5/skylake_config/system/")
import m5
from m5.objects import *
import argparse
from system.se  import MySystem
from system.core import *
from options import *

# valid_configs = [VerbatimCPU, TunedCPU]
# valid_configs = {cls.__name__[:-3]:cls for cls in valid_configs}

parser = argparse.ArgumentParser()
addOptions(parser)
args = parser.parse_args()
np = int(args.str_numcores)

def get_core_ipc(cpu, start_tick, end_tick, clock_period):
    """
    IPC = Instructions / Cycles
    Cycles = (end_tick - start_tick) / clock_period
    """
    insts = cpu.totalInsts()
    ticks = end_tick - start_tick
    cycles = ticks / int(clock_period)
    
    if cycles > 0:
        ipc = insts / cycles
    else:
        ipc = 0.0
    
    return ipc, insts, cycles

def check_and_handle_completion(cause, start_tick, end_tick):
    """Check Each Core is Done or not, and record"""
    global done_cnt
    
    for i, cpu in enumerate(system.cpu):
        if core_done[i]:
            continue
            
        insts = cpu.totalInsts()
                
        print(f"[{iteration}] Core {i} Insts={insts:,}")
        if insts >= TARGET_INSTS:
            core_done[i] = True
            core_insts_at_done[i] = insts
            done_cnt += 1

            clock_period = float(cpu.clk_domain.clock[0]) / 1e-12
            ipc, insts, cycles = get_core_ipc(cpu, start_tick, end_tick, clock_period)
            core_ipc_at_done[i] = ipc
            core_cycles_at_done[i] = cycles
            print(f"Core {i}: IPC={ipc:.4f}, Insts={insts:,}, Cycles={cycles:,.0f}")

    if "exiting with last active thread context" in cause and done_cnt < num_cores:
        for i, cpu in enumerate(system.cpu):
            if not core_done[i]:
                try:
                    cpu.workload[0].rewind()
                except:
                    pass

# "../ext/ramulator2/ramulator2/ddr5_config.yaml"
# "output_ramulator2.yaml"
class TestSystem(MySystem):
    # We Fix CPU Simulation Model 
    _CPUModel = TunedCPU
    _ramulator2_use = True
    if args.ramulator2_config_path == "":
        print("Not Exist Ramulator2 Configuration File!")
        exit(1)
    _ramulator2_config_path = args.ramulator2_config_path
    _ramulator2_output_path = args.ramulator2_output_path
    _num_process = np
    if args.ramu_cap != None:
        _ramulator2_memory_capacity = int(args.ramu_cap.strip()) 

    if args.spec_path != "":
        _spec_cpu_path = args.spec_path

    if args.poly_path != "":
        _polybench_path = args.poly_path

    if args.run_path != "":
        _run_path = args.run_path

# Set the number of process 
system = TestSystem()
if args.binary != "":
    print("Run Simple Binary File :",args.binary)
    system.setTestBinary(args.binary)
elif args.poly_bench != "":
    print("Run Polybenchmark :",args.poly_bench)
    system.setPolyBenchmark(args.poly_bench,np)      
elif args.mibench != "":
    print("Run Mibench :",args.mibench)
    system.setMibench(args.mibench,np)              
elif args.spec_bench != "":
    print("Run SPEC CPU 2006 Benchmark")
    print(" - set SPEC CPU Benchmark Path")
    print(" - Input is Test? : ",args.spec_bench_test)
    system.setSpecBenchmark(args.spec_bench_test,args.spec_bench,np)
elif args.mix_bench != "":
    print(system._run_path)
    print("Run Mix (SPEC CPU + Polybench) Benchmark {}",args.mix_bench)
    system.setMixbench(args.mix_bench,np)
else:
    print("Not Supported Workload!!")
    exit(1)

if args.str_maxinsts != None:
    max_inst = int(args.str_maxinsts.strip())
    # for i in range(np):
    #     system.cpu[i].max_insts_any_thread = max_inst

TARGET_INSTS = max_inst
'''
Worst Assumption: IPC 5
CPU Frequency: 3.5GHz --> 1 Cycle --> 285 Ticks
Estimation Running Ticks E_TICK: (TARGET_INSTS / IPC) * 285 tick/cycle
--> QUANTUM_TICK = E_TICK/50
'''
# if max_inst == int(10e8):
#     QUANTUM_TICKS = int(10e6)  
# else:
#     QUANTUM_TICKS = int(max_inst/100)
QUANTUM_TICKS = int((float(max_inst) * 285 / 5) / 50)

num_cores = len(system.cpu)
core_done = [False] * num_cores
core_insts_at_done = [0] * num_cores   
core_ipc_at_done = [0] * num_cores     
core_cycles_at_done = [0] * num_cores  

root = Root(full_system = False, system = system)
m5.instantiate()

done_cnt = 0
iteration = 0

print(f"Starting simulation: {num_cores} cores, target {TARGET_INSTS:,} insts each")
print(f"Polling quantum: {QUANTUM_TICKS:,} ticks")
print("-" * 60)

start_tick = m5.curTick()

while done_cnt < num_cores:
    iteration += 1
    exit_event = m5.simulate(QUANTUM_TICKS)
    cause = exit_event.getCause()
    check_and_handle_completion(cause, start_tick, m5.curTick())

    if done_cnt == num_cores:
        m5.stats.dump()
        break    

print("-" * 60)
print("Simulation completed!")
print(f"Total iterations: {iteration}")
for i in range(num_cores):
    print(f"  core {i}: {core_insts_at_done[i]:,} instructions {core_cycles_at_done[i]:,.0f} cycles --> IPC {core_ipc_at_done[i]:.4f}")


if exit_event.getCause() != 'exiting with last active thread context':
    print("Benchmark failed with bad exit cause.")
    print(exit_event.getCause())
    exit(1)
if exit_event.getCode() != 0:
    print("Benchmark failed with bad exit code.")
    print("Exit code {}".format(exit_event.getCode()))
    exit(1)
