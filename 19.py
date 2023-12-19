from pathlib import Path
from operator import lt, gt
import re


def parse_input(input: str):
    """Parse the input."""
    first, second = input.split("\n\n")
    rules = dict(re.findall(r"(?P<name>\w+){(?P<rules>[\w<>:,]+)}", first))
    parts = [
        (int(x), int(m), int(a), int(s))
        for x, m, a, s in re.findall(
            r"{x=(?P<x>\d+),m=(?P<m>\d+),a=(?P<a>\d+),s=(?P<s>\d+)}", second
        )
    ]
    return rules, parts


def process(part, rules):
    """Process a part."""
    d = {"x": part[0], "m": part[1], "a": part[2], "s": part[3]}
    operators = {"<": lt, ">": gt}
    queue = ["in"]
    while True:
        processing = queue.pop()
        to_process = rules[processing].split(",")
        for rule in to_process:
            m = re.match(
                r"(?P<cond>(?P<name>\w)(?P<op>[<>])(?P<res>\w+):)?((?P<next>\w+))",
                rule,
            )
            if m["cond"] is None or operators[m["op"]](d[m["name"]], int(m["res"])):
                if m["next"] in "AR":
                    return m["next"] == "A"
                queue.append(m["next"])
                break


text = Path("19.in").read_text()
text = Path("19.ex").read_text()

rules, parts = parse_input(text)
print(sum(sum(part) for part in parts if process(part, rules)))
