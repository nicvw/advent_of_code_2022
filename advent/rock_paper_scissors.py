#
# On the second day of xmas...
# https://adventofcode.com/2022/day/2
#

from typing import Iterator, Tuple

from .utils import iterate_over_data

PLAYER_ONE_MAP = {
    'A': 1, # rock
    'B': 2, # paper
    'C': 3  # scissors
}

PLAYER_TWO_MAP = {
    'X': 1, # rock
    'Y': 2, # paper
    'Z': 3  # scissors
}

Round = Tuple[str, str]

def rounds_from_datafile() -> Iterator[Round]:
    """Convert lines of data into a Tuple"""
    for line in iterate_over_data('rock_paper_scissors.txt'):
        p1, p2 = line.split()[:2]
        yield p1, p2

def tally_scores(rounds: Iterator[Round]) -> Tuple[int, int]:
    p1_score = 0
    p2_score = 0
    for p1, p2 in rounds:
        p1_score += PLAYER_ONE_MAP[p1]
        p2_score += PLAYER_TWO_MAP[p2]
        if PLAYER_ONE_MAP[p1] == PLAYER_TWO_MAP[p2]:
            p1_score += 3
            p2_score += 3
            continue
        elif PLAYER_ONE_MAP[p1] % 3 == (PLAYER_TWO_MAP[p2] + 1) % 3:
            p1_score += 6
            continue
        else:
            p2_score += 6
            continue

    return p1_score, p2_score


def convert_round(p1: str, p2: str) -> Round:
    """Convert the second players action in a round

    The second column says how the round needs to end:
        X means you need to lose,
        Y means you need to end the round in a draw,
        Z means you need to win. Good luck!"
    """
    p2_plays = ('X', 'Y', 'Z',)

    p1_int = PLAYER_ONE_MAP[p1]
    if p2 == 'X':
        # X means you need to lose
        return p1, p2_plays[(p1_int + 1) % 3]
    elif p2 == 'Y':
        # Y means you need to end the round in a draw
        return p1, p2_plays[p1_int - 1]
    else:
        # Z means you need to win
        return p1, p2_plays[p1_int % 3]


def convert_game(rounds: Iterator[Round]) -> Iterator[Round]:
    """Wrapper for converting all the rounds in a game
    """
    for p1, p2 in rounds:
        yield convert_round(p1, p2)
