from dataclasses import dataclass, field
from typing import List

from advent.rope import Motion, Rope, Knot
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


class TestKnot:
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
            head = Knot(*t.head)
            tail = Knot(*t.tail)
            assert head.adjacent(tail) == t.adjacent
    
    def test_equality(self):
        assert Knot(1, 2) == Knot(1, 2)
        assert Knot(1, 2) != Knot(2, 3)
        pt = Knot(1, 1)
        pt.move(0, 1)
        assert pt == Knot(1, 2)


@dataclass
class OrchestratorTest:
    moves: List[Motion]
    history: int
    knots: int = field(default=2)
    rope: Rope = field(init=False)

    def __post_init__(self):
        self.rope = Rope(self.moves, [Knot() for _ in range(self.knots)])
    

class TestOrchestrator:
    tests = [
        OrchestratorTest(
            moves=[('R', 1), ('R', 1)],
            history=2
        ),
        OrchestratorTest(
            moves=[('L', 1), ('L', 1)],
            history=2
        ),
        OrchestratorTest(
            moves=[('U', 1), ('U', 1)],
            history=2
        ),
        OrchestratorTest(
            moves=[('D', 1), ('D', 1)],
            history=2
        ),
        OrchestratorTest(
            moves=[('R', 1), ('U', 2)],
            history=2
        ),
        OrchestratorTest(
            moves=[('L', 1), ('U', 2)],
            history=2
        ),
        OrchestratorTest(
            moves=[('R', 1), ('D', 2)],
            history=2
        ),
        OrchestratorTest(
            moves=[('L', 1), ('D', 2)],
            history=2
        ),
        OrchestratorTest(
            moves=[('U', 1), ('R', 2)],
            history=2
        ),
        OrchestratorTest(
            moves=[('U', 1), ('L', 2)],
            history=2
        ),
        OrchestratorTest(
            moves=[('D', 1), ('R', 2)],
            history=2
        ),
        OrchestratorTest(
            moves=[('D', 1), ('L', 2)],
            history=2
        ),
        OrchestratorTest(
            moves=[('R', 4), ('U', 4), ('L', 3), ('D', 1), ('R', 4), ('D', 1), ('L', 5), ('R', 2)],
            history=13
        ),
        OrchestratorTest(
            moves=[("R", 9)],
            knots=5,
            history=6
        ),
        OrchestratorTest(
            moves=[("R", 20), ("L", 10)],
            knots=5,
            history=17
        ),
        OrchestratorTest(
            moves=[("R", 10), ("U", 5)],
            knots=5,
            history=12
        ),
        # OrchestratorTest(
        #     moves=[("R", 5), ("U", 8), ("L", 8), ("D", 3), ("R", 17), ("D", 10), ("L", 25), ("U", 20)],
        #     knots=9,
        #     history=36
        # )

    ]

    def test_orchestrator(self):
        for t in self.tests:
            t.rope()
            assert len(set(t.rope.knots[-1].history)) == t.history
