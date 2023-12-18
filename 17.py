from pathlib import Path
from collections import defaultdict
from heapq import heapify, heappop, heappush

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

oposite = {UP: DOWN, DOWN: UP, LEFT: RIGHT, RIGHT: LEFT}


def parse_input(input: str) -> list[list[int]]:
    """Parse the input."""
    return [list(map(int, list(line))) for line in input.splitlines()]


text = Path("17.in").read_text()
text = Path("17.ultra").read_text()
text = Path("17.txt").read_text()


def next_directions(direction: tuple[int, int]) -> list[tuple[int, int]]:
    """Return next directions."""
    dx, dy = direction
    return [(-dy, -dx), (dy, dx)]


def path(
    x: int, y: int, direction: tuple[int, int], distance
) -> list[tuple[int, int, int]]:
    """Return the path of the given distance from x,y in the given direction.

    Starting point is not included.
    """
    path = []
    for path_len in range(1, distance + 1):
        path.append(
            (x + direction[0] * path_len, y + direction[1] * path_len, path_len)
        )
    return path


def outside(x, y, rows, columns) -> bool:
    """Is the coordinate outside the grid?"""
    return x < 0 or x >= columns or y < 0 or y >= rows


def min_loss(input: list[list[int]], min_moves: int, max_moves: int) -> int:
    states: dict[tuple[int, int, tuple[int, int]], float] = defaultdict(
        lambda: float("inf")
    )
    queue: list[tuple[int, int, int, tuple[int, int]]] = []
    rows = len(input)
    columns = len(input[0])
    heappush(queue, (0, 0, 0, RIGHT))
    heappush(queue, (0, 0, 0, DOWN))
    while queue:
        loss, x, y, next_direction = heappop(queue)
        if x == columns - 1 and y == rows - 1:
            return loss
        if loss >= states[(x, y, next_direction)]:
            continue
        states[(x, y, next_direction)] = loss
        added_loss = 0
        for nx, ny, path_len in path(x, y, next_direction, max_moves):
            if outside(nx, ny, rows, columns):
                break
            added_loss += input[ny][nx]
            if path_len >= min_moves:
                for possible_direction in next_directions(next_direction):
                    heappush(queue, (loss + added_loss, nx, ny, possible_direction))
    return -1


text = Path("17.ultra").read_text()
text = Path("17.ex").read_text()
text = Path("17.in").read_text()
input = parse_input(text)
# print(min_loss(input, 1, 3))
print(min_loss(input, 4, 10))
