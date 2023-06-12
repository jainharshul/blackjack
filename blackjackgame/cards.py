"""A French suited playing card class and a Deck of 52 cards class"""

from collections import namedtuple
from random import shuffle, randrange
from math import ceil

Card = namedtuple("Card", ["rank", "suit"])


def _str_card(card):
    """Convert a card to a nicely formatted string"""
    return f"{card.rank} of {card.suit}"


Card.__str__ = _str_card


def is_ace(card):
    """Check to see if a card has the rank of Ace."""
    return card.rank == "Ace"


Card.is_ace = is_ace


def is_ten(card):
    """Check to see if a given card has the rank of 10"""
    return card.rank in "10 Jack Queen King".split()


Card.is_ten = is_ten


class Deck:
    """Deck class to hold 52 French suited playing cards."""

    ranks = ["Ace"] + [str(x) for x in range(2, 11)] + "Jack Queen King".split()
    suits = "♣️ ♥️ ♠️ ♦️".split()
    values = list(range(1, 11)) + [10, 10, 10]
    value_dict = dict(zip(ranks, values))

    def __init__(self, num_decks=1):
        """Create multiple decks of cards. The cards are not in new deck order."""
        self._cards = [
            Card(rank, suit)
            for _ in range(num_decks)
            for suit in self.suits
            for rank in self.ranks
        ]
        self._cursor = 0

    def __len__(self):
        """Return the number of cards in the deck."""
        return len(self._cards)

    def __getitem__(self, position):
        """Return the card at the given position."""
        return self._cards[position]

    def __iter__(self):
        """Iterator to start from the face of the deck and iterate to the bottom."""
        self._cursor = 0
        return self

    def __next__(self):
        """Return the next card in the deck."""
        if self._cursor < len(self._cards):
            pos = self._cursor
            self._cursor = self._cursor + 1
            return self._cards[pos]
        self._cursor = 0
        raise StopIteration()

    def shuffle(self, num=1):
        """Shuffle the deck n times. Default is 1 time."""
        for _ in range(num):
            shuffle(self._cards)

    def cut(self):
        """Cut the deck at approximately the half way point +/- 10 cards."""
        extra = ceil(len(self._cards) * 0.2)
        half = (len(self._cards) // 2) + randrange(-extra, extra)
        tophalf = self._cards[:half]
        bottomhalf = self._cards[half:]
        self._cards = bottomhalf + tophalf

    def get_cards(self):
        """Return the cards in the deck."""
        return self._cards

    def deal(self, num=1):
        """Deal n cards. Default is 1 card."""
        return [self._cards.pop() for x in range(num)]

    def merge(self, deck: "Deck"):
        """Merge the current deck with the deck passed as a parameter."""
        self._cards.extend(deck.get_cards())

    def __str__(self):
        """Convert the deck to a string."""
        return ", ".join(map(str, self._cards))


def card_value(card):
    """Return the numerical value of the rank of a given card."""
    return Deck.value_dict[card.rank]


Card.value = card_value
Card.__int__ = card_value
