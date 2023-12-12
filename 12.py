import re
from pathlib import Path


def parse_input(input: list[str]):
    """Parse a line of the input."""
    to_return = []
    for line in input:
        pattern, rest = line.split()
        to_return.append((pattern, [int(number) for number in rest.strip().split(",")]))
    return to_return


def unfold(parsed: list[tuple[str, list[int]]]) -> list[tuple[str, list[int]]]:
    """Unfold the input five times."""
    return [("?".join([pattern] * 5), numbers * 5) for pattern, numbers in parsed]


def smart(pattern, numbers, index=0, group=0, seen=0, cache=None):
    """Recursion with memoization.

    The solution depends on three arguments:
    - index: the index of the character in the pattern we are currently looking at
    - group: the index of the group of numbers we are currently looking at
    - seen: the number of numbers we have already seen in the current group

    If the index is equal or greater than the length of the pattern, check if all
    groups have been processed.

    The current character can be:
    - a dot:
      * if seen is zero: same as possibilities for increased index.
      * if seen is equal to the number in the current group: same as possibilities for
        increased index, increased group and seen set to zero.
    - a hash:
      * if group index is too large: 0 possibilities
      * if seen is equal or greater to the number in the current group: 0 possibilities
      * if seen is lees than the number in the current group: same as possibilities
        with increased index and seen
    If we encounter a "?" we must check both options and sum them together.
    """
    if (already_computed := cache.get((index, group, seen))) is not None:
        return already_computed

    if index == len(pattern):
        return (
            group == len(numbers)
            or group == len(numbers) - 1
            and seen == numbers[group]
        )

    char = pattern[index]
    possibilities = 0
    if char in ".?":
        if seen == 0:
            possibilities += smart(pattern, numbers, index + 1, group, seen, cache)
        elif seen == numbers[group]:
            possibilities += smart(pattern, numbers, index + 1, group + 1, 0, cache)
    if char in "#?":
        if group < len(numbers) and seen < numbers[group]:
            possibilities += smart(pattern, numbers, index + 1, group, seen + 1, cache)
    cache[(index, group, seen)] = possibilities
    return possibilities


input = Path("12.in").read_text().splitlines()
# input = Path("12.ex").read_text().splitlines()

parsed = parse_input(input)
unfolded = unfold(parsed)
# unfolded = parsed

s = 0
for pattern, numbers in unfolded:
    s += smart(pattern, numbers, cache=dict())
print(s)
