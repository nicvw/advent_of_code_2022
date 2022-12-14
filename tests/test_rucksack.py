from dataclasses import dataclass
from typing import Tuple

from advent.rucksack import overlap_wrapper, priority, split


@dataclass
class PriorityTestData:
    input: str
    output: int


class TestPriority:
    data = [
        PriorityTestData(input='a', output=1),
        PriorityTestData(input='p', output=16),
        PriorityTestData(input='L', output=38),
        PriorityTestData(input='P', output=42),
        PriorityTestData(input='v', output=22),
        PriorityTestData(input='t', output=20),
        PriorityTestData(input='s', output=19),
    ]

    def test_priority(self):
        for i in self.data:
            assert priority(i.input) == i.output


@dataclass
class SplitTestData:
    input: str
    output: Tuple[str, str]

class TestSplit:
    data = [
        SplitTestData(input="vJrwpWtwJgWrhcsFMMfFFhFp", output=("vJrwpWtwJgWr", "hcsFMMfFFhFp",)),
        SplitTestData(input="jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", output=("jqHRNqRjqzjGDLGL", "rsFMfFZSrLrFZsSL")),
        SplitTestData(input="PmmdzqPrVvPwwTWBwg", output=("PmmdzqPrV", "vPwwTWBwg",)),
    ]

    def test_split(self):
        for i in self.data:
            assert split(i.input) == i.output


@dataclass
class OverlapTestData:
    input: Tuple[str, ...]
    output: str


class TestOverWrapper:
    data = [
        OverlapTestData(input=("vJrwpWtwJgWr", "hcsFMMfFFhFp",), output="p"),
        OverlapTestData(input=("jqHRNqRjqzjGDLGL", "rsFMfFZSrLrFZsSL"), output="L"),
        OverlapTestData(input=("PmmdzqPrV", "vPwwTWBwg",), output="P"),
        OverlapTestData(
            input=("vJrwpWtwJgWrhcsFMMfFFhFp", "jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL", "PmmdzqPrVvPwwTWBwg"),
            output="r"
        ),
        OverlapTestData(
            input=("wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn", "ttgJtRGJQctTZtZT", "CrZsJsPPZsGzwwsLwLmpwMDw"),
            output="Z"
        ),
    ]

    def test_overlap_wrapper(self):
        for i in self.data:
            assert overlap_wrapper(*i.input) == i.output
