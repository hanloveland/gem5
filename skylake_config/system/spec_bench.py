# SPEC CPU Benchmark 
import m5
from m5.objects import *
from os import chdir
import shutil
from pathlib import Path

exe_suffix = "_base.none"

benchmark_list = [
    "400.perlbench",
    "401.bzip2",
    "403.gcc",
    "410.bwaves",
    "416.gamess",
    "429.mcf",
    "433.milc",
    "434.zeusmp",
    "435.gromacs",
    "436.cactusADM",
    "437.leslie3d",
    "444.namd",
    "445.gobmk",
    "450.soplex",
    "453.povray",
    "454.calculix",
    "456.hmmer",
    "458.sjeng",
    "459.GemsFDTD",
    "462.libquantum",
    "464.h264ref",
    "465.tonto",
    "470.lbm",
    "471.omnetpp",
    "473.astar",
    "481.wrf",
    "482.sphinx3",
    "483.xalancbmk",
    "998.specrand",
    "999.specrand",
]

poly_datamining_list = [ "correlation", "covariance" ]
poly_kernel_list = [ "2mm", "3mm", "atax", "bicg", "doitgen", "mvt"]
poly_blas_list = [ "gemm", "gemver", "gesummv", "symm", "syr2k", "syrk", "trmm"]
poly_solver_list = [ "durbin", "lu", "ludcmp", "trisolv", "cholesky", "gramschmidt" ]
poly_medley_list = [ "deriche", "floyd-warshall", "nussinov" ]
poly_stencil_list = [ "adi", "fdtd-2d", "heat-3d", "jacobi-1d", "jacobi-2d", "seidel-2d" ]

mibench_automotive_list = ["basicmath", "bitcount", "qsort", "susan"] 
mibench_security_list = ["blowfish", "rijndael", "sha"]
mibench_network_list = ["dijkstra","patricia"]
mibench_telecomm_list = ["CRC32","FFT","gsm"] 

