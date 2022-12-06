#
# twas the sixth day of xmas...
# https://adventofcode.com/2022/day/6
#

from dataclasses import dataclass
from io import StringIO
from typing import TextIO

from advent.comm_device import SignalDecoder


@dataclass
class SignalDecoderTestData:
    input: TextIO
    start_of_packet: int
    start_of_message: int


class TestSignalDecoder:
    tests = [
        SignalDecoderTestData(input=StringIO("mjqjpqmgbljsphdztnvjfqwrcgsmlb"), start_of_packet=7, start_of_message=19),
        SignalDecoderTestData(input=StringIO("bvwbjplbgvbhsrlpgdmjqwftvncz"), start_of_packet=5, start_of_message=23),
        SignalDecoderTestData(input=StringIO("nppdvjthqldpwncqszvftbrmjlhg"), start_of_packet=6, start_of_message=23),
        SignalDecoderTestData(input=StringIO("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg"), start_of_packet=10, start_of_message=29),
        SignalDecoderTestData(input=StringIO("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw"), start_of_packet=11, start_of_message=26),
    ]

    def test_decoder(self):
        for t in self.tests:
            decoder = SignalDecoder(t.input)
            decoder.process_data()
            assert decoder.start_of_packet == t.start_of_packet
            assert decoder.start_of_message == t.start_of_message
