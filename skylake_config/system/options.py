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

polybench_choice = [
    "covariance", "2mm", "3mm", "atax", "bicg", "doitgen", "mvt", "gemm",
    "gemver", "gesummv", "symm", "syr2k", "syrk", "trmm", "durbin", "lu",
    "ludcmp", "trisolv", "deriche",  "floyd-warshall", "nussinov", "adi",
    "fdtd-2d", "heat-3d", "jacobi-1d", "jacobi-2d", "seidel-2d", "cholesky",
    "gramschmidt", "correlation"
]

mibench_choice = [
    "basicmath", "bitcount", "qsort", "susan", "blowfish", "rijndael", "sha",
    "dijkstra", "patricia", "adpcm", "CRC32", "FFT", "gsm"
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
        '--run_path', 
        type = str, 
        default="",
        help = "Path to run Workload")

    parser.add_argument(
        '--spec_path', 
        type = str, 
        default="",
        help = "Path to spec cpu 2006")
    
    parser.add_argument(
        '--spec_bench', 
        dest="spec_bench", 
        type = str, 
        choices=benchmark_choices,
        default="",
        help = "Input the benchmark program (SPEC CPU 2006) to execute")    
    
    parser.add_argument(
        '--spec_bench_test', 
        action="store_true",
        default=False,
        help = "Test SPEC CPU Benchmark input is Test")        
    
    parser.add_argument(
        '--poly_path', 
        type = str, 
        default="",
        help = "Path to polybench")

    parser.add_argument(
        '--poly_bench', 
        dest="poly_bench", 
        type = str, 
        choices=polybench_choice,
        default="",
        help = "Input the benchmark program (polybench) to execute") 

    parser.add_argument(
        '--mibench', 
        dest="mibench", 
        type = str, 
        choices=mibench_choice,
        default="",
        help = "Input the benchmark program (mibench) to execute") 

    parser.add_argument(
        '--mix_bench', 
        dest="mix_bench", 
        type = str, 
        default="",
        help = "Input the benchmark program (mixed workload) to execute") 

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
        '--ramu_cap', 
        action="store",
        type=str,
        default=None,
        help="""Ramulator2 Memory Capacity (string). unit is GB)""",
    )       
        
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
    
    parser.add_argument(
        "--str_numcores",
        action="store",
        type=str,
        default=1,
        help="""Total number of instructions to
                                            simulate (default: run forever)""",
    )             