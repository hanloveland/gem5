# -*- coding: utf-8 -*-
# Standalone SE system for Option D - per-core SimPoint stall-alignment.
#
# Independent from se.py (original is preserved). This system is built for the
# fast-forward + CPU-switch flow:
#   - starts in 'atomic_noncaching' memory mode
#   - self.cpu        : NonCachingSimpleCPU per core (fast-forward, active).
#       Caches are wired to these CPUs but BYPASSED at runtime while the system
#       is in atomic_noncaching mode (BaseCache::CpuSidePort forwards straight
#       to mem_side), giving cacheless-speed FF. Caches are therefore NOT warmed
#       during FF (cold start after the switch).
#   - self.switch_cpus: TunedCPU (O3) per core   (detailed, switched_out, no caches)
#   - switchToDetailed(): m5.switchCpus(atomic_noncaching -> O3); switchCpus
#       internally drains, changes memory mode to 'timing', and rebinds cache
#       ports (takeOverFrom) so the (now active) caches carry over to the O3 CPUs.
#
# Mirrors the proven upstream fast-forward pattern in
# configs/common/Simulation.py:511-547 (switch_cpus share workload/isa/clk,
# createThreads, no private caches).
from os import environ
import m5
from m5.objects import *
from core import *
from caches import *
import sys

GEM5_CONF_PATH = environ.get("GEM5_COMMON_CONFIG_PATH")
sys.path.append(GEM5_CONF_PATH)
from common import ObjectList
from spec_bench import *

spec_benchmark_list = [
  "400.perlbench","401.bzip2","403.gcc","410.bwaves","416.gamess","429.mcf","433.milc",
  "434.zeusmp","435.gromacs","436.cactusADM","437.leslie3d","444.namd","445.gobmk",
  "450.soplex","453.povray","454.calculix","456.hmmer","458.sjeng","459.GemsFDTD","462.libquantum",
  "464.h264ref","465.tonto","470.lbm","471.omnetpp","473.astar","481.wrf","482.sphinx3","483.xalancbmk",
  "998.specrand","999.specrand"
]

polybench_list = [
  "covariance", "2mm", "3mm", "atax", "bicg", "doitgen", "mvt", "gemm",
  "gemver", "gesummv", "symm", "syr2k", "syrk", "trmm", "durbin", "lu",
  "ludcmp", "trisolv", "deriche",  "floyd-warshall", "nussinov", "adi",
  "fdtd-2d", "heat-3d", "jacobi-1d", "jacobi-2d", "seidel-2d", "cholesky",
  "gramschmidt", "correlation"
]

mibench_list = [
  "basicmath", "bitcount", "qsort", "susan", "blowfish", "rijndael", "sha",
  "dijkstra", "patricia", "adpcm", "CRC32", "FFT", "gsm"
]


