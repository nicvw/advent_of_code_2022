#
# twas the seventh day of xmas...
#

from collections import defaultdict
from dataclasses import dataclass, field
from operator import itemgetter
import os
from typing import DefaultDict, Iterable, List, Tuple


@dataclass
class Storage:
    terminal: Iterable[str]
    directories: DefaultDict[str, int] = field(default_factory=lambda: defaultdict(int))
    breadcrumb: List[str] = field(default_factory=list)
    total_capacity: int = 70000000

    def __post_init__(self):
        for line in self.terminal:
            self._parse_line(line)

    def _parse_line(self, line: str):
        if line.startswith("$"):
            _, cmd, *args = line.split()
            if cmd == "cd":
                self._cd(args[0])
        elif line.startswith("dir"):
            pass
        else:
            size, name = line.split()
            self._process_file(name, int(size))

    def _cd(self, arg: str):
        match arg:
            case "/":
                self.breadcrumb = ["/"]
            case "..":
                self.breadcrumb = self.breadcrumb[:-1]
            case _:
                self.breadcrumb.append(os.path.join(self.breadcrumb[-1], arg))

    def _process_file(self, filename: str, size: int):
        for directory in self.breadcrumb:
            self.directories[directory] += size

    def freeup_space(self, space_required: int) -> Tuple[str, int]:
        currently_available = self.total_capacity - self.directories["/"]
        minimum_to_delete = space_required - currently_available
        candidates = [(k, v) for k, v in self.directories.items() if v >= minimum_to_delete]
        return sorted(candidates, key=itemgetter(1))[0]
