#
# twas the third day of xmas...
#

from functools import reduce
import string
from typing import List, Tuple

from advent.utils import iterate_over_data

CHARS = list(string.ascii_letters)

def priority(character: str):
    """Convert an ascii character to value"""
    return CHARS.index(character) + 1

def split(backpack: str) -> Tuple[str, str]:
    """Split a backpack <str> into two lists of items"""
    split_at = int(len(backpack) / 2)
    return backpack[:split_at], backpack[split_at:]

def find_overlap(first: str, second: str) -> str:
    """Find the overlapping characters in a string"""
    s1 = set(list(first))
    s2 = set(list(second))
    return "".join(list(s1 & s2))

def reorder_rucksacks():
    """Path One"""
    overlap: List[str] = []
    for backpack in iterate_over_data('rucksack.txt'):
        overlap.append(find_overlap(*split(backpack)))
    return sum([priority(x) for x in overlap])

def overlap_wrapper(*args: str) -> str:
    """Wrapper for finding the overlap in more than two strings"""
    return reduce(find_overlap, args)

def auth_stickers() -> int:
    """Part Two"""
    rucksacks = iterate_over_data('rucksack.txt')
    overlap: List[str] = []
    for r1, r2, r3 in zip(rucksacks, rucksacks, rucksacks):
        overlap.append(overlap_wrapper(r1, r2, r3))
    return sum([priority(x) for x in overlap])

