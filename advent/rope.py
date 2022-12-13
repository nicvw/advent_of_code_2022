from __future__ import annotations

from dataclasses import dataclass, field
from typing import Iterable, List, Literal, TextIO, Tuple

from rich import print
from typer import confirm

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
    history: List[Coordinate] = field(default_factory=list)

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

    def move(self, x: int, y: int):
        self.x += x
        self.y += y
        self._update()

    def _update(self):
        self.history.append((self.x, self.y))


@dataclass
class Rope:
    moves: List[Motion]
    knots: List[Knot]

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
            for i in range(len(self.knots)):
                if i == 0:
                    self.knots[i].move(*move)
                    continue

                previous_knot = self.knots[i-1]

                if self.knots[i].adjacent(previous_knot) or previous_knot == self.knots[i]:
                    self.knots[i].move(0, 0)
                    continue

                if self.knots[i].y - previous_knot.y not in (-1, 0, 1):
                    move = previous_knot.x - self.knots[i].x, move[1]
                elif self.knots[i].x - previous_knot.x not in (-1, 0, 1):
                    move = move[0], previous_knot.y - self.knots[i].y

                self.knots[i].move(*move)


@dataclass
class Plotter:
    rope: Rope
    offset: Coordinate = field(init=False)
    graph: List[List[str]] = field(default_factory=list)
    max_moves: int = field(init=False)
    rows: int = field(init=False)
    cols: int = field(init=False)


    def __post_init__(self):
        self.max_moves = len(self.rope.knots[0].history)
        max_x = 0
        max_y = 0
        min_x = 0
        min_y = 0
        for knot in self.rope.knots:
            for x, y in knot.history:
                max_x = x if x > max_x else max_x
                max_y = y if y > max_y else max_y
                min_x = x if x < min_x else min_x
                min_y = y if y < min_y else min_y
        self.offset = (0 - min_x, 0 - min_y)
        self.cols = max_x - min_x
        self.rows = max_y - min_y
        self._blank_graph()
        self.graph[0 + self.offset[1]][0 + self.offset[0]] = "0"

    def _blank_graph(self):
        self.graph = [["." for _ in range(self.cols)] for _ in range(self.rows)]

    def _print(self, heading: str):
        print(f"== {heading} ==")
        print("")
        for row in self.graph:
            print(" ".join(row))
        print("")


    def play(self):
        knots = len(self.rope.knots)
        i = 0
        self._print("Initial State")
        confirm("continue?", abort=True)
        for move, num in self.rope.moves:
            i += num
            self._blank_graph()
            for k in range(knots-1, -1, -1):
                try:
                    x, y = self.rope.knots[k].history[i]
                except IndexError:
                    continue
                self.graph[y + self.offset[1]][x + self.offset[0]] = f"{k}"
            self._print(f"{move} {num}")
            confirm("continue?", abort=True)


def load_rope(data: TextIO) -> List[Motion]:
    return [(x, int(y)) for x, y in [m.split() for m in data]] # type: ignore