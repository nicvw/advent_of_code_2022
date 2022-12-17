"""Utility functions"""

from pathlib import Path
from typing import Iterator


def iterate_over_data(path: str) -> Iterator[str]:
    datafile = Path('.').absolute().joinpath(f'data/{path}')
    with datafile.open() as fhl:
        for line in fhl.readlines():
            yield line.strip()
