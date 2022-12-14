#
# twas the seventh day of xmas...
#

from textwrap import dedent
import pytest
from typing import Iterable

from advent.storage_device import Storage


@pytest.fixture
def test_data() -> Iterable[str]:
    data = dedent("""
    $ cd /
    $ ls
    dir a
    14848514 b.txt
    8504156 c.dat
    dir d
    $ cd a
    $ ls
    dir e
    29116 f
    2557 g
    62596 h.lst
    $ cd e
    $ ls
    584 i
    $ cd ..
    $ cd ..
    $ cd d
    $ ls
    4060174 j
    8033020 d.log
    5626152 d.ext
    7214296 k""").split("\n")
    return iter([x for x in data if x])

@pytest.fixture
def iut(test_data: Iterable[str]):
    return Storage(test_data)

def test_storage(iut: Storage):
    assert iut.directories["/a/e"] == 584
    assert iut.directories["/a"] == 94853
    assert iut.directories["/d"] == 24933642
    assert iut.directories["/"] == 48381165
    assert sum([v for v in iut.directories.values() if v <= 100000]) == 95437

def test_freeup_space(iut: Storage):
    assert iut.freeup_space(30000000) == ("/d", 24933642)