def set_spec_bench(_spec_path,_is_test,_bench,_pid,_run_path=""):
    shutil.copytree(_spec_path, _run_path, dirs_exist_ok=True)
    if _bench == "400.perlbench":
        exe_binary = _run_path + "/" + "perlbench" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['-I.lib', 'attrs.pl']
        else:
            # process.cmd = [exe_binary] + ['-I./lib', 'checkspam.pl', '2500', '5', '25', '11', '150', '1', '1', '1', '1']
            # process.cmd = [exe_binary] + ['-I./lib', 'diffmail.pl', '4', '800', '10', '17', '19', '300']
            process.cmd = [exe_binary] + ['-I./lib', 'splitmail.pl', '1600', '12', '26', '16', '4500']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"
    elif _bench == "401.bzip2":
        exe_binary = _run_path + "/" + "bzip2" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['input.program', '5']
        else:
            process.cmd = [exe_binary] + ['input.source', '280']
            # process.cmd = [exe_binary] + ['chicken.jpg', '30']
            # process.cmd = [exe_binary] + ['liberty.jpg', '30']
            # process.cmd = [exe_binary] + ['input.program', '280']
            # process.cmd = [exe_binary] + ['input.program', '280']
            # process.cmd = [exe_binary] + ['text.html', '280']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"     
    elif _bench == "403.gcc":
        exe_binary = _run_path + "/" + "gcc" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['cccp.in', '-o', 'cccp.s']
        else:
            process.cmd = [exe_binary] + ['166.in', '-o', '166.s']
            #process.cmd = [exe_binary] + ['200.in', '-o', '200.s']
            #process.cmd = [exe_binary] + ['c-typeck.in', '-o', 'c-typeck.s']
            #process.cmd = [exe_binary] + ['cp-decl.in', '-o', 'cp-decl.s']
            #process.cmd = [exe_binary] + ['expr.in', '-o', 'expr.s']
            #process.cmd = [exe_binary] + ['expr2.in', '-o', 'expr2.s']
            #process.cmd = [exe_binary] + ['g23.in', '-o', 'g23.s']
            #process.cmd = [exe_binary] + ['s04.in', '-o', 's04.s']
            #process.cmd = [exe_binary] + ['scilab.in', '-o', 'scilab.s']     
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"                    
    elif _bench == "410.bwaves":
        exe_binary = _run_path + "/" + "bwaves" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary]
        else:
            process.cmd = [exe_binary]
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"     
    elif _bench == "416.gamess":
        print("Error - Not Working")
        exe_binary = _run_path + "/" + "gamess" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary       
        if _is_test == True:
            process.cmd = [exe_binary]
            process.input = f"{_run_path}/exam29.config"
        else:
            process.cmd = [exe_binary]
            process.input = f"{_run_path}/h2ocu2+.gradient.config"
            # process.input = 'triazolium.config'
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"          
    elif _bench == "429.mcf":
        exe_binary = _run_path + "/" + "mcf" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['inp.in']
        else:
            process.cmd = [exe_binary] + ['inp.in']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"                
    elif _bench == "433.milc":
        exe_binary = _run_path + "/" + "milc" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] 
            process.input = f"{_run_path}/su3imp.in"
        else:
            process.cmd = [exe_binary] 
            process.input = f"{_run_path}/su3imp.in"
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"            
    elif _bench == "434.zeusmp":
        exe_binary = _run_path + "/" + "zeusmp" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] 
        else:
            process.cmd = [exe_binary] 
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"      
    elif _bench == "435.gromacs":
        exe_binary = _run_path + "/" + "gromacs" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['-silent','-deffnm', 'gromacs', '-nice','0']
        else:
            process.cmd = [exe_binary] + ['-silent','-deffnm', 'gromacs', '-nice','0']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"             
    elif _bench == "436.cactusADM":
        print("Error - Not Working")
        exit(1)
        exe_binary = _run_path + "/" + "cactusADM" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['benchADM.par']
        else:
            process.cmd = [exe_binary] + ['benchADM.par']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"  
    elif _bench == "437.leslie3d":
        exe_binary = _run_path + "/" + "leslie3d" + exe_suffix
        # exe_binary = "leslie3d" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary]
            process.input = f"{_run_path}/leslie3d.in"
        else:
            process.cmd = [exe_binary]
            process.input = f"{_run_path}/leslie3d.in"
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt" 
        # process.output = f"stdout.txt"
        # process.errout = f"stderr.txt"         
    elif _bench == "444.namd":
        exe_binary = _run_path + "/" + "namd" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['--input', 'namd.input', '--output', 'namd.out', '--iterations', '1']
        else:
            process.cmd = [exe_binary] + ['--input', 'namd.input', '--output', 'namd.out', '--iterations', '38']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"        
    elif _bench == "445.gobmk":
        exe_binary = _run_path + "/" + "gobmk" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['--quiet','--mode', 'gtp']
            process.input = f"{_run_path}/dniwog.tst"
        else:
            process.cmd = [exe_binary] + ['--quiet','--mode', 'gtp']
            process.input = f"{_run_path}/13x13.tst"
            # process.input = 'nngs.tst'
            # process.input = 'score2.tst'
            # process.input = 'trevorc.tst'
            # process.input = 'trevord.tst'            
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"             
    elif _bench == "447.dealII":      
        exe_binary = _run_path + "/" + "dealII" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['8']
        else:
            process.cmd = [exe_binary] + ['23']               
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"                                  
    elif _bench == "450.soplex":     
        exe_binary = _run_path + "/" + "soplex" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['-m10000', 'test.mps']
        else:
            process.cmd = [exe_binary] + ['-m45000', 'pds-50.mps']
            # process.cmd = [exe_binary] + ['-m3500', 'ref.mps']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"
    elif _bench == "453.povray":          
        exe_binary = _run_path + "/" + "povray" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['SPEC-benchmark-test.ini']
        else:
            process.cmd = [exe_binary] + ['SPEC-benchmark-ref.ini']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt" 
    elif _bench == "454.calculix":            
        exe_binary = _run_path + "/" + "calculix" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['-i', 'beampic']
        else:
            process.cmd = [exe_binary] + ['-i', 'hyperviscoplastic']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"
    elif _bench == "456.hmmer":
        exe_binary = _run_path + "/" + "hmmer" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['--fixed', '0', '--mean', '325', '--num', '45000', '--sd', '200', '--seed', '0', 'bombesin.hmm']
        else:
            process.cmd = [exe_binary] + ['nph3.hmm', 'swiss41']
            # process.cmd = [exe_binary] + ['--fixed', '0', '--mean', '500', '--num', '500000', '--sd', '350', '--seed', '0', 'retro.hmm']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"
    elif _bench == "458.sjeng":
        exe_binary = _run_path + "/" + "sjeng" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['test.txt']
        else:
            process.cmd = [exe_binary] + ['ref.txt']
            # process.cmd = [exe_binary] + ['--fixed', '0', '--mean', '500', '--num', '500000', '--sd', '350', '--seed', '0', 'retro.hmm']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"
    elif _bench == "459.GemsFDTD":
        print("Need check whether it is workingor not")
        exit(1)              
        exe_binary = "GemsFDTD" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary]
        else:
            process.cmd = [exe_binary]
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"      
    elif _bench == "462.libquantum":
        exe_binary = _run_path + "/" + "libquantum" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['33','5']
        else:
            process.cmd = [exe_binary] + ['1397','8']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"
    elif _bench == "464.h264ref":
        exe_binary = _run_path + "/" + "h264ref" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['-d', 'foreman_test_encoder_baseline.cfg']
        else:
            # process.cmd = [exe_binary] + ['-d', 'foreman_ref_encoder_baseline.cfg']
            process.cmd = [exe_binary] + ['-d', 'foreman_ref_encoder_main.cfg']
            # process.cmd = [exe_binary] + ['-d', 'sss_encoder_main.cfg']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"      
    elif _bench == "465.tonto":       
        exe_binary = _run_path + "/" + "tonto" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary]
        else:
            process.cmd = [exe_binary]
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"            
    elif _bench == "470.lbm":           
        exe_binary = _run_path + "/" + "lbm" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['20', 'reference.dat', '0', '1', '100_100_130_cf_a.of']
        else:
            process.cmd = [exe_binary] + ['300', 'reference.dat', '0', '0', '100_100_130_ldc.of']           
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"        
    elif _bench == "471.omnetpp":
        exe_binary = _run_path + "/" + "omnetpp" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['omnetpp.ini']
        else:
            process.cmd = [exe_binary] + ['omnetpp.ini']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"         
    elif _bench == "473.astar":
        exe_binary = _run_path + "/" + "astar" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['lake.cfg']
        else:
            process.cmd = [exe_binary] + ['rivers.cfg']   
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"        
    elif _bench == "481.wrf":             
        exe_binary = _run_path + "/" + "wrf" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary]
        else:
            process.cmd = [exe_binary]
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"
    elif _bench == "482.sphinx3": 
        exe_binary = _run_path + "/" + "sphinx_livepretend" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['ctlfile', '.', 'args.an4']
        else:
            process.cmd = [exe_binary] + ['ctlfile', '.', 'args.an4']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt" 
    elif _bench == "483.xalancbmk":
        exe_binary = _run_path + "/" + "Xalan" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['-v','test.xml','xalanc.xsl']
        else:
            process.cmd = [exe_binary] + ['-v','t5.xml','xalanc.xsl']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"                                                                                            
    elif _bench == "998.specrand":
        exe_binary = _run_path + "/" + "specrand" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['324342', '24239']
        else:
            process.cmd = [exe_binary] + ['1255432124', '234923']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"
    elif _bench == "999.specrand":
        exe_binary = _run_path + "/" + "specrand" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['324342', '24239']
        else:
            process.cmd = [exe_binary] + ['1255432124', '234923']
        process.cwd = _run_path
        process.output = f"{_run_path}/stdout.txt"
        process.errout = f"{_run_path}/stderr.txt"
    else: 
        print("Wrong SPEC CPU Benchmark!")
        exit(1)

    return process


