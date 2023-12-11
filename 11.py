import re
from pathlib import Path
from itertools import combinations


PROBLEM = 2


def expand_input(
    lines: list[str], expansion_factor=1000000
) -> list[list[tuple[int, int]]]:
    """Expand the input by a factor of expansion_factor."""
    expanded = [[(1, 1) if c == "." else (0, 0) for c in line] for line in lines]
    for row in (e for e, line in enumerate(lines) if all(c == "." for c in line)):
        for column in range(len(lines[0])):
            expanded[row][column] = (1, expansion_factor)
    for column in (
        column
        for column in range(len(lines[0]))
        if all(line[column] == "." for line in lines)
    ):
        for line in expanded:
            line[column] = (expansion_factor, 1)
    return expanded


def extract_galaxies(input: list[str]) -> list[tuple[int, int]]:
    """Extract the coordinates of all galaxies from the input."""
    return [
        (x, y) for y, line in enumerate(input) for x, c in enumerate(line) if c == "#"
    ]


def path_length(path_from, path_to, expanded):
    """Length of the path between two galaxies."""
    length = 0
    x1, y1 = path_from
    x2, y2 = path_to
    while x1 != x2:
        length += expanded[y1][x1][0]
        x1 += 1 if x1 < x2 else -1
    while y1 != y2:
        length += expanded[y1][x1][1]
        y1 += 1 if y1 < y2 else -1
    return length


if PROBLEM == 1:
    expansion_factor = 2
else:
    expansion_factor = 1000000

# input = Path("11.ex").read_text().splitlines()
input = Path("11.in").read_text().splitlines()
galaxies = extract_galaxies(input)
expanded = expand_input(input, expansion_factor)

print(
    sum(
        path_length(*combination, expanded) for combination in combinations(galaxies, 2)
    )
)
