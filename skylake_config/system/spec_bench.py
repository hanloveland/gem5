# SPEC CPU Benchmark 
import m5
from m5.objects import *
from os import chdir

exe_suffix = "_base.none"

def set_spec_bench(_spec_path,_is_test,_bench,_pid):
    if _bench == "400.perlbench":
        exe_binary = "perlbench" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['-I.lib', 'attrs.pl']
        else:
            process.cmd = [exe_binary] + ['-I./lib', 'checkspam.pl', '2500', '5', '25', '11', '150', '1', '1', '1', '1']
            # process.cmd = [exe_binary] + ['-I./lib', 'diffmail.pl', '4', '800', '10', '17', '19', '300']
            # process.cmd = [exe_binary] + ['-I./lib', 'splitmail.pl', '1600', '12', '26', '16', '4500']
        process.output = _bench + '.out'
    elif _bench == "401.bzip2":
        exe_binary = "bzip2" + exe_suffix
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
        process.output = _bench + '.out'        
    elif _bench == "403.gcc":
        exe_binary = "gcc" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['cccp.i', '-o', 'cccp.s']
        else:
            process.cmd = [exe_binary] + ['166.i', '-o', '166.s']
            #process.cmd = [exe_binary] + ['200.i', '-o', '200.s']
            #process.cmd = [exe_binary] + ['c-typeck.i', '-o', 'c-typeck.s']
            #process.cmd = [exe_binary] + ['cp-decl.i', '-o', 'cp-decl.s']
            #process.cmd = [exe_binary] + ['expr.i', '-o', 'expr.s']
            #process.cmd = [exe_binary] + ['expr2.i', '-o', 'expr2.s']
            #process.cmd = [exe_binary] + ['g23.i', '-o', 'g23.s']
            #process.cmd = [exe_binary] + ['s04.i', '-o', 's04.s']
            #process.cmd = [exe_binary] + ['scilab.i', '-o', 'scilab.s']            
        process.output = _bench + '.out'          
    elif _bench == "410.bwaves":
        exe_binary = "bwaves" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary]
        else:
            process.cmd = [exe_binary]
        process.output = _bench + '.out'          
    elif _bench == "416.gamess":
        print("Error - Not Working")
        exe_binary = "gamess" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary       
        if _is_test == True:
            process.cmd = [exe_binary]
            process.input = 'exam29.config'
        else:
            process.cmd = [exe_binary]
            process.input = 'h2ocu2+.gradient.config'
            # process.input = 'triazolium.config'
        process.output = _bench + '.out'           
    elif _bench == "429.mcf":
        exe_binary = "mcf" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['inp.in']
        else:
            process.cmd = [exe_binary] + ['inp.in']
        process.output = _bench + '.out'              
    elif _bench == "433.milc":
        exe_binary = "milc" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] 
            process.input = 'su3imp.in'
        else:
            process.cmd = [exe_binary] 
            process.input = 'su3imp.in'
        process.output = _bench + '.out'  
    elif _bench == "434.zeusmp":
        exe_binary = "zeusmp" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] 
        else:
            process.cmd = [exe_binary] 
        process.output = _bench + '.out'           
    elif _bench == "435.gromacs":
        exe_binary = "gromacs" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['-silent','-deffnm', 'gromacs', '-nice','0']
        else:
            process.cmd = [exe_binary] + ['-silent','-deffnm', 'gromacs', '-nice','0']
        process.output = _bench + '.out'           
    elif _bench == "436.cactusADM":
        print("Error - Not Working")
        exit(1)
        exe_binary = "cactusADM" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['benchADM.par']
        else:
            process.cmd = [exe_binary] + ['benchADM.par']
        process.output = _bench + '.out'    
    elif _bench == "437.leslie3d":
        exe_binary = "leslie3d" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary]
            process.input = 'leslie3d.in'
        else:
            process.cmd = [exe_binary]
            process.input = 'leslie3d.in'
        process.output = _bench + '.out'    
    elif _bench == "444.namd":
        exe_binary = "namd" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['--input', 'namd.input', '--output', 'namd.out', '--iterations', '1']
        else:
            process.cmd = [exe_binary] + ['--input', 'namd.input', '--output', 'namd.out', '--iterations', '38']
        process.output = _bench + '.out'     
    elif _bench == "445.gobmk":
        exe_binary = "gobmk" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['--quiet','--mode', 'gtp']
            process.input = 'dniwog.tst'
        else:
            process.cmd = [exe_binary] + ['--quiet','--mode', 'gtp']
            process.input = '13x13.tst'
            # process.input = 'nngs.tst'
            # process.input = 'score2.tst'
            # process.input = 'trevorc.tst'
            # process.input = 'trevord.tst'            
        process.output = _bench + '.out'       
    elif _bench == "447.dealII":      
        exe_binary = "dealII" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['8']
        else:
            process.cmd = [exe_binary] + ['23']
        process.output = _bench + '.out'                                                   
    elif _bench == "450.soplex":     
        exe_binary = "soplex" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['-m10000', 'test.mps']
        else:
            process.cmd = [exe_binary] + ['-m45000', 'pds-50.mps']
            # process.cmd = [exe_binary] + ['-m3500', 'ref.mps']
        process.output = _bench + '.out'   
    elif _bench == "453.povray":          
        exe_binary = "povray" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['SPEC-benchmark-test.ini']
        else:
            process.cmd = [exe_binary] + ['SPEC-benchmark-ref.ini']
        process.output = _bench + '.out'       
    elif _bench == "454.calculix":            
        exe_binary = "calculix" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['-i', 'beampic']
        else:
            process.cmd = [exe_binary] + ['-i', 'hyperviscoplastic']
        process.output = _bench + '.out'    
    elif _bench == "456.hmmer":
        exe_binary = "hmmer" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['--fixed', '0', '--mean', '325', '--num', '45000', '--sd', '200', '--seed', '0', 'bombesin.hmm']
        else:
            process.cmd = [exe_binary] + ['nph3.hmm', 'swiss41']
            # process.cmd = [exe_binary] + ['--fixed', '0', '--mean', '500', '--num', '500000', '--sd', '350', '--seed', '0', 'retro.hmm']
        process.output = _bench + '.out' 
    elif _bench == "458.sjeng":
        exe_binary = "sjeng" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['test.txt']
        else:
            process.cmd = [exe_binary] + ['ref.txt']
            # process.cmd = [exe_binary] + ['--fixed', '0', '--mean', '500', '--num', '500000', '--sd', '350', '--seed', '0', 'retro.hmm']
        process.output = _bench + '.out' 
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
        process.output = _bench + '.out'           
    elif _bench == "462.libquantum":
        exe_binary = "libquantum" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['33','5']
        else:
            process.cmd = [exe_binary] + ['1397','8']
        process.output = _bench + '.out'   
    elif _bench == "464.h264ref":
        exe_binary = "h264ref" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['-d', 'foreman_test_encoder_baseline.cfg']
        else:
            process.cmd = [exe_binary] + ['-d', 'foreman_ref_encoder_baseline.cfg']
            # process.cmd = [exe_binary] + ['-d', 'foreman_ref_encoder_main.cfg']
            # process.cmd = [exe_binary] + ['-d', 'sss_encoder_main.cfg']
        process.output = _bench + '.out'      
    elif _bench == "465.tonto":       
        exe_binary = "tonto" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary]
        else:
            process.cmd = [exe_binary]
    elif _bench == "470.lbm":           
        exe_binary = "lbm" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['20', 'reference.dat', '0', '1', '100_100_130_cf_a.of']
        else:
            process.cmd = [exe_binary] + ['300', 'reference.dat', '0', '0', '100_100_130_ldc.of']           
        process.output = _bench + '.out'     
    elif _bench == "471.omnetpp":
        exe_binary = "omnetpp" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['omnetpp.ini']
        else:
            process.cmd = [exe_binary] + ['omnetpp.ini']
        process.output = _bench + '.out'          
    elif _bench == "473.astar":
        exe_binary = "astar" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['lake.cfg']
        else:
            process.cmd = [exe_binary] + ['rivers.cfg']
        process.output = _bench + '.out'             
    elif _bench == "481.wrf":             
        exe_binary = "wrf" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary]
        else:
            process.cmd = [exe_binary]
        process.output = _bench + '.out'       
    elif _bench == "482.sphinx3": 
        exe_binary = "sphinx_livepretend" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['ctlfile', '.', 'args.an4']
        else:
            process.cmd = [exe_binary] + ['ctlfile', '.', 'args.an4']
        process.output = _bench + '.out'    
    elif _bench == "483.xalancbmk":
        exe_binary = "Xalan" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['-v','test.xml','xalanc.xsl']
        else:
            process.cmd = [exe_binary] + ['-v','t5.xml','xalanc.xsl']
        process.output = _bench + '.out'                                                                                      
    elif _bench == "998.specrand":
        exe_binary = "specrand" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['324342', '24239']
        else:
            process.cmd = [exe_binary] + ['1255432124', '234923']
        process.output = _bench + '.out'  
    elif _bench == "999.specrand":
        exe_binary = "specrand" + exe_suffix
        process = Process(pid=_pid)
        process.executable = exe_binary
        if _is_test == True:
            process.cmd = [exe_binary] + ['324342', '24239']
        else:
            process.cmd = [exe_binary] + ['1255432124', '234923']
        process.output = _bench + '.out'         
    else: 
        print("Wrong SPEC CPU Benchmark!")
        exit(1)

    return process