def set_mibench(_bench,_pid):
    if _bench == "basicmath":
        exe_binary = "basicmath_large"
        process = Process(pid=_pid)
        process.executable = exe_binary
        process.cmd = [exe_binary]
        process.output = _bench + '.out'
    elif _bench == "bitcount":
        exe_binary = "bitcnts"
        process = Process(pid=_pid)
        process.executable = exe_binary
        process.cmd = [exe_binary] + ['1125000']
        process.output = _bench + '.out'  
    elif _bench == "qsort":
        exe_binary = "qsort_large"
        process = Process(pid=_pid)
        process.executable = exe_binary
        process.cmd = [exe_binary] + ['input_large.dat']
        process.output = _bench + '.out'        
    elif _bench == "susan":
        exe_binary = "susan"
        process = Process(pid=_pid)
        process.executable = exe_binary
        process.cmd = [exe_binary] + ['input_large.pgm', 'output_large.smoothing.pgm','-s']
        process.output = _bench + '.out'        
    elif _bench == "blowfish":
        exe_binary = "bf"
        process = Process(pid=_pid)
        process.executable = exe_binary
        process.cmd = [exe_binary] + ['e','input_large.asc','output_large.enc','1234567890abcdeffedcba0987654321']
        process.output = _bench + '.out'      
    elif _bench == "rijndael":
        exe_binary = "rijndael"
        process = Process(pid=_pid)
        process.executable = exe_binary
        process.cmd = [exe_binary] + ['input_large.asc', 'output_large.enc', 'e', '1234567890abcdeffedcba09876543211234567890abcdeffedcba0987654321']
        process.output = _bench + '.out'         
    elif _bench == "sha":
        exe_binary = "sha"
        process = Process(pid=_pid)
        process.executable = exe_binary
        process.cmd = [exe_binary] + ['input_large.asc']
        process.output = _bench + '.out'        
    elif _bench == "dijkstra":
        exe_binary = "dijkstra_large"
        process = Process(pid=_pid)
        process.executable = exe_binary
        process.cmd = [exe_binary] + ['input.dat']
        process.output = _bench + '.out'           
    elif _bench == "patricia":
        exe_binary = "patricia"
        process = Process(pid=_pid)
        process.executable = exe_binary
        process.cmd = [exe_binary] + ['large.udp']
        process.output = _bench + '.out'              
    elif _bench == "adpcm":
        exe_binary = "rawcaudio"
        process = Process(pid=_pid)
        process.executable = exe_binary
        process.cmd = [exe_binary] + ['<','large.pcm']
        process.output = _bench + '.out'          
    elif _bench == "CRC32":
        exe_binary = "crc"
        process = Process(pid=_pid)
        process.executable = exe_binary
        process.cmd = [exe_binary] + ['../adpcm/data/large.pcm']
        process.output = _bench + '.out' 
    elif _bench == "FFT":
        exe_binary = "fft"
        process = Process(pid=_pid)
        process.executable = exe_binary
        process.cmd = [exe_binary] + ['8', '32768']
        process.output = _bench + '.out'   
    elif _bench == "gsm":
        exe_binary = "bin/toast"
        process = Process(pid=_pid)
        process.executable = exe_binary
        process.cmd = [exe_binary] + ['-fps', '-c', 'data/large.au']
        process.output = _bench + '.out'            
    else: 
        print("Wrong Mibench")
        exit(1)

    return process

