import array
import re
from pathlib import Path

from collections import defaultdict

RangeStart = int
RangeEnd = int
Difference = int
RangeMap = tuple[RangeStart, RangeEnd, Difference]
RangeMaps = list[RangeMap]
SeedRange = tuple[RangeStart, RangeEnd]
SeedRanges = list[SeedRange]


def parse_game(lines: list[str]) -> tuple[SeedRanges, list[RangeMaps]]:
    """Parse the game strings."""
    m = re.match(r"seeds: (?P<seeds>.*)", lines[0])
    assert m is not None
    seeds = list(map(int, m["seeds"].strip().split()))
    seed_ranges = [
        (seeds[i], seeds[i + 1] + seeds[i] - 1) for i in range(0, len(seeds), 2)
    ]
    mappings: list[RangeMaps] = []
    current_mapping: RangeMaps = []

    for line in lines[3:]:
        if re.search(r"(?P<map_name>[\w-]+) map:", line):
            mappings.append(current_mapping)
            current_mapping = []
        elif line:
            destination, source, length = map(int, line.split())
            current_mapping.append((source, source + length - 1, destination - source))
    mappings.append(current_mapping)
    return seed_ranges, mappings


def map_intersection(range: SeedRange, map: RangeMap) -> tuple[SeedRanges, SeedRanges]:
    """Map the intersection of the range."""
    mapped: SeedRanges = []
    remaining = [range]
    if (start := max(range[0], map[0])) <= (end := min(range[1], map[1])):
        remaining = []
        if range[0] < start:
            remaining.append((range[0], start - 1))
        mapped.append((start + map[2], end + map[2]))
        if end < range[1]:
            remaining.append((end + 1, range[1]))
    return remaining, mapped


lines = Path("5.in").read_text().splitlines()
# lines = """seeds: 79 14 55 13

# seed-to-soil map:
# 50 98 2
# 52 50 48

# soil-to-fertilizer map:
# 0 15 37
# 37 52 2
# 39 0 15

# fertilizer-to-water map:
# 49 53 8
# 0 11 42
# 42 0 7
# 57 7 4

# water-to-light map:
# 88 18 7
# 18 25 70

# light-to-temperature map:
# 45 77 23
# 81 45 19
# 68 64 13

# temperature-to-humidity map:
# 0 69 1
# 1 0 69

# humidity-to-location map:
# 60 56 37
# 56 93 4""".split(
#     "\n"
# )

ranges, mappings_list = parse_game(lines)
for maps in mappings_list:
    new_ranges = []
    while ranges:
        current_range = ranges.pop()
        for current_map in maps:
            remaining, mapped = map_intersection(current_range, current_map)
            if mapped:
                new_ranges += mapped
                ranges += remaining
                break
        else:
            new_ranges.append(current_range)
    ranges = new_ranges

print(min(min(ranges)))
