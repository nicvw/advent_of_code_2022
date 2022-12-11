from dataclasses import dataclass, field
from typing import List, Set

from advent.rope import Motion, Orchestrator, PositionTracker
from advent.trees import Coordinate


grid = [
    [(-1, 2),  (0, 2),  (1, 0),  (2, 2),  (3, 2)],
    [(-1, 1),  (0, 1),  (1, 1),  (2, 1),  (3, 1)],
    [(-1, 0),  (0, 0),  (1, 0),  (2, 0),  (3, 0)],
    [(-1, -1), (0, -1), (1, -1), (2, -1), (3, -1)],
    [(-1, -2), (0, -2), (1, -2), (2, -2), (3, -2)],
]

@dataclass
class RelativePositionTest:
    head: Coordinate
    tail: Coordinate
    aligned: bool
    adjacent: bool


class TestPositionTracker:
    positional_tests = [
        RelativePositionTest(head=(0, 0), tail=(0, 0), aligned=True, adjacent=False),
        RelativePositionTest(head=(1, 0), tail=(1, 1), aligned=True, adjacent=True),
        RelativePositionTest(head=(1, 0), tail=(1, -1), aligned=True, adjacent=True),
        RelativePositionTest(head=(1, 0), tail=(0, 0), aligned=True, adjacent=True),
        RelativePositionTest(head=(1, 0), tail=(2, 0), aligned=True, adjacent=True),
        RelativePositionTest(head=(1, 0), tail=(0, 1), aligned=False, adjacent=True),
        RelativePositionTest(head=(1, 0), tail=(2, 1), aligned=False, adjacent=True),
        RelativePositionTest(head=(1, 0), tail=(0, -1), aligned=False, adjacent=True),
        RelativePositionTest(head=(1, 0), tail=(2, -1), aligned=False, adjacent=True),
        RelativePositionTest(head=(1, 0), tail=(-1, 2), aligned=False, adjacent=False),
        RelativePositionTest(head=(1, 0), tail=(3, 2), aligned=False, adjacent=False),
        RelativePositionTest(head=(1, 0), tail=(-2, -1), aligned=False, adjacent=False),
        RelativePositionTest(head=(1, 0), tail=(3, -2), aligned=False, adjacent=False),
    ]

    def test_position(self):
        for t in self.positional_tests:
            head = PositionTracker(*t.head)
            tail = PositionTracker(*t.tail)
            assert head.aligned(tail) == t.aligned
            assert head.adjacent(tail) == t.adjacent
    
    def test_equality(self):
        assert PositionTracker(1, 2) == PositionTracker(1, 2)
        assert PositionTracker(1, 2) != PositionTracker(2, 3)
        pt = PositionTracker(1, 1)
        pt.move(0, 1)
        assert pt == PositionTracker(1, 2)


@dataclass
class OrchestratorTest:
    moves: List[Motion]
    history: Set[Coordinate]
    history_length: int
    head: PositionTracker = field(default_factory=PositionTracker)
    tail: PositionTracker = field(default_factory=PositionTracker)
    orchestrator: Orchestrator = field(init=False)

    def __post_init__(self):
        self.orchestrator = Orchestrator(self.moves, self.head, self.tail)
    

class TestOrchestrator:
    tests = [
        OrchestratorTest(
            moves=[('R', 1), ('R', 1)],
            history={(0, 0), (1, 0)},
            history_length=2),
        OrchestratorTest(
            moves=[('L', 1), ('L', 1)],
            history={(0, 0), (-1, 0)},
            history_length=2),
        OrchestratorTest(
            moves=[('U', 1), ('U', 1)],
            history={(0, 0), (0, 1)},
            history_length=2),
        OrchestratorTest(
            moves=[('D', 1), ('D', 1)],
            history={(0, 0), (0, -1)},
            history_length=2),
        OrchestratorTest(
            moves=[('R', 1), ('U', 2)],
            history={(0, 0), (1, 1)},
            history_length=2),
        OrchestratorTest(
            moves=[('L', 1), ('U', 2)],
            history={(0, 0), (-1, 1)},
            history_length=2),
        OrchestratorTest(
            moves=[('R', 1), ('D', 2)],
            history={(0, 0), (1, -1)},
            history_length=2),
        OrchestratorTest(
            moves=[('L', 1), ('D', 2)],
            history={(0, 0), (-1, -1)},
            history_length=2),
        OrchestratorTest(
            moves=[('U', 1), ('R', 2)],
            history={(0, 0), (1, 1)},
            history_length=2),
        OrchestratorTest(
            moves=[('U', 1), ('L', 2)],
            history={(0, 0), (-1, 1)},
            history_length=2),
        OrchestratorTest(
            moves=[('D', 1), ('R', 2)],
            history={(0, 0), (1, -1)},
            history_length=2),
        OrchestratorTest(
            moves=[('D', 1), ('L', 2)],
            history={(0, 0), (-1, -1)},
            history_length=2),
        OrchestratorTest(
            moves=[('R', 4), ('U', 4), ('L', 3), ('D', 1), ('R', 4), ('D', 1), ('L', 5), ('R', 2)],
            history={(0, 0), (1, 0), (2, 0), (3, 0), (4, 1), (4, 2), (3, 2), (2, 2), (1, 2), (3, 3), (4, 3), (2, 4), (3, 4)},
            history_length=13),
    ]

    def test_orchestrator(self):
        for t in self.tests:
            t.orchestrator()
            assert t.tail.history == t.history
            assert len(t.tail.history) == t.history_length
