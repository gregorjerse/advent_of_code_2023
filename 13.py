from typing import Optional
from pathlib import Path


def parse_input(input: str) -> list[list[str]]:
    """Parse input."""
    return [test_case.splitlines() for test_case in input.split("\n\n")]


def reflect_horizontal(input: list[str], ignore: Optional[int] = None) -> int:
    """Get all horizontal refrections."""
    for reflection in range(1, len(input)):
        if reflection == ignore:
            continue
        end = min(len(input), 2 * reflection)
        start = max(2 * reflection - len(input), 0)
        before = input[start:reflection]
        before.reverse()
        if before == input[reflection:end]:
            return reflection
    return 0


def reflect_vertical(input, ignore: Optional[int] = None) -> int:
    """Get all vertical refrections."""
    return reflect_horizontal(["".join(e) for e in zip(*input)], ignore=ignore)


text = Path("13.in").read_text()
# text = Path("13.ex").read_text()
input = parse_input(text)

s2 = 0
s1 = 0
for game in input:
    found = False
    old_horizontal = reflect_horizontal(game)
    old_vertical = reflect_vertical(game)
    s1 += old_horizontal * 100 + old_vertical
    for y in range(len(game)):
        for x in range(len(game[0])):
            new_character = "." if game[y][x] == "#" else "#"
            new_game = game[:y]
            new_game.append(game[y][:x] + new_character + game[y][x + 1 :])
            new_game.extend(game[y + 1 :])
            if result := (
                reflect_horizontal(new_game, ignore=old_horizontal) * 100
                + reflect_vertical(new_game, ignore=old_vertical)
            ):
                s2 += result
                found = True
                break
        if found:
            break
    assert found
print(s1, s2)
