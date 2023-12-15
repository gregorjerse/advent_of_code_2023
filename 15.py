import re
from pathlib import Path
from typing import Optional


def parse_input(input: str) -> list[tuple[str, int, str, Optional[str]]]:
    """Parse input."""
    parsed = []
    for split in input.strip().split(","):
        m = re.match(r"(?P<label>\w+)(?P<operator>[=\-])(?P<focal>\d+)?", split)
        assert m is not None
        parsed.append((m["label"], hash_me(m["label"]), m["operator"], m["focal"]))
    return parsed


def hash_me(string: str):
    """Return the hast of the input strin."""
    value = 0
    for character in string:
        value = ((value + ord(character)) * 17) % 256
    return value


text = Path("15.in").read_text()
# text = Path("15.ex").read_text()


"""Note: the solution for part 2 heavily relies on the fact that iteration ove
keys (or values) in Python dictionary is guaranteed to be in the same order as
they were insterted. This was implementation detail in CPython 3.6 but it is 
guaranteed in Python 3.7+. This is not necessary true for other Python
implementations."""

hash_sum = 0
boxes: list[dict[str, int]] = [dict() for _ in range(256)]
for label, box_number, operator, focal in parse_input(text):
    hash_sum += hash_me(f"{label}{operator}" + (focal if focal is not None else ""))
    match operator, focal:
        case "-", None:
            boxes[box_number].pop(label, None)
        case "=", number if number is not None:
            boxes[box_number][label] = int(number)
        case _:
            raise ValueError(f"Invalid input: {label}{operator}{number}")

print(hash_sum)
print(
    sum(
        (box_num + 1) * (slot + 1) * focal
        for box_num in range(256)
        for slot, focal in enumerate(boxes[box_num].values())
    )
)
