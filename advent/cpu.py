from dataclasses import dataclass, field
from typing import List, Literal, TextIO, Tuple

InstructionAction = Literal['addx', 'noop']
Instruction = Tuple[InstructionAction, int]
InstructionSet = List[Instruction]
Sprite = Tuple[int, int, int]


@dataclass
class CRT:
    cycle = 0
    eol = 39

    def tick(self, sprite: Sprite):
        if self.cycle in sprite:
            print("#", end="")
        else:
            print(".", end="")

        if self.cycle == self.eol:
            self.cycle = 0
            print("")
        else:
            self.cycle += 1

@dataclass
class CPU:
    instructions: InstructionSet
    cycles: int = field(default=0)
    x_register: int = field(default=1)
    signal_cycle: int = field(default=20)
    signal_strength: List[int] = field(default_factory=list)
    screen: CRT = field(default_factory=CRT)

    def _tick(self, cycles: int):
        for _ in range(cycles):
            self.cycles += 1
            self.screen.tick(self._sprite())
            if self.cycles == self.signal_cycle:
                self._signal_strength()

    def _signal_strength(self):
        self.signal_strength.append(self.x_register * self.signal_cycle)
        self.signal_cycle += 40

    def _noop(self):
        self._tick(1)

    def _addx(self, value: int):
        self._tick(2)
        self.x_register += value

    def _sprite(self):
        return (self.x_register - 1, self.x_register, self.x_register + 1)

    def __call__(self):
        for instruction in self.instructions:
            if instruction[0] == 'noop':
                self._noop()
            if instruction[0] == 'addx':
                self._addx(instruction[1])

def load_instructions(data: TextIO) -> InstructionSet:
    instructions: InstructionSet = []
    for row in data:
        instruction, *value = row.split()
        if instruction == 'addx':
            instructions.append((instruction, int(value[0])))
        if instruction == 'noop':
            instructions.append((instruction, 0))
    return instructions