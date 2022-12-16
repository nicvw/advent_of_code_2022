from dataclasses import dataclass, field
from pathlib import Path

from advent.cpu import CPU, load_instructions

@dataclass
class CpuTestData:
    file: Path
    cycles: int
    register: int
    signal_cycle: int
    signal_sum: int
    cpu: CPU = field(init=False)

    def __post_init__(self):
        self.cpu = CPU(load_instructions(self.file.open()))
        self.cpu()

class TestCPU:
    tests = [
        CpuTestData(
            file=Path("data/cpu_demo1.txt"),
            cycles=5,
            register=-1,
            signal_cycle=20,
            signal_sum=0
        ),
        CpuTestData(
            file=Path("data/cpu_demo2.txt"),
            cycles=240,
            register=17,
            signal_cycle=260,
            signal_sum=13140
        ),
    ]

    def test_cpu(self):
        for t in self.tests:
            assert t.cpu.cycles == t.cycles
            assert t.cpu.x_register == t.register
            assert t.cpu.signal_cycle == t.signal_cycle
            assert sum(t.cpu.signal_strength) == t.signal_sum
