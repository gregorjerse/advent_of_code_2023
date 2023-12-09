import re
from pathlib import Path


def parse_game(lines: list[str]):
    """Parse the game string and return mapping and instructions."""
    return [list(map(int, re.findall(r"[-\d]+", line))) for line in lines]


def difference(sequence: list[int]) -> list[int]:
    """Return the differences between consecutive elements."""
    return [sequence[i + 1] - sequence[i] for i in range(len(sequence) - 1)]


def prediction(sequence: list[int]) -> tuple[int, int]:
    sum_last, sum_first, counter = 0, 0, 0
    while not all(d == 0 for d in sequence):
        sum_last += sequence[-1]
        sum_first += sequence[0] * (-1) ** counter
        counter += 1
        sequence = difference(sequence)
    return sum_first, sum_last


lines = Path("9.in").read_text().splitlines()
# lines = Path("9.ex").read_text().splitlines()


parsed = parse_game(lines)
predictions = [prediction(entry) for entry in parsed]
print(sum(prediction[0] for prediction in predictions))
print(sum(prediction[1] for prediction in predictions))
