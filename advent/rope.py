from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Literal, Set, Tuple

Coordinate = Tuple[int, int]
Direction = Literal['U', 'D', 'L', 'R']
Up = Tuple[Literal[0], Literal[1]]
Down = Tuple[Literal[0], Literal[-1]]
Left = Tuple[Literal[-1], Literal[0]]
Right = Tuple[Literal[1], Literal[0]]
Motion = Tuple[Direction, int]


@dataclass
class PositionTracker:
    x: int = field(default=0)
    y: int = field(default=0)
    history: Set[Coordinate] = field(default_factory=set)

    def __post_init__(self):
        self._update()

    def __eq__(self, __o: object) -> bool:
        return self.x == __o.__dict__['x'] and self.y == __o.__dict__['y']

    @property
    def neighbours(self) -> Iterable[Coordinate]:
        """Iterate and yield neighboring coordinates"""
        for xadjust in  (-1, 0, 1,):
            for yadjust in (-1, 0, 1,):
                if xadjust == 0 and yadjust == 0:
                    continue
                yield (self.x + xadjust, self.y + yadjust)

    @property
    def position(self) -> Coordinate:
        return self.x, self.y

    def adjacent(self, other: PositionTracker) -> bool:
        return other.position in self.neighbours

    def relative(self, other: PositionTracker) -> Coordinate:
        return (other.x - self.x, other.y - self.y)

    def aligned(self, other: PositionTracker) -> bool:
        return self.x == other.x or self.y == other.y

    def move(self, x: int, y: int):
        self.x += x
        self.y += y
        self._update()

    def _update(self):
        self.history.add((self.x, self.y))


@dataclass
class Orchestrator:
    moves: List[Motion]
    head: PositionTracker = field(default_factory=PositionTracker)
    tail: PositionTracker = field(default_factory=PositionTracker)

    @property
    def U(self) -> Coordinate:
        return (0, 1)

    @property
    def D(self) -> Coordinate:
        return (0, -1)

    @property
    def L(self) -> Coordinate:
        return (-1, 0)

    @property
    def R(self) -> Coordinate:
        return (1, 0)

    @property
    def _aligned(self):
        return self.tail.aligned(self.head)

    def __call__(self):
        for direction, num in self.moves:
            self.move(direction=direction, num=num)
    
    def move(self, direction: Direction, num: int):
        for _ in range(num):
            move = getattr(self, direction)
            self.head.move(*move)

            if self.tail.adjacent(self.head) or self.head == self.tail:
                continue

            if self.tail.y - self.head.y in (-2, 2):
                move = self.head.x - self.tail.x, move[1]
            elif self.tail.x - self.head.x in (-2, 2):
                move = move[0], self.head.y - self.tail.y

            self.tail.move(*move)

