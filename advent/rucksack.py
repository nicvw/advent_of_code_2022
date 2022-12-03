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
    s1 = set(list(first))
    s2 = set(list(second))
    return (s1 & s2).pop()

def process_rucksacks_from_data():
    overlap: List[str] = []
    for backpack in iterate_over_data('data/rucksack.txt'):
        overlap.append(find_overlap(*split(backpack)))
    return sum([priority(x) for x in overlap])
