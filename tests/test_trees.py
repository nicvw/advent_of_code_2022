#
# twas the eighth day of xmas...
#

from textwrap import dedent
from typing import  Iterator, List
import pytest

from advent.trees import TreeTops

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
def test_data() -> List[List[str]]:
    return [
        ['3', '0', '3', '7', '3'],
        ['2', '5', '5', '1', '2'],
        ['6', '5', '3', '3', '2'],
        ['3', '3', '5', '4', '9'],
        ['3', '5', '3', '9', '0']
    ]

@pytest.fixture()
def iut(test_input: Iterator[str]):
    return TreeTops(input=test_input)

def test_instantiation(iut: TreeTops, test_data: List[List[str]]):
    assert iut.rows == test_data
    assert iut.max_x == 5
    assert iut.max_y == 5
    assert iut.trees == 16


def test_tree_tops(iut: TreeTops, test_data: List[List[str]]):
    iut()
    assert iut.trees == 21
    print(iut.coordinates)
