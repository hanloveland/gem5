import argparse

benchmark_choices = [
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

def addOptions(parser):
    parser.add_argument(
        "--binary", 
        dest="binary", 
        action = "store", 
        type = str, 
        default ="", 
        help = "Path to binary to run")
    
    parser.add_argument(
        '--spec_path', 
        type = str, 
        help = "Path to spec cpu 2006")
    
    parser.add_argument(
        '--spec_bench', 
        dest="spec_bench", 
        type = str, 
        choices=benchmark_choices,
        help = "Input the becnhamrk progream to execute")    
    
    parser.add_argument(
        '--spec_bench_test', 
        action="store_true",
        default=False,
        help = "Test SPEC CPU Benchmark input is Test")        
    
    parser.add_argument(
        '--ramu_config', 
        type = str, 
        dest="ramulator2_config_path", 
        action = "store", 
        default ="",
        help = "Ramulator2 Configuration Yaml FIle Path")        
    
    parser.add_argument(
        '--ramu_output', 
        type = str, 
        dest="ramulator2_output_path", 
        default ="output_ramulator2.yaml",
        help = "Ramulator2 Simulation Result file Path")           
    
    parser.add_argument(
        "-I",
        "--maxinsts",
        action="store",
        type=int,
        default=None,
        help="""Total number of instructions to
                                            simulate (default: run forever)""",
    )   

    parser.add_argument(
        "--str_maxinsts",
        action="store",
        type=str,
        default=None,
        help="""Total number of instructions to
                                            simulate (default: run forever)""",
    )         