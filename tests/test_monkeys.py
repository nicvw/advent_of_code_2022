from pathlib import Path
from typing import Dict

import pytest
import yaml

from advent.monkeys import Monkey, MonkeyMaker, Monkeys

@pytest.fixture
def monkey_dict() -> Dict[str, str]:
    return {
    "Starting items": "79, 98",
    "Operation": "new = old * 19",
    "Test": "divisible by 23",
    "If true": "throw to monkey 2",
    "If false": "throw to monkey 3"
    }

@pytest.fixture
def monkey_maker(monkey_dict: Dict[str, str]) -> MonkeyMaker:
    return MonkeyMaker(**monkey_dict)

@pytest.fixture
def monkey(monkey_maker: MonkeyMaker) -> Monkey:
    return monkey_maker.create(3)

def test_monkey_maker_init(monkey_maker: MonkeyMaker):
    assert monkey_maker.items == "79, 98"
    assert monkey_maker.operation == "new = old * 19"
    assert monkey_maker.test == "divisible by 23"
    assert monkey_maker.true == "throw to monkey 2"
    assert monkey_maker.false == "throw to monkey 3"

def test_monkey_maker(monkey: Monkey):
    assert monkey.items == [79, 98]
    assert monkey.operation(10) == 190
    assert monkey.test == 23
    assert monkey.true == 2
    assert monkey.false == 3

def test_monkey_turn(monkey: Monkey):
    throws = monkey.turn(7742)
    assert throws == [
        (3, 8242),
        (3, 8362)
    ]

@pytest.fixture
def monkeys_data():
    with Path('data/monkeys_demo1.txt').open() as fhl:
        return yaml.safe_load(fhl)

def test_monkeys(monkeys_data: Dict[str, Dict[str, str]]):
    monkeys = Monkeys(makers=monkeys_data, relief=3)
    assert len(monkeys.monkeys) == 4
