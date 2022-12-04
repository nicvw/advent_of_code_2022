from dataclasses import dataclass

from advent.camp_cleanup import assignment_to_range


@dataclass
class AssignmentToRangeData:
    input: str
    output: range


class TestAssignmentToRange:
    data = [
        AssignmentToRangeData(input="1-3", output=range(1, 4)),
        AssignmentToRangeData(input="5-7", output=range(5, 8)),
        AssignmentToRangeData(input="11-17", output=range(11, 18)),
        AssignmentToRangeData(input="2-4", output=range(2, 5)),
    ]

    def test_assignment_to_range(self):
        for t in self.data:
            assert assignment_to_range(t.input) == t.output


@dataclass
class RangeOverlapData:
    range1: range
    range2: range
    output: bool


class TestRangeOverlap:
    data = [
        RangeOverlapData(range1=range(2, 5), range2=range(2, 5), output=True),
        RangeOverlapData(range1=range(1, 4), range2=range(2, 4), output=True),
        RangeOverlapData(range1=range(1, 4), range2=range(1, 3), output=True),
        RangeOverlapData(range1=range(3, 9), range2=range(4, 10), output=False),
        RangeOverlapData(range1=range(3, 9), range2=range(2, 6), output=False),
    ]