#
# twas the eighth day of xmas...
#

from dataclasses import dataclass, field
from typing import Iterator, List, Set, Tuple

Row = List[int]
Coordinate = Tuple[int, int]

@dataclass
class TreeSurveyor:
    trees: List[int]
    viable: Set[int] = field(default_factory=set)
    index: int = 0
    highest: int = field(init=False)

    def __post_init__(self):
        self.index = len(self.trees) - 1
        self.highest = self.trees[0]

    def __call__(self):
        self._compare(1)
        self.highest = self.trees[-1]
        self._compare(len(self.trees) - 2)
        return self.viable

    def _compare(self, start: int):
        index = self.index
        self.index = 0 if start < index else -1
        for i in range(start, index, 1 if start < index else -1):
            if self.highest == 9:
                break
            elif self.trees[i] > self.highest:
                self.viable.add(i)
                self.highest = self.trees[i]
                self.index = i - 1
            elif self.trees[i] == self.highest:
                self.index = i - 1

@dataclass
class TreeTops:
    input: Iterator[str]
    rows: List[Row] = field(default_factory=list)
    max_x: int = field(init=False)
    max_y: int = field(init=False)
    coordinates: Set[Coordinate] = field(default_factory=set)
    # max_score: Tuple[Coordinate, int] = field(init=False)

    def __post_init__(self):
        for row in self.input:
            self.rows.append([int(x) for x in row])
        self.max_x = len(self.rows[0])
        self.max_y = len(self.rows)

        # add all the trees on the boundary
        for x in range(self.max_x):
            self.coordinates.add((x, 0))
            self.coordinates.add((x, self.max_y - 1))
        for y in range(self.max_y):
            self.coordinates.add((0, y))
            self.coordinates.add((self.max_x - 1, y))

    def __call__(self):
        # process rows
        for y in range(1, self.max_y - 1):
            surveyor = TreeSurveyor(self.rows[y])
            for x in surveyor():
                self.coordinates.add((x, y))

        # process columns
        for x in range(1, self.max_x - 1):
            surveyor = TreeSurveyor([r[x] for r in self.rows])
            for y in surveyor():
                self.coordinates.add((x, y))

    @property
    def trees(self) -> int:
        return len(self.coordinates)

    def _score_row(self, x: int, y: int, height: int, reverse: bool = False) -> int:
        score = 0
        row = self.rows[y]
        trees = row[x+1:] if reverse else row[x-1::-1]
        for tree in trees:
            score += 1
            if tree >= height:
                break
        return score

    def _score_column(self, x: int, y: int, height: int, reverse: bool = False) -> int:
        score = 0
        column = [row[x] for row in self.rows]
        trees = column[y+1:] if reverse else column[y-1::-1]
        for tree in trees:
            score += 1
            if tree >= height:
                break
        return score
