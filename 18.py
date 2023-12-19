from pathlib import Path
from collections import defaultdict
from heapq import heapify, heappop, heappush
import re

direction = {"R": (1, 0), "D": (0, 1), "L": (-1, 0), "U": (0, -1)}
direction2 = {"0": (1, 0), "1": (0, 1), "2": (-1, 0), "3": (0, -1)}


def parse_input(input: str) -> list[tuple[tuple[int, int], int, str]]:
    """Parse the input."""
    m = re.findall(r"(?P<direction>[RDLU]) (?P<steps>\d+) \((?P<color>#\w+)\)", input)
    return [(m[0], int(m[1]), m[2]) for m in m]


def parse_hexa(input):
    """Parse the color entry and convert it to a direction and a number."""
    return [
        (direction2[color[-1]], int(color[1:-1], 16), color) for _, _, color in input
    ]


def turning_points(input):
    """Get the turning points from the input."""
    position = (0, 0)
    path = defaultdict(set)
    for direction, steps, _ in input:
        position = (
            position[0] + direction[0] * steps,
            position[1] + direction[1] * steps,
        )
        path[position[1]].add(position[0])
    return path


def intersects(s1, e1, s2, e2):
    """Do two intervals intersect (touching at a single point does not count)."""
    return s2 >= s1 and s2 < e1 or s1 >= s2 and s1 < e2


def merge_intervals(intervals):
    """Merge intervals that intersect.

    The procedure is as follows:
    - sort the intervals by the start
    - remove intervals of the form (x, x)
    - if two intervals have a common intersection join them into one.
    """
    intervals.sort()
    i = 0
    while i < len(intervals) - 1:
        if intervals[i][0] == intervals[i][1]:
            del intervals[i]
        elif intervals[i + 1][0] <= intervals[i][1]:
            intervals[i] = (intervals[i][0], max(intervals[i][1], intervals[i + 1][1]))
            del intervals[i + 1]
        else:
            i += 1


def volume(path):
    """Get the volume for the path."""
    intervals = []
    ys = list(sorted(path))
    to_add = 0
    all_together = 0
    for y_position, y in enumerate(ys):
        xes = list(sorted(path[y]))
        # Process all the lines in between two ys.
        if y_position > 0:
            y_before = ys[y_position - 1]
            all_together += (y - y_before - 1) * to_add
        # Process the line of change (current y).
        interval_current = intervals[:]
        # Prepare for the lines between changes (lines between this and the next y).
        for i in range(0, len(xes), 2):
            x1, x2 = xes[i : i + 2]
            interval_current.append((x1, x2))
            intersection_index = -1
            for i, interval in enumerate(intervals):
                if intersects(x1, x2, interval[0], interval[1]):
                    intersection_index = i
                    break
            if intersection_index >= 0:
                s1, e1 = intervals[intersection_index][0], x1
                s2, e2 = x2, intervals[intersection_index][1]
                if s1 != e1:
                    intervals.append((s1, e1))
                if s2 != e2:
                    intervals.append((s2, e2))
                intervals.pop(intersection_index)
            else:
                intervals.append((x1, x2))

        merge_intervals(interval_current)
        all_together += sum(end - start + 1 for start, end in interval_current)
        merge_intervals(intervals)
        to_add = sum(end - start + 1 for start, end in intervals)
    return all_together


text = Path("18.in").read_text()
# text = Path("18.ex").read_text()

input = parse_input(text)
big_input = parse_hexa(input)
big_path = turning_points(big_input)
print(volume(big_path))
