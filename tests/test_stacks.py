from dataclasses import dataclass
from typing import Tuple

from advent.stacks import SupplyStacks


@dataclass
class ParseMoveTestData:
    input: str
    output: Tuple[int, int, int]

class TestParseMove:
    tests = [
        ParseMoveTestData(
            "move 1 from 3 to 5",
            (1, 2, 4,)
        ),
        ParseMoveTestData(
            "move 10 from 35 to 15",
            (10, 34, 14,)
        ),
        ParseMoveTestData(
            "move 0 from 0 to 0",
            (0, 0, 0,)
        ),
        ParseMoveTestData(
            "move sea from dog to cat",
            (0, 0, 0,)
        ),
    ]

    def test_parse_move(self):
        for t in self.tests:
            m = SupplyStacks.parse_move(t.input)
            assert (m.num, m.src, m.dst,) == t.output


class TestMove:
    moves = [
        "move 1 from 2 to 1",
        "move 3 from 1 to 3",
        "move 2 from 2 to 1",
        "move 1 from 1 to 2",
    ]
    stacks = [
        ["Z", "N"],
        ["M", "C", "D"],
        ["P"]
    ]
    single_result = [
        ["C"],
        ["M"],
        ["P", "D", "N", "Z"]
    ]
    multi_result = [
        ["M"],
        ["C"],
        ["P", "Z", "N", "D"]
    ]

    def test_single_move(self):
        s = SupplyStacks(stacks=self.stacks, moves=iter(self.moves))
        s.move()
        assert s.stacks == self.single_result

    def test_multi_move(self):
        s = SupplyStacks(stacks=self.stacks, moves=iter(self.moves))
        s.move(True)
        assert s.stacks == self.multi_result