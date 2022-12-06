#
# twas the sixth day of xmas...
# https://adventofcode.com/2022/day/6
#

from dataclasses import dataclass, field
from typing import List, TextIO

Buffer = List[str]

@dataclass
class SignalDecoder:
    stream: TextIO
    message: str = ""
    buffer: Buffer = field(default_factory=list)
    start_of_packet: int = 0
    start_of_message: int = 0

    def process_data(self):
        """Read datastream and extract the message
        """
        index = 0
        for char in self.stream.read():
            if self.start_of_message:
                self.message += char
                continue

            index += 1
            self.buffer.append(char)
            if len(self.buffer) < 4:
                continue

            if self.start_of_packet == 0:
                if len(set(self.buffer[-4:])) == 4:
                    self.start_of_packet = index
                continue

            if self.start_of_message == 0:
                if len(set(self.buffer[-14:])) == 14:
                    self.start_of_message = index
                continue
