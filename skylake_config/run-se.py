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

system = TestSystem()
if args.binary != "":
    print("Run Simple Binary File :",args.binary)
    system.setTestBinary(args.binary)
else:
    print("Run SPEC CPU 2006 Benchmark")
    print(" - set SPEC CPU Benchmark Path")
    print(" - Input is Test? : ",args.spec_bench_test)
    system.setSpecBenmark(args.spec_path,args.spec_bench_test,args.spec_bench)

if args.str_maxinsts != None:
    max_inst = int(args.str_maxinsts.strip())
    system.cpu.max_insts_any_thread = max_inst

root = Root(full_system = False, system = system)
m5.instantiate()

exit_event = m5.simulate()

if exit_event.getCause() != 'exiting with last active thread context':
    print("Benchmark failed with bad exit cause.")
    print(exit_event.getCause())
    exit(1)
if exit_event.getCode() != 0:
    print("Benchmark failed with bad exit code.")
    print("Exit code {}".format(exit_event.getCode()))
    exit(1)
