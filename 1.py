# This solution is an exercise in Aho - Corasick algorithm (not really necessary for
# this problem, but a good implementation exercise).
#
# https://en.wikipedia.org/wiki/Aho%E2%80%93Corasick_algorithm
#

from collections import deque
from enum import Enum, auto
from pathlib import Path
from typing import Iterable, Optional

from num2words import num2words


class NodeType(Enum):
    INTERNAL = auto()
    DICTIONARY = auto()


class Node:
    """A node in a trie."""

    def __init__(self, node_type: NodeType, value: str = ""):
        """Initialize the node."""
        self.type = node_type
        self.value = value
        self.suffix_node: Optional[Node] = None
        self.dictionary_nodes: list[Node] = []
        self.children: list[Node] = []
        self.parent: Optional[Node] = None

    def add_child(self, node: "Node"):
        """Add a child node."""
        self.children.append(node)
        node.parent = self

    def search(self, value: str) -> Optional["Node"]:
        """Search the childred for the value."""
        for node in self.children:
            if node.value == value:
                return node
        return None

    def __iter__(self):
        """Perform the BFS starting from this node.

        The current node is not included.
        """
        queue = deque(self.children)
        while queue:
            node = queue.popleft()
            queue.extend(node.children)
            yield node

    def __repr__(self) -> str:
        """Construct a string representation of the node."""
        prefix = self.value
        start: Optional[Node] = self
        while start := start.parent:
            prefix = start.value + prefix
        return prefix


class AhoCorasick:
    """Aho-Corasick implementation."""

    def __init__(self, patterns: Iterable[str]):
        """Construct the Aho-Corasick graph from the patterns."""
        self.root = self._construct_graph(patterns)
        self._compute_suffix_links()
        self._compute_dictionary_links()
        self._state = self.root

    def _add_char(self, char: str):
        """Apply char to the current state."""
        while True:
            if child := self._state.search(char):
                self._state = child
                break
            elif self._state.suffix_node is None:
                self._state = self.root
                break
            else:
                self._state = self._state.suffix_node

    def first_match(self, text: str) -> Optional[str]:
        """Return the first occurence of the substring."""
        self._state = self.root
        for char in text:
            self._add_char(char)
            dictionary_nodes = self._state.dictionary_nodes
            if self._state.type == NodeType.DICTIONARY:
                dictionary_nodes.append(self._state)
            if dictionary_nodes:
                return str(dictionary_nodes[0])
        return None

    def _compute_dictionary_links(self):
        """Compute the dictionary nodes."""
        for node in self.root:
            node.dictionary_nodes = list(node.suffix_node.dictionary_nodes)
            if node.suffix_node.type == NodeType.DICTIONARY:
                node.dictionary_nodes.append(node.suffix_node)

    def _compute_suffix_links(self):
        """Compute the suffix links.

        Compute the suffix links by performing the BFS on the trie and process nodes along
        the way.
        """
        for node in self.root:
            if node.parent == self.root:
                node.suffix_node = self.root
                continue
            current_node = node.parent.suffix_node
            while node.suffix_node is None:
                if child := current_node.search(node.value):
                    node.suffix_node = child
                elif current_node == self.root:
                    node.suffix_node = self.root
                current_node = current_node.suffix_node

    def _construct_graph(self, patterns: Iterable[str]) -> Node:
        """Constract a trie from the patterns.

        :returns: the root node of the trie.
        """
        root = Node(NodeType.INTERNAL)
        for pattern in patterns:
            current_node = root
            for char in pattern:
                child = current_node.search(char)
                if not child:
                    child = Node(NodeType.INTERNAL, char)
                    current_node.add_child(child)
                current_node = child
            # The node representing the last char in pattern is a dictionary node.
            current_node.type = NodeType.DICTIONARY
        return root


patterns = {str(i): i for i in range(1, 10)}
patterns.update({num2words(i): i for i in range(1, 10)})


def line_value(
    text: str, corasich: AhoCorasick, reverse_corasich: AhoCorasick, mapping
) -> int:
    first = corasich.first_match(text)
    last = reverse_corasich.first_match(text[::-1])
    assert first is not None and last is not None
    return 10 * mapping[first] + mapping[last[::-1]]


reverse_patterns = {key[::-1] for key in patterns.items()}
corasich = AhoCorasick(patterns.keys())
reverse_corasich = AhoCorasick({key[::-1] for key in patterns})
data = Path("1.in").read_text().splitlines()
result = sum(line_value(line, corasich, reverse_corasich, patterns) for line in data)
print(result)