def set_polybench(_poly_path,_bench,_pid,_run_path=""):
    shutil.copytree(_poly_path, _run_path, dirs_exist_ok=True)
    exe_binary = _run_path + "/" + _bench
    process = Process(pid=_pid)
    process.executable = exe_binary
    process.cmd = [exe_binary]
    process.cwd = _run_path
    process.output = f"{_run_path}/stdout.txt"
    process.errout = f"{_run_path}/stderr.txt"

    return process

def get_spec_bench_path(_spec_path,_bench,_is_test):
    if _bench in benchmark_list:
        if _is_test:
            run_path = _spec_path + "/" + _bench + "/run/run_base_test_none.0000/"            
        else: 
            run_path = _spec_path + "/" + _bench + "/run/run_base_ref_none.0000/"            
        return run_path    
    else: 
        print("Wrong SPEC CPU Benchmark!")
        exit(1)

def get_poly_bench_path(_poly_path,_bench):
    if _bench in poly_datamining_list:
        run_path = _poly_path + "/" + "datamining/" + _bench
    elif _bench in poly_kernel_list:
        run_path = _poly_path + "/" + "linear-algebra/kernels/" + _bench
    elif _bench in poly_blas_list:
        run_path = _poly_path + "/" + "linear-algebra/blas/" + _bench       
    elif _bench in poly_solver_list:
        run_path = _poly_path + "/" + "linear-algebra/solvers/" + _bench             
    elif _bench in poly_medley_list:
        run_path = _poly_path + "/" + "medley/" + _bench      
    elif _bench in poly_stencil_list:
        run_path = _poly_path + "/" + "stencils/" + _bench           
    else: 
        print("Wrong PolyBench!!")
        exit(1)
    return run_path
    
def get_mibench_path(_mibench_path,_bench):
    if _bench in mibench_automotive_list:
        run_path = _mibench_path + "/" + "automotive/" + _bench    
    elif _bench in mibench_security_list:
        run_path = _mibench_path + "/" + "security/" + _bench  
    elif _bench in mibench_network_list:
        run_path = _mibench_path + "/" + "network/" + _bench  
    elif _bench in mibench_telecomm_list:
        run_path = _mibench_path + "/" + "telecomm/" + _bench       
    elif _bench == "adpcm":
        run_path = _mibench_path + "/" + "telecomm/" + _bench + "/bin"
    else: 
        print(f"{_bench} is not Mibench!!")
        exit(1)
    return run_path    