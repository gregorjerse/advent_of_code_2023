from pathlib import Path
from itertools import dropwhile
from collections import Counter

Strength = int
Hand = str
Card = str
Cards = dict[Card, Strength]

# Possible values: True / False
JOKER = True

cards = {"A": 14, "K": 13, "Q": 12, "J": 1 if JOKER else 11, "T": 10}
cards.update({str(i): i for i in range(2, 9 + 1)})


class CardHand:
    def __init__(self, hand: Hand, factor: int, cards: Cards, joker: bool = False):
        self.cards = cards
        self.hand = hand
        self.joker = joker
        self.factor = factor
        self._compute_strength()

    def _compute_strength(self):
        if self.joker and "J" in self.hand:
            self.hand_strength = sorted(
                CardHand(new_hand, self.factor, self.cards)
                for new_hand in (hand.replace("J", card) for card in cards)
            )[-1].hand_strength
        else:
            self.hand_strength = self._hand_strength(self.hand)

    def _hand_strength(self, hand: Hand) -> Strength:
        """Return the strength of a hand."""
        card_counter = Counter(hand)
        return {(5, 1): 10, (4, 2): 9, (3, 2): 8, (3, 3): 7, (2, 3): 6, (2, 4): 5}.get(
            (card_counter.most_common()[0][1], len(card_counter)), 4
        )

    def __lt__(self, other: "CardHand") -> bool:
        """Compare cards."""
        if self.hand_strength != other.hand_strength:
            return self.hand_strength < other.hand_strength
        try:
            card1, card2 = next(
                dropwhile(
                    lambda cards: cards[0] == cards[1], zip(self.hand, other.hand)
                )
            )
            return self.cards[card1] < self.cards[card2]
        except StopIteration:
            return False

    def __repr__(self) -> str:
        """Return string representation."""
        return f"({self.hand}, {self.factor})"


lines = Path("7.in").read_text().splitlines()
# lines = Path("7.ex").read_text().splitlines()

hands = []
for line in lines:
    hand, factor = line.split()
    hands.append(CardHand(hand, int(factor), cards, JOKER))

print(sum(rank * card.factor for rank, card in enumerate(sorted(hands), start=1)))
