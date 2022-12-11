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
class Knot:
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

    def adjacent(self, other: Knot) -> bool:
        return other.position in self.neighbours

    def relative(self, other: Knot) -> Coordinate:
        return (other.x - self.x, other.y - self.y)

    # def aligned(self, other: Knot) -> bool:
    #     return self.x == other.x or self.y == other.y

    def move(self, x: int, y: int):
        self.x += x
        self.y += y
        self._update()

    def _update(self):
        self.history.add((self.x, self.y))


@dataclass
class Rope:
    moves: List[Motion]
    knots: List[Knot]

    # head: Knot = field(default_factory=Knot)
    # tail: Knot = field(default_factory=Knot)

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

    def __call__(self):
        for direction, num in self.moves:
            self.move(direction=direction, num=num)
    
    def move(self, direction: Direction, num: int):
        for _ in range(num):
            move: Coordinate = getattr(self, direction)
            for i, knot in enumerate(self.knots):
                if i == 0:
                    knot.move(*move)
                    continue

                previous_knot = self.knots[i-1]

                if knot.adjacent(previous_knot) or previous_knot == knot:
                    continue

                if knot.y - previous_knot.y in (-2, 2):
                    move = previous_knot.x - knot.x, move[1]
                elif knot.x - previous_knot.x in (-2, 2):
                    move = move[0], previous_knot.y - knot.y

                knot.move(*move)

