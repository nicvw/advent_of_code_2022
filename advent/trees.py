#
# twas the eighth day of xmas...
#

from dataclasses import dataclass, field
from typing import Iterator, List, Set, Tuple

Row = List[int]
Coordinate = Tuple[int, int]

@dataclass
class TreeTops:
    input: Iterator[str]
    rows: List[Row] = field(default_factory=list)
    max_x: int = field(init=False)
    max_y: int = field(init=False)
    coordinates: Set[Coordinate] = field(default_factory=set)

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
        # print("")
        # process rows
        for y in range(1, self.max_y - 1):
            # top -> down
            max_height=self.rows[y][0]
            self._row(y=y, start=1, end=self.max_x - 1, max_height=max_height)
            # bottom -> up
            max_height=self.rows[y][-1]
            self._row(y=y, start=self.max_x - 2, end=0, step=-1 , max_height=max_height)

        # process columns
        for x in range(1, self.max_x - 1):
            # top -> down
            max_height = self.rows[0][x]
            self._column(x, 1, self.max_y - 1, max_height)
            # bottom -> up
            max_height = self.rows[-1][x]
            self._column(x=x, start=self.max_y - 2, end=0, max_height=max_height, step=-1)

    @property
    def trees(self) -> int:
        return len(self.coordinates)

    def _tree(self, x: int, y: int, max_height: int) -> int:
        # print(f"col: {x}, row: {y}")
        if self.rows[y][x] > max_height:
            self.coordinates.add((x, y))
            max_height = self.rows[y][x]
        return max_height

    def _row(self, y: int, start: int, end: int, max_height: int, step: int = 1):
        for x in range(start, end, step):
            if max_height == 9:
                # print("break: max height reached")
                return
            max_height = self._tree(x, y, max_height)

    def _column(self, x: int, start: int, end: int, max_height: int, step: int = 1):
        for y in range(start, end, step):
            if max_height == 9:
                # print("break: max height reached")
                return
            max_height = self._tree(x, y, max_height)
