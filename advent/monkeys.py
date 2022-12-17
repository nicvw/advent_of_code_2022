from dataclasses import dataclass, field
from math import lcm
import re
from rich import print
from pydantic import BaseModel, Field
from typing import Callable, Dict, List, Tuple
import yaml

Operation = Callable[[int], int]
MonkeyID = int
Item = int
Throw = Tuple[MonkeyID, Item]


@dataclass
class Monkey:
    items: List[int]
    operation: Operation
    test: int
    true: int
    false: int
    relief: int = field(default=3)
    operations: int = field(init=False, default=0)

    def turn(self, common: int) -> List[Throw]:
        throws: List[Throw] = []
        for item in self.items:
            self.operations += 1
            worry = int(self.operation(item) / self.relief)
            throws.append((self.true if worry % self.test == 0 else self.false, common + worry % common))
        self.items = []
        return throws

class MonkeyMaker(BaseModel):
    items: str = Field(alias="Starting items")
    operation: str = Field(alias="Operation")
    test: str = Field(alias="Test")
    true: str = Field(alias="If true", )
    false: str = Field(alias="If false")

    def create(self, relief: int) -> Monkey:
        return Monkey(
            items=self._items,
            operation=self._operation,
            test=self._test,
            true=self._true,
            false=self._false,
            relief=relief
        )

    @property
    def _items(self):
        return [int(x) for x in self.items.split(", ")]

    @property
    def _operation(self):
        match = re.search(r'^new = (?P<eval>.*)', self.operation)
        if match is not None:
            operation: Operation = lambda old: eval(match.groupdict()['eval'])
            return operation
        raise Exception

    @property
    def _test(self) -> int:
        # divisible by 13
        match = re.search(r'(?:divisible by )(\d+)', self.test)
        if match:
            return int(match.groups()[0])
        raise Exception

    def _bool(self, action: str) -> int:
        match = re.search(r'(?:throw to monkey )(\d+)', action)
        if match:
            return int(match.groups()[0])
        raise Exception

    @property
    def _true(self):
        return self._bool(self.true)

    @property
    def _false(self):
        return self._bool(self.false)


@dataclass
class Monkeys:
    makers: Dict[str, Dict[str, str]]
    relief: int
    monkeys: List[Monkey] = field(default_factory=list)
    lcm: int = field(init=False)

    def __post_init__(self) -> None:
        for i in range(len(self.makers)):
            maker = MonkeyMaker(**self.makers[f"Monkey {i}"])
            self.monkeys.append(maker.create(self.relief))
        self.lcm = lcm(*[m.test for m in self.monkeys])

    def round(self):
        for monkey in self.monkeys:
            items = monkey.turn(self.lcm)
            for item in items:
                self.monkeys[item[0]].items.append(item[1])

    def play_rounds(self, rounds: int):
        for _ in range(rounds):
            self.round()
            # self._state

    @property
    def scores(self) -> Dict[str, int]:
        return {f"Monkey {i}": m.operations for i, m in enumerate(self.monkeys)}

    @property
    def _state(self):
        for i, m in enumerate(self.monkeys):
            print(f"Monkey {i}: {m.items}")

def monkey_loader(textdata: str):
    return yaml.safe_load(textdata)