class SimpointSystem(System):
  """SE system with a NonCachingSimpleCPU (atomic_noncaching, cache-bypass)
  fast-forward set and a TunedCPU (O3) detailed set, ready for m5.switchCpus()."""

  _DetailedCPUModel = TunedCPU      # O3 model used for the measured region
  _ramulator2_use = False
  _ramulator2_memory_capacity = 1   # Ramulator2 timing-model DEVICE capacity (GB)
  _host_memory_capacity = 0         # Host DRAM = gem5 addr-range/backing (GB);
                                    # 0 -> fall back to _ramulator2_memory_capacity
  _ramulator2_config_path = ""
  _ramulator2_output_path = ""
  _num_process = 1
  _spec_cpu_path = ""
  _polybench_path = ""
  _run_path = ""

  def __init__(self):
    super(SimpointSystem, self).__init__()

    self.clk_domain = SrcClockDomain()
    self.clk_domain.clock = '3.5GHz'
    self.clk_domain.voltage_domain = VoltageDomain()

    # Start in atomic_noncaching mode so the NonCachingSimpleCPU fast-forward
    # phase BYPASSES the (wired) L1/L2/L3 caches at runtime for cacheless-speed
    # FF. Caches stay connected so switchCpus' takeOverFrom can hand the ports
    # to the O3 CPUs; BaseCache::CpuSidePort::recvAtomic just forwards packets
    # to mem_side while system->bypassCaches() is true (mem/cache/base.cc).
    # switchToDetailed() switches the system to 'timing' for the O3 CPUs, at
    # which point the same caches become active.
    # NOTE: caches are NOT warmed during FF in this mode (cold start after the
    # switch); use --warmup_insts > 0 if cache-warm accuracy is needed.
    self.mem_mode = 'atomic_noncaching'

    # --- Host DRAM capacity vs Ramulator2 device capacity (decoupled) --------
    # Host DRAM capacity = the gem5 physical address range the workload sees and
    # that gem5 backs with host memory (mem_ranges below). It is INDEPENDENT of
    # the Ramulator2 timing-model device capacity (_ramulator2_memory_capacity,
    # which is checked against the YAML org by ramulator2.cc:check_dram_capcity).
    # The Ramulator2 controller's gem5 range follows mem_ranges (host_cap), so
    # the system exposes host_cap of memory, while Ramulator2 internally models a
    # (larger) ramu_cap device geometry for timing/banking -- only the low
    # host_cap-sized address region is ever exercised.
    # Constraint: host_cap <= ramu_cap (else host addresses would exceed the
    # modeled device's address space -> Ramulator2 address mapping breaks).
    host_cap = self._host_memory_capacity or self._ramulator2_memory_capacity
    if host_cap > self._ramulator2_memory_capacity:
      m5.fatal("host_cap (%d GB) > ramu_cap (%d GB): Host DRAM must not exceed "
               "the Ramulator2 device capacity (address-mapping safety)."
               % (host_cap, self._ramulator2_memory_capacity))
    if host_cap != self._ramulator2_memory_capacity:
      print("[MEM] Host DRAM = %d GB (gem5 addr/backing), Ramulator2 device = "
            "%d GB (timing model)" % (host_cap, self._ramulator2_memory_capacity))
    mem_size = str(host_cap) + 'GB'
    self.mem_ranges = [AddrRange(Addr(mem_size), size = '100MB'),
                       AddrRange(mem_size)]

    np = self._num_process

    # ---- Fast-forward CPUs (active, atomic_noncaching = cache-bypass) ----
    # NonCachingSimpleCPU is an AtomicSimpleCPU subclass forcing
    # 'atomic_noncaching' memory mode; support_take_over() is True so the
    # existing m5.switchCpus(atomic_noncaching -> O3/timing) flow is unchanged.
    self.cpu = [NonCachingSimpleCPU(cpu_id=i) for i in range(np)]

    # ---- Detailed CPUs (switched out, O3, no private caches) ----
    # workload/isa are assigned later in finalizeSwitchCpus() (after the
    # fast-forward CPUs' createThreads() has populated isa).
    self.switch_cpus = [self._DetailedCPUModel(switched_out=True, cpu_id=i)
                        for i in range(np)]
    # NOTE: do NOT set switch_cpus[i].system = self here. At __init__ time the
    # System has no parent yet, so a SimObject param assigned an unparented
    # object gets ADOPTED as a child (SimObject.py), creating a self<->cpu
    # parent cycle -> RecursionError in path(). The CPUs are already children
    # of the System, so BaseCPU.system = Param.System(Parent.any) auto-resolves
    # (same as the fast-forward CPUs, which also never set .system explicitly).
    for i in range(np):
      self.switch_cpus[i].clk_domain = self.clk_domain

    # Create a memory bus
    self.membus = SystemXBar(width = 192)
    self.membus.badaddr_responder = BadAddr()
    self.membus.default = Self.badaddr_responder.pio

    self.system_port = self.membus.cpu_side_ports

    self.l3bus = L2XBar(width = 192,
                        snoop_filter = SnoopFilter(max_capacity='32MB'))

    # Caches attached ONLY to the fast-forward CPUs. switchCpus' takeOverFrom
    # rebinds these ports to the O3 CPUs. During FF (atomic_noncaching) these
    # caches are bypassed at runtime, so they carry over EMPTY (cold) to the O3
    # CPUs; the wiring exists purely so takeOverFrom has ports to hand over.
    for cpu in self.cpu:
      cpu.l2bus = L2XBar()
      cpu.icache = L1ICache()
      cpu.dcache = L1DCache()
      cpu.mmucache = MMUCache()
      cpu.icache.connectCPU(cpu)
      cpu.dcache.connectCPU(cpu)
      cpu.mmucache.connectCPU(cpu)
      cpu.icache.connectBus(cpu.l2bus)
      cpu.dcache.connectBus(cpu.l2bus)
      cpu.mmucache.connectBus(cpu.l2bus)
      cpu.l2cache = L2Cache()
      cpu.l2cache.connectCPUSideBus(cpu.l2bus)
      cpu.l2cache.connectMemSideBus(self.l3bus)

    self.l3cache = L3Cache()
    if np == 1:
      self.l3cache.size = '2MB'
    elif np == 2:
      self.l3cache.size = '4MB'
    elif np == 4:
      self.l3cache.size = '8MB'
    elif np == 8:
      self.l3cache.size = '16MB'
    self.l3cache.connectCPUSideBus(self.l3bus)
    self.l3cache.connectMemSideBus(self.membus)

    for i in range(np):
      self.cpu[i].createInterruptController()
      self.cpu[i].interrupts[0].pio = self.membus.mem_side_ports
      self.cpu[i].interrupts[0].int_requestor = self.membus.cpu_side_ports
      self.cpu[i].interrupts[0].int_responder = self.membus.mem_side_ports

    self.createMemoryControllersDDR4()

  # ---------------------------------------------------------------------------
  # Memory controllers (copied verbatim from se.py / MySystem)
  # ---------------------------------------------------------------------------
  def createMemoryControllersDDR4(self):
    self._createMemoryControllers(1, DDR4_2400_16x4)

  def _createMemoryControllers(self, num, cls):
    kernel_controller = self._createKernelMemoryController(cls)
    ranges = self._getInterleaveRanges(self.mem_ranges[-1], num, 6, 20)

    mcs = []
    for i in range(num):
      if self._ramulator2_use == True:
        intf = ObjectList.mem_list.get("Ramulator2")
        if issubclass(intf, m5.objects.Ramulator2):
            print(" ============= USE RAMULATOR ============== ")
            print("Ramualtor2 CONFIG PATH : ", self._ramulator2_config_path)
            print("Ramualtor2 OUTPUT PATH : ", self._ramulator2_output_path)
            test_interface = intf()
            test_interface.range = ranges[i]
            test_mem_ctrl = test_interface
            test_mem_ctrl.config_path   = self._ramulator2_config_path
            test_mem_ctrl.output_path   = self._ramulator2_output_path
            test_mem_ctrl.dram_capacity = self._ramulator2_memory_capacity
            test_mem_ctrl.port = self.membus.mem_side_ports
            mcs.append(test_mem_ctrl)
        else:
            exit(1)
      else:
        print("Use Gem5 DRAM Intf")
        mcs.append(MemCtrl(dram = cls(range = ranges[i]), port = self.membus.mem_side_ports))

    self.mem_cntrls = [mcs[i] for i in range(num)] + [kernel_controller]

  def _createKernelMemoryController(self, cls):
    return MemCtrl(dram = cls(range = self.mem_ranges[0]), port = self.membus.mem_side_ports)

  def _getInterleaveRanges(self, rng, num, intlv_low_bit, xor_low_bit):
    from math import log
    bits = int(log(num, 2))
    if 2**bits != num:
        m5.fatal("Non-power of two number of memory controllers")
    intlv_bits = bits
    ranges = [
        AddrRange(start=rng.start, end=rng.end,
                  intlvHighBit = intlv_low_bit + intlv_bits - 1,
                  xorHighBit = xor_low_bit + intlv_bits - 1,
                  intlvBits = intlv_bits,
                  intlvMatch = i)
            for i in range(num)
        ]
    return ranges

  # ---------------------------------------------------------------------------
  # Workload setup - assigns to the FAST-FORWARD CPUs (self.cpu).
  # The detailed CPUs share the same Process objects via finalizeSwitchCpus().
  # ---------------------------------------------------------------------------
  def setTestBinary(self, binary_path):
    self.cpu[0].workload = Process(cmd = [binary_path], executable = binary_path)
    self.cpu[0].createThreads()
    process0_path = self.cpu[0].workload[0].executable
    self.workload = SEWorkload.init_compatible(process0_path)

  def setSpecBenchmark(self, _is_test, bench, np):
    print("SPEC CPU Path:", self._spec_cpu_path)
    for i in range(np):
      cwd_path = self._run_path + "/core_" + str(i) + "_" + bench
      spec_abs_path = get_spec_bench_path(self._spec_cpu_path, bench, _is_test)
      self.cpu[i].workload = set_spec_bench(spec_abs_path, False, bench, i*100, cwd_path)
      print(" -- process.cmd:", self.cpu[i].workload[0].cmd)
      self.cpu[i].createThreads()
    process0_path = self.cpu[0].workload[0].executable
    self.workload = SEWorkload.init_compatible(process0_path)

  def setPolyBenchmark(self, bench, np):
    for i in range(np):
      cwd_path = self._run_path + "/core_" + str(i) + "_" + bench
      poly_abs_path = get_poly_bench_path(self._polybench_path, bench)
      self.cpu[i].workload = set_polybench(poly_abs_path, bench, i*100, cwd_path)
      print(" -- process.cmd:", self.cpu[i].workload[0].cmd)
      self.cpu[i].createThreads()
    process0_path = self.cpu[0].workload[0].executable
    self.workload = SEWorkload.init_compatible(process0_path)

  def setMibench(self, bench, np):
    for i in range(np):
      self.cpu[i].workload = set_mibench(bench, i*100)
      print(" -- process.cmd:", self.cpu[i].workload[0].cmd)
      self.cpu[i].createThreads()
    process0_path = self.cpu[0].workload[0].executable
    self.workload = SEWorkload.init_compatible(process0_path)

  def setMixbench(self, bench, np):
    mix_bench = bench.split(":")
    if len(mix_bench) != np:
      print("Mix Bench Only Support 4 Core! {}".format(np))
      exit(1)
    for i in range(np):
      cwd_path = self._run_path + "/core_" + str(i) + "_" + mix_bench[i]
      if mix_bench[i] in spec_benchmark_list:
        spec_abs_path = get_spec_bench_path(self._spec_cpu_path, mix_bench[i], False)
        self.cpu[i].workload = set_spec_bench(spec_abs_path, False, mix_bench[i], i*100, cwd_path)
        print(" -- process.cmd:", self.cpu[i].workload[0].cmd)
      elif mix_bench[i] in polybench_list:
        poly_abs_path = get_poly_bench_path(self._polybench_path, mix_bench[i])
        self.cpu[i].workload = set_polybench(poly_abs_path, mix_bench[i], i*100, cwd_path)
        print(" -- process.cmd:", self.cpu[i].workload[0].cmd)
      else:
        print("Not Support Benchmark {} ! Only SPEC CPU or Polybench".format(mix_bench[i]))
        exit(1)
      self.cpu[i].createThreads()
    process0_path = self.cpu[0].workload[0].executable
    self.workload = SEWorkload.init_compatible(process0_path)

  # ---------------------------------------------------------------------------
  # Switch-CPU finalization + the actual switch.
  # ---------------------------------------------------------------------------
  def finalizeSwitchCpus(self):
    """Bind the detailed (O3) CPUs to the same workload/isa as the FF CPUs and
    create their threads. MUST be called AFTER set*Benchmark() (which runs the
    FF CPUs' createThreads(), populating isa)."""
    np = self._num_process
    for i in range(np):
      self.switch_cpus[i].workload = self.cpu[i].workload
      self.switch_cpus[i].isa = self.cpu[i].isa
      self.switch_cpus[i].createThreads()

  def switchToDetailed(self):
    """Switch from the atomic fast-forward CPUs to the O3 detailed CPUs.
    m5.switchCpus drains, changes memory mode atomic->timing, and rebinds the
    cache ports via takeOverFrom (warm caches carry over)."""
    import m5
    m5.switchCpus(self, list(zip(self.cpu, self.switch_cpus)))
