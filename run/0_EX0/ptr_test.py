from gem5.components.boards.simple_board import SimpleBoard
from gem5.components.cachehierarchies.classic.no_cache import NoCache
from gem5.components.memory.single_channel import SingleChannelDDR3_1600
from gem5.components.processors.simple_processor import SimpleProcessor
from gem5.components.processors.cpu_types import CPUTypes
from gem5.resources.resource import Resource
from gem5.simulate.simulator import Simulator
from gem5.resources.resource import CustomResource


# Obtain the components.
cache_hierarchy = NoCache()
memory = SingleChannelDDR3_1600("1GiB")
processor = SimpleProcessor(cpu_type=CPUTypes.TIMING, num_cores=1)

# Add them to the board.
board = SimpleBoard(
    clk_freq="3GHz",
    processor=processor,
    memory=memory,
    cache_hierarchy=cache_hierarchy,
)

# Set the workload.
# binary = Resource("x86-hello64-static")
binary = CustomResource("/home/gem5/gem5/run/0_EX0/ptr_test")
board.set_se_binary_workload(binary)


simulator = Simulator(board=board)
simulator._instantiate()
simulator._board.processor.cores[0].core.workload[0].map(
    0x50000, 0x2000, 1024, False
)
simulator.run()
