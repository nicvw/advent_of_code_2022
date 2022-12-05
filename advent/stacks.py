#
# twas the fifth day of xmas...
#

from dataclasses import dataclass
import re
from typing import Iterator, List

Stack = List[str]
MoveRegex = re.compile(r"move (?P<num>\d+) from (?P<src>\d+) to (?P<dst>\d+)")

@dataclass
class Move:
    num: int
    src: int
    dst: int

    def __post_init__(self):
        """Account for zero-indexed lists in Python"""
        if self.src > 0:
            self.src -= 1
        if self.dst > 0:
            self.dst -= 1


@dataclass
class SupplyStacks:
    stacks: List[Stack]
    moves: Iterator[str]

    @staticmethod
    def parse_move(move: str) -> Move:
        """Convert a move `move 1 from 3 to 5` to an instance of Move"""
        match = MoveRegex.search(move)
        if match is not None:
            return Move(*[int(x) for x in match.groups()])
        return Move(0, 0, 0)

    def _move_a_crate(self, move: Move):
        """Move an individual crate between two stacks"""
        for _ in range(move.num):
            self.stacks[move.dst].append(self.stacks[move.src].pop())

    def _move_a_stack(self, move: Move):
        """Move ordered set of crates between two stacks"""
        stack: List[str] = []
        for _ in range(move.num):
            stack.append(self.stacks[move.src].pop())
        self.stacks[move.dst] += reversed(stack)

    def move(self, multi: bool = False):
        """Process all the move operations"""
        for m in self.moves:
            m = self.parse_move(m)
            if multi:
                self._move_a_stack(m)
            else:
                self._move_a_crate(m)
