import re
from functools import reduce
from operator import mul
from pathlib import Path


def all_numbers(lines: list[str]) -> list[tuple[int, tuple[int, int]]]:
    """Return all numbers in the lines and their position."""
    return [
        (int(match.group(0)), divmod(match.start(), len(lines[0])))
        for match in re.finditer(r"\d+", "".join(lines))
    ]


def all_stars(lines: list[str]) -> list[tuple[int, int]]:
    """Return the position of all start."""
    return [
        divmod(match.start(), len(lines[0]))
        for match in re.finditer(r"\*", "".join(lines))
    ]


def is_part_number(number: int, x: int, y: int, lines: list[str]) -> bool:
    """Check if the number is the part number."""
    number_length = len(str(number))
    x_start = x - 1
    x_end = x + number_length + 1
    return any(
        (
            re.search(r"[^.\d]", lines[y - 1][x_start:x_end]),
            re.search(r"[^.\d]", lines[y + 1][x_start:x_end]),
            re.search(r"[^.\d]", lines[y][x_start : x_start + 1]),
            re.search(r"[^.\d]", lines[y][x_end - 1 : x_end]),
        )
    )


def get_ratio(x: int, y: int, numbers: list[tuple[int, tuple[int, int]]]) -> int:
    """Get the ration of the gear (or 0 if star is not a gear)."""
    gear_numbers: list[int] = []
    for number, (number_y, number_x) in numbers:
        x_start = number_x - 1
        x_end = number_x + len(str(number))
        if x_start <= x <= x_end and number_y - 1 <= y <= number_y + 1:
            gear_numbers.append(number)
    return reduce(mul, gear_numbers, 1) if len(gear_numbers) == 2 else 0


lines = Path("3.in").read_text().splitlines()
# lines = """467..114..
# ...*......
# ..35..633.
# ......#...
# 617*......
# .....+.58.
# ..592.....
# ......755.
# ...$.*....
# .664.598..""".split(
#     "\n"
# )

line_length = len(lines[0])
dot_line = ["." * line_length]
lines = dot_line + lines + dot_line
lines = list(map(lambda line: "." + line + ".", lines))
numbers = all_numbers(lines)
print(sum(number for number, (y, x) in numbers if is_part_number(number, x, y, lines)))
print(sum(get_ratio(x, y, numbers) for y, x in all_stars(lines)))
