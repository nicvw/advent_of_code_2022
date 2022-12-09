#
# twas the eighth day of xmas...
#

from textwrap import dedent
from typing import  Iterator, List, Set
import pytest

from advent.trees import TreeSurveyor, TreeTops

@pytest.fixture()
def test_input() -> Iterator[str]:
    data = dedent("""
    30373
    25512
    65332
    33549
    35390""").splitlines()
    return iter(x for x in data if x)

@pytest.fixture()
def test_data() -> List[List[int]]:
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
def treetops(test_input: Iterator[str]):
    return TreeTops(input=test_input)

def test_instantiation(treetops: TreeTops, test_data: List[List[str]]):
    assert treetops.rows == test_data
    assert treetops.max_x == 5
    assert treetops.max_y == 5
    assert treetops.trees == 16

def test_tree_tops(treetops: TreeTops):
    treetops()
    assert treetops.trees == 21
    print(treetops.coordinates)

def test_tree_surveyor(test_data: List[List[int]], test_viable: List[Set[int]]):
    for trees, viable in zip(test_data, test_viable):
        surveyor = TreeSurveyor(trees)
        assert surveyor() == viable
