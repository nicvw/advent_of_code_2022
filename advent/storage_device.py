from collections import defaultdict
from dataclasses import dataclass, field
from typing import DefaultDict, Iterable, List


@dataclass
class Storage:
    terminal: Iterable[str]
    directories: DefaultDict[str, int] = field(default_factory=lambda: defaultdict(int))
    breadcrumb: List[str] = field(default_factory=list)

    def __post_init__(self):
        for line in self.terminal:
            self._parse_line(line)

    def _parse_line(self, line: str):
        if line.startswith("$"):
            _, cmd, *args = line.split()
            if cmd == "cd":
                self._cd(args[0])
            else:
                print(f"Skipping '{line}'")
        elif line.startswith("dir"):
            print(f"Skipping '{line}'")
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
                self.breadcrumb.append(arg)

    def _process_file(self, filename: str, size: int):
        for directory in self.breadcrumb:
            self.directories[directory] += size
