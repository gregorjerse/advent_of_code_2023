import array
import re
from pathlib import Path


def parse_game(game: str) -> int:
    """Parse the game string."""
    m = re.match(r"Card +(?P<card>\d+): *(?P<win>[\d ]*) *\| *(?P<given>[\d ]+)", game)
    assert m is not None, game
    return len(
        set(map(int, re.sub(r" +", " ", m["win"]).strip().split(" ")))
        & set(map(int, re.sub(r" +", " ", m["given"]).strip().split(" ")))
    )


lines = Path("4.in").read_text().splitlines()
# lines = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
# Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
# Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
# Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
# Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
# Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11""".split(
#     "\n"
# )

parsed = [parse_game(line) for line in lines]
print(sum(2 ** (match - 1) for match in parsed if match))

how_many: array.array = array.array("I", [1] * len(lines))
for card_number, match in enumerate(parsed):
    for copies in range(match):
        how_many[card_number + copies + 1] += how_many[card_number]
print(sum(how_many))
