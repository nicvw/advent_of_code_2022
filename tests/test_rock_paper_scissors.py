from dataclasses import dataclass
from typing import List, Tuple

from advent.rock_paper_scissors import convert_round, tally_scores


@dataclass
class Game:
    result: Tuple[int, int]
    rounds: List[Tuple[str, str]]


@dataclass
class RoundConvertTestData:
    input: Tuple[str, str]
    output: Tuple[str, str]


class TestScores:
    games = [
        Game(
            result=(1 + 6, 3,),
            rounds=[
                ('A', 'Z',)
            ]
        ),
        Game(
            result=(2 + 6, 1,),
            rounds=[
                ('B', 'X',)
            ]
        ),
        Game(
            result=(3 + 6, 2,),
            rounds=[
                ('C', 'Y',)
            ]
        ),
        Game(
            result=(15, 15,),
            rounds=[
                ('A', 'Y',),
                ('B', 'X',),
                ('C', 'Z',)
            ]
        ),
        Game(
            result=(6 + 18, 6,),
            rounds=[
                ('A', 'Z',),
                ('B', 'X',),
                ('C', 'Y',)
            ]
        ),
        Game(
            result=(28 + 12 * 6, 16,),
            rounds=[
                ('A', 'X',),
                ('B', 'X',),
                ('B', 'X',),
                ('B', 'X',),
                ('B', 'X',),
                ('B', 'X',),
                ('B', 'X',),
                ('B', 'X',),
                ('B', 'X',),
                ('B', 'X',),
                ('B', 'X',),
                ('B', 'X',),
                ('B', 'X',),
            ]
        )

    ]

    def test_scores(self):
        for game in self.games:
            assert tally_scores(iter(game.rounds)) == game.result


class TestConvert:
    # X means you need to lose
    # Y means you need to end the round in a draw
    # Z means you need to win
    rounds = [
        RoundConvertTestData(input=('A', 'X',), output=('A', 'Z',)),
        RoundConvertTestData(input=('A', 'Y',), output=('A', 'X',)),
        RoundConvertTestData(input=('A', 'Z',), output=('A', 'Y',)),
        RoundConvertTestData(input=('B', 'X',), output=('B', 'X',)),
        RoundConvertTestData(input=('B', 'Y',), output=('B', 'Y',)),
        RoundConvertTestData(input=('B', 'Z',), output=('B', 'Z',)),
        RoundConvertTestData(input=('C', 'X',), output=('C', 'Y',)),
        RoundConvertTestData(input=('C', 'Y',), output=('C', 'Z',)),
        RoundConvertTestData(input=('C', 'Z',), output=('C', 'X',)),
    ]

    def test_conversion(self):
        for round in self.rounds:
            assert convert_round(*round.input) == round.output
