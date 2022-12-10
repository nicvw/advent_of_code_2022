#
# twas the eighth day of xmas...
#

from dataclasses import dataclass
from typing import List, Set
import pytest

from advent.trees import TreeSurveyor, TreeTops, ViewFinder, ViewScoreCalculator

TestData = List[List[int]]

@pytest.fixture()
def test_data() -> TestData:
    return [
        [3, 0, 3, 7, 3],
        [2, 5, 5, 1, 2],
        [6, 5, 3, 3, 2],
        [3, 3, 5, 4, 9],
        [3, 5, 3, 9, 0]
    ]

@pytest.fixture()
def test_viable() -> List[Set[int]]:
    return [
        {3},
        {1, 2},
        {1, 3},
        {2},
        {1, 3}
    ]

@pytest.fixture()
def treetops(test_data: TestData):
    return TreeTops(rows=test_data)

def test_instantiation(treetops: TreeTops, test_data: List[List[str]]):
    assert treetops.rows == test_data
    assert treetops.max_x == 5
    assert treetops.max_y == 5
    assert treetops.trees == 16

def test_tree_tops(treetops: TreeTops):
    treetops()
    assert treetops.trees == 21
    # assert treetops.high_score == 8
    # assert treetops.best_location == (2, 3)

def test_tree_surveyor(test_data: TestData, test_viable: List[Set[int]]):
    for trees, viable in zip(test_data, test_viable):
        surveyor = TreeSurveyor(trees)
        assert surveyor() == viable


@dataclass
class ViewScoreCalculatorCreator:
    trees: List[int]
    index: int
    output: int

    @property
    def calculator(self):
        return ViewScoreCalculator(self.index, self.trees)


class TestViewScoreCalculator:
    tests = [
        ViewScoreCalculatorCreator(
            trees=[3, 3, 5, 4, 9],
            index=2,
            output=4
        ),
        ViewScoreCalculatorCreator(
            trees=[3, 5, 3, 5, 3],
            index=3,
            output=2
        ),
    ]

    def test_calculator(self):
        for t in self.tests:
            assert t.calculator() == t.output


def test_view_finder(test_data: TestData):
    view_finder = ViewFinder(test_data)
    output = {
            "score": 8,
            "coordinate": (2, 3)
        }
    assert view_finder() == output
