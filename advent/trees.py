#
# twas the eighth day of xmas...
#

from dataclasses import dataclass, field
from typing import Dict, List, Set, Tuple

Trees = List[int]
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
    # input: Iterator[str]
    rows: List[Trees]
    coordinates: Set[Coordinate] = field(default_factory=set)
    max_x: int = field(init=False)
    max_y: int = field(init=False)

    def __post_init__(self):
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
                if (x, y) in self.coordinates:
                    continue
                self.coordinates.add((x, y))

        # process columns
        for x in range(1, self.max_x - 1):
            surveyor = TreeSurveyor([r[x] for r in self.rows])
            for y in surveyor():
                if (x, y) in self.coordinates:
                    continue
                self.coordinates.add((x, y))

    @property
    def trees(self) -> int:
        return len(self.coordinates)


@dataclass
class ViewScoreCalculator:
    """Calculate the product of the view distance from the tree"""
    index: int
    trees: Trees
    scores: List[int] = field(default_factory=list)
    before: int = 0
    behind: int = 0
    height: int = field(init=False)

    def __post_init__(self):
        self.height = self.trees[self.index]

    def __call__(self) -> int:
        for i, height in enumerate(self.trees):
            if i < self.index:
                if height < self.height:
                    self.before += 1
                else:
                    self.before = 1
            elif i > self.index:
                if height < self.height:
                    self.behind += 1
                else:
                    self.behind += 1
                    break
        return self.before * self.behind


@dataclass
class ViewFinder:
    """Process rows of trees for find the tree with the highest view score"""
    trees: List[Trees]
    score: int = 0
    coordinate: Coordinate = field(init=False)

    def __call__(self) -> Dict[str, int | Coordinate]:
        max_x = len(self.trees[0])
        max_y = len(self.trees)
        for x in range(max_x):
            if x == 0 or x == max_x - 1:
                continue
            for y in range(len(self.trees)):
                if y == 0 or y == max_y - 1:
                    continue
                self._calculate_view_score(x, y)

        return {
            "score": self.score,
            "coordinate": self.coordinate
        }

    def _calculate_view_score(self, x: int, y: int):
        row_calc = ViewScoreCalculator(x, self.trees[y])
        col_calc = ViewScoreCalculator(y, [r[x] for r in self.trees])
        score = row_calc() * col_calc()
        if score > self.score:
            self.score = score
            self.coordinate = (x, y)
