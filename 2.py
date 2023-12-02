import re
from collections import defaultdict
from functools import reduce
from operator import mul
from pathlib import Path
from typing import Literal, get_args

Color = Literal["red", "green", "blue"]
AllColors = get_args(Color)
GameNumber = int


def parse_game(
    game: str,
) -> tuple[GameNumber, list[dict[Color, int]]]:
    """Parse the game string."""
    m = re.match(r"Game (?P<game_number>\d+): (?P<data>.*)", game)
    assert m is not None
    grabs: list[dict[Color, int]] = []
    for grab in m["data"].split(";"):
        grab_data: dict[Color, int] = defaultdict(int)
        for color_num in grab.split(","):
            num, color = color_num.strip().split(" ")
            assert color in AllColors
            grab_data[color] = int(num)
        grabs.append(grab_data)
    return int(m["game_number"]), grabs
    # return int(m["game_number"]), list(
    #     dict(reversed(g.strip().split(" ")) for g in game.split(","))
    #     for game in m["data"].split(";")
    # )


def is_possible(
    game_data: list[dict[Color, int]], max_available: dict[Color, int]
) -> bool:
    """Check if the game is passible."""
    return all(
        data[color] <= max_available[color] for data in game_data for color in AllColors
    )


def power(game_data: list[dict[Color, int]]) -> int:
    """Calculate the power of the game."""
    min_cubes: dict[Color, int] = defaultdict(int)
    for data in game_data:
        for color in AllColors:
            min_cubes[color] = max(min_cubes[color], data[color])
    return reduce(mul, min_cubes.values(), 1)


lines = Path("2.in").read_text().splitlines()
parsed = [parse_game(line) for line in lines]
print(
    "1:",
    sum(
        game_number
        for game_number, game_data in parsed
        if is_possible(game_data, {"red": 12, "green": 13, "blue": 14})
    ),
)
print("2:", sum(power(game_data) for _, game_data in parsed))
