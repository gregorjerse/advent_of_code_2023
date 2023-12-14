from pathlib import Path
from functools import reduce


def parse_input(input: str) -> list[str]:
    """Parse input."""
    return input.splitlines()


def move_north(lines):
    """Move to the north."""
    for y in range(len(lines)):
        for x in range(len(lines[0])):
            if lines[y][x] == "O":
                counter = y
                while counter >= 1 and lines[counter - 1][x] == ".":
                    lines[counter - 1][x] = "O"
                    lines[counter][x] = "."
                    counter -= 1
    return lines


def move_south(lines):
    """Move to the south."""
    for y in range(len(lines) - 1, -1, -1):
        for x in range(len(lines[0])):
            if lines[y][x] == "O":
                counter = y
                while counter < len(lines) - 1 and lines[counter + 1][x] == ".":
                    lines[counter + 1][x] = "O"
                    lines[counter][x] = "."
                    counter += 1
    return lines


def move_west(lines):
    """Move to the west."""
    for x in range(len(lines[0])):
        for y in range(len(lines)):
            if lines[y][x] == "O":
                counter = x
                while counter >= 1 and lines[y][counter - 1] == ".":
                    lines[y][counter - 1] = "O"
                    lines[y][counter] = "."
                    counter -= 1
    return lines


def move_east(lines):
    """Move to the east."""
    for x in range(len(lines[0]) - 1, -1, -1):
        for y in range(len(lines)):
            if lines[y][x] == "O":
                counter = x
                while counter < len(lines[0]) - 1 and lines[y][counter + 1] == ".":
                    lines[y][counter + 1] = "O"
                    lines[y][counter] = "."
                    counter += 1
    return lines


def compose_functions(*functions):
    """Compose functions"""

    def compose(f, g):
        """Compose two functions."""
        return lambda x: f(g(x))

    return reduce(compose, functions, lambda x: x)


def cycle(lines):
    """Move one cycle."""
    cycle = compose_functions(move_east, move_south, move_west, move_north)
    return cycle(lines)


def rock_description(lines):
    """Return a description of the rocks.

    A tuple of tuples starting from top-left to bottom-right.
    """
    return tuple(
        (x, len(lines) - y)
        for y in range(len(lines))
        for x in range(len(lines[0]))
        if lines[y][x] == "O"
    )


def weight(rocks):
    """Return the weight on the north beam."""
    return sum(rock[1] for rock in rocks)


text = Path("14.in").read_text()
# text = Path("14.ex").read_text()

input = [list(line) for line in parse_input(text)]

positions = set()
cycles = [rock_description(input)]
while True:
    input = cycle(input)
    rocks = rock_description(input)
    if rocks in positions:
        break
    positions.add(rocks)
    cycles.append(rocks)

first_index = cycles.index(rocks)
period = len(cycles) - first_index
print(weight(cycles[(1000000000 - first_index) % period + first_index]))
