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


def process(rules):
    """Process a part."""
    queue = [
        {
            "x": (1, 4000),
            "m": (1, 4000),
            "a": (1, 4000),
            "s": (1, 4000),
            "process": "in",
            "rule_num": 0,
        }
    ]
    operators = {"<": lt, ">": gt}
    accepted_states = 0
    while queue:
        current = queue.pop()
        if current["process"] == "R":
            continue
        if current["process"] == "A":
            accepted_states += (
                (current["x"][1] - current["x"][0] + 1)
                * (current["m"][1] - current["m"][0] + 1)
                * (current["a"][1] - current["a"][0] + 1)
                * (current["s"][1] - current["s"][0] + 1)
            )
            continue

        to_process = rules[current["process"]].split(",")
        current_rule = to_process[current["rule_num"]]
        if current["rule_num"] == len(to_process) - 1:
            queue.append({**current, "rule_num": 0, "process": current_rule})
            continue

        m = re.match(
            r"(?P<property>\w)(?P<op>[<>])(?P<result>\w+):((?P<next>\w+))",
            current_rule,
        )
        e = int(m["result"])
        current_interval = current[m["property"]]
        op = operators[m["op"]]
        if m["op"] == ">":
            current_interval = [current_interval[1], current_interval[0]]
        diff = 1 if m["op"] == ">" else -1
        interval_pass = list()
        interval_fail = list()
        if op(current_interval[1], e):
            interval_pass = current_interval
        elif op(current_interval[0], e):
            interval_pass = sorted((e + diff, current_interval[0]))
            interval_fail = sorted((current_interval[1], e))
        else:
            interval_fail = current_interval
        if interval_fail:
            queue.append(
                {
                    **current,
                    m["property"]: interval_fail,
                    "rule_num": current["rule_num"] + 1,
                }
            )
        if interval_pass:
            queue.append(
                {
                    **current,
                    m["property"]: interval_pass,
                    "rule_num": 0,
                    "process": m["next"],
                }
            )

    return accepted_states


text = Path("19.in").read_text()
# text = Path("19.ex").read_text()

rules, parts = parse_input(text)
print(process(rules))
