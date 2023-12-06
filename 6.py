import re
from functools import reduce
from operator import mul
from pathlib import Path
import math

Time = int
Distance = int


def parse_game1(game: list[str]) -> list[tuple[Time, Distance]]:
    """Parse the game string."""
    mt = re.match(r"Time: *(?P<times>[\d ]*)", game[0])
    md = re.match(r"Distance: *(?P<distances>[\d ]*)", game[1])
    assert mt is not None and md is not None
    times = list(map(int, re.findall("(\d+)", mt["times"])))
    distances = list(map(int, re.findall("(\d+)", md["distances"])))
    return list(zip(times, distances))


def parse_game2(game: list[str]) -> list[tuple[Time, Distance]]:
    """Parse the game string."""
    mt = re.match(r"Time: *(?P<times>[\d ]*)", game[0])
    md = re.match(r"Distance: *(?P<distances>[\d ]*)", game[1])
    assert mt is not None and md is not None
    times = "".join(re.findall("(\d+)", mt["times"]))
    distances = "".join(re.findall("(\d+)", md["distances"]))
    return [(int(times), int(distances))]


lines = Path("6.in").read_text().splitlines()
lines = Path("6.ex").read_text().splitlines()


def winnings(time: int, min_distance: int) -> int:
    """How many timo one can win.

    You have to solve a quadratic equation:
      s**2 - time*s + min_distance = 0

    The solution is the number of integers strictly between the two roots,
    roots must be excluded.
    """
    d = time**2 - 4 * min_distance
    if d <= 0:
        return 0
    dr = math.sqrt(d)
    to_add = -1 if dr == int(dr) else 1
    return int(int((time + dr) / 2) - (time - dr) / 2) + to_add


print(reduce(mul, [winnings(*game) for game in parse_game1(lines)], 1))
print(reduce(mul, [winnings(*game) for game in parse_game2(lines)], 1))
