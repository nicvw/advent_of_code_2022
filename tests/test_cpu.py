from textwrap import dedent
from dataclasses import dataclass, field
from pathlib import Path

import pytest
from _pytest.capture import CaptureResult, CaptureFixture

from advent.cpu import CPU, load_instructions

@dataclass
class CpuTestData:
    file: Path
    cycles: int
    register: int
    signal_cycle: int
    signal_sum: int
    stdout: str
    cpu: CPU = field(init=False)

    def __post_init__(self):
        self.cpu = CPU(load_instructions(self.file.open()))

class TestCPU:
    tests = [
        CpuTestData(
            file=Path("data/cpu_demo1.txt"),
            cycles=5,
            register=-1,
            signal_cycle=20,
            signal_sum=0,
            stdout="#####"
        ),
        CpuTestData(
            file=Path("data/cpu_demo2.txt"),
            cycles=240,
            register=17,
            signal_cycle=260,
            signal_sum=13140,
            stdout=dedent("""
                ##..##..##..##..##..##..##..##..##..##..
                ###...###...###...###...###...###...###.
                ####....####....####....####....####....
                #####.....#####.....#####.....#####.....
                ######......######......######......####
                #######.......#######.......#######.....
                """).lstrip()
        ),
    ]

    def test_cpu(self, capsys: CaptureFixture):  # type: ignore
        for t in self.tests:
            t.cpu()
            assert t.cpu.cycles == t.cycles
            assert t.cpu.x_register == t.register
            assert t.cpu.signal_cycle == t.signal_cycle
            assert sum(t.cpu.signal_strength) == t.signal_sum
            captured = capsys.readouterr()  # type: ignore
            assert captured.out == t.stdout  # type: ignore
