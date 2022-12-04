from advent.utils import iterate_over_data

def range_includes(range1: range, range2: range) -> bool:
    """Whether range1 contains range2"""
    x1, x2 = range1.start, range1.stop
    y1, y2 = range2.start, range2.stop
    return x1 <= y1 and y2 <= x2

def assignment_to_range(assignment: str) -> range:
    """Convert a section assignment to a range"""
    start, stop = assignment.split("-")
    return range(int(start), int(stop) + 1)

def overlapping_pairs() -> int:
    overlaps = 0
    for pair in iterate_over_data("camp_cleanup.txt"):
        range1, range2 = [assignment_to_range(x) for x in pair.split(",")]
        if range_includes(range1, range2) or range_includes(range2, range1):
            overlaps += 1
    return overlaps