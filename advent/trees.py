from dataclasses import dataclass, field
from typing import Iterator, List, Set, Tuple

Row = List[str]
Coordinate = Tuple[int, int]

@dataclass
class TreeTops:
    input: Iterator[str]
    rows: List[Row] = field(default_factory=list)
    max_x: int = field(init=False)
    max_y: int = field(init=False)
    coordinates: List[Coordinate] = field(default_factory=list)

    def __post_init__(self):
        for row in self.input:
            self.rows.append(list(row))
        self.max_x = len(self.rows[0])
        self.max_y = len(self.rows)

        # add all the trees on the boundary
        for x in range(self.max_x):
            self.coordinates.append((x, 0))
            self.coordinates.append((x, self.max_y - 1))
        for y in range(self.max_y):
            self.coordinates.append((0, y))
            self.coordinates.append((self.max_x - 1, y))

    def __call__(self):
        for index, row in enumerate(self.rows[1:-1]):
            self._process_row(row, index + 1)
        self._process_columns()

    @property
    def trees(self) -> int:
        return len(self.coordinates)

    def _process_row(self, row: Row, x: int):
        for y, height in enumerate(row[1:-1]):
            if height > row[y]:
                self.coordinates.append((x, y + 1))
                continue
            break
        for y, height in enumerate(row[-2:0:-1]):
            if height > row[-y - 3]:
                self.coordinates.append((x, self.max_y - y - 2))
                continue
            break

    def _process_columns(self):
        for x in range(1, self.max_x - 1):
            # print(f"x: {x}")
            for y in range(1, self.max_y - 1):
                # print(f"y: {y}")
                if self.rows[y][x] > self.rows[y - 1][x]:
                    # print(f"positive: {(x, y)}")
                    # print(f"{self.rows[y][x]} > {self.rows[y - 1][x]}")
                    self.coordinates.append((x, y))
                    continue
                break
            for y in range(-2, -self.max_y - 1, -1):
                print(f"y: {y}")
                if self.rows[y][x] > self.rows[y + 1][x]:
                    print(f"negative {(x, self.max_y + y)}")
                    print(f"{self.rows[y][x]} > {self.rows[y + 1][x]}")
                    self.coordinates.append((x, self.max_y + y))
                    continue
                break
