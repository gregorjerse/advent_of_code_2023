import re
import math
from pathlib import Path
from itertools import cycle
from typing import Callable

Instructions = str
Node = str
Mapping = dict[Node, tuple[Node, Node]]

# Set to 1 or 2.
PROBLEM = 2


def parse_game(lines: list[str]) -> tuple[Instructions, Mapping]:
    """Parse the game string and return mapping and instructions."""
    instructions = lines[0]
    mapping = dict()
    for line in lines[2:]:
        m = re.match(r"(?P<node>\w+) = \((?P<left>\w+), (?P<right>\w+)\)", line)
        assert m is not None, line
        mapping[m["node"]] = (m["left"], m["right"])
    return instructions, mapping


def single_node_path(
    node: Node,
    mapping: Mapping,
    instructions: Instructions,
    final_condition: Callable[[Node], bool],
) -> int:
    """Return the length of the path for a single node."""
    for step, instruction in enumerate(cycle(instructions), start=1):
        node = mapping[node][0] if instruction == "L" else mapping[node][1]
        if final_condition(node):
            return step
    return 0


lines = Path("8.in").read_text().splitlines()
# lines = Path("8.ex").read_text().splitlines()

if PROBLEM == 1:
    starting_condition = lambda node: node == "AAA"
    final_condition = lambda node: node == "ZZZ"
else:
    starting_condition = lambda node: node[-1] == "A"
    final_condition = lambda node: node[-1] == "Z"

instructions, mapping = parse_game(lines)
starting_nodes = [node for node in mapping if starting_condition(node)]
cycles = (
    single_node_path(node, mapping, instructions, final_condition)
    for node in starting_nodes
)
print(math.lcm(*cycles))
