from enum import Enum
from abc import ABC, abstractmethod
import random
from collections import Counter

"""Card library with a standard deck, standard cards and a hand which holds the cards and is able to find
the best poker hand.
Created by Rikard Radovac & Péter Gaal in the course DAT171 at Chalmers university of technology
2022-02-17
"""


class Suit(Enum):
    """Class representing suit values with Enum
    """
    Hearts = 1
    Spades = 2
    Clubs = 3
    Diamonds = 4

    def __str__(self):
        """Returns the suit unicode symbol
        """
        if self.name == "Hearts":
            return "♥"
        elif self.name == "Spades":
            return "♠"
        elif self.name == "Clubs":
            return "♣"
        elif self.name == "Diamonds":
            return "♦"

    def __lt__(self, other):
        return self.value < other.value

    def __eq__(self, other):
        return self.value == other.value


class PlayingCard(ABC):
    """Base class defining values and suits and passing on the methods to its children.
    """

    def __init__(self, suit: Suit):
        self.suit = suit

    @abstractmethod
    def get_value(self):
        """
        Abstract method that represents the value for the card

        Returns:
            int: Returns the card value
        """
        pass

    @abstractmethod
    def __str__(self):
        pass

    @abstractmethod
    def __repr__(self):
        pass

    def __lt__(self, other):
        """Defines the "less than" comparing between values

        Args:
            other (int, Suit): other card value

        Returns:
            int, Suit: returns the smaller value
        """
        return (self.get_value(), self.suit) < (other.get_value(), other.suit)

    def __eq__(self, other):
        """Defines the equal comparing between cards

        Args:
            other (int, Suit): Other card value

        Returns:
            int, Suit: equal value
        """
        return (self.get_value(), self.suit) == (other.get_value(), other.suit)


class NumberedCard(PlayingCard):
    """Class representing the Numbered cards. Subclass of PlayingCard
    """

    def __init__(self, value: int, suit: Suit):
        super().__init__(suit)
        self.value = value

    def get_value(self):
        """Returns the cards value

        Returns:
            int: Card value
        """
        return self.value

    def __str__(self):
        """Defines how the str-method is applied

        Returns:
            string: "number" "suit"
        """
        return f"{self.get_value()} {self.suit}"

    def __repr__(self):
        return f"{self.get_value()} {self.suit}"


class JackCard(PlayingCard):
    """Class representing the Jack cards. Subclass of PlayingCard
    """

    def get_value(self):
        """Returns the cards value

        Returns:
            int: Card value
        """
        return 11

    def __str__(self):
        """Defines how the str-method is applied

        Returns:
            string: Jack of "suit"
        """
        return f"Jack {self.suit}"

    def __repr__(self):
        return f"Jack {self.suit}"


class QueenCard(PlayingCard):
    """Class representing the Queen cards. Subclass of PlayingCard
    """

    def get_value(self):
        """Returns the cards value

        Returns:
            int: Card value
        """
        return 12

    def __str__(self):
        """Defines how the str-method is applied

        Returns:
            string: Queen "suit"
        """
        return f"Queen {self.suit}"

    def __repr__(self):
        return f"Queen {self.suit}"


class KingCard(PlayingCard):
    """Class representing the King cards. Subclass of PlayingCard
    """

    def get_value(self):
        """Returns the cards value

        Returns:
            int: Card value
        """
        return 13

    def __str__(self):
        """Defines how the str-method is applied

        Returns:
            string: King "suit"
        """
        return f"King {self.suit}"

    def __repr__(self):
        return f"King {self.suit}"


class AceCard(PlayingCard):
    """Class representing the Ace cards. Subclass of PlayingCard
    """

    def get_value(self):
        """Returns the cards value

        Returns:
            int: Card value
        """
        return 14

    def __str__(self):
        """Defines how the str-method is applied

        Returns:
            string: Ace "suit"
        """
        return f"Ace of {self.suit}"

    def __repr__(self):
        return f"Ace {self.suit}"


class Hand:
    """Hand class describing the current cards in the hand with methods to add, draw, sort and calculate the
    best poker hand
    """

    def __init__(self):
        self.cards = []

    def add_card(self, card):
        """Adds a specified card to the hand

        Args:
            card (Object): The card to add
        """
        self.cards.append(card)

    def drop_cards(self, index_list: list):
        """Drops cards on specified indices

        Args:
            index_list (list): list of indices
        """
        for index in sorted(index_list, reverse=True):
            self.cards.pop(index)

    def sort(self):
        """Sorts the hand in ascending order
        """
        self.cards.sort()

    def best_poker_hand(self, cards: list[PlayingCard] = []):
        """Checks the current best possible poker hand

        Args:
            cards (list): List of cards on the table

        Returns:
            PokerHand (Object): Object representing the poker hand
        """

        total_cards = self.cards + cards
        return PokerHand(total_cards)

    def __str__(self):
        return f"Current cards in hand: {self.cards}"

    def __lt__(self, other):
        """Defines the "less than" comparing between values

        Args:
            other (Hand): other cards

        Returns:
            list: returns the smaller list
        """
        return self.cards < other.cards

    def __eq__(self, other):
        return self.cards == other.cards


class PokerHandType(Enum):
    """Class representing the different poker hand types with Enum values.
    """
    straight_flush = 9
    four_of_a_kind = 8
    full_house = 7
    flush = 6
    straight = 5
    three_of_a_kind = 4
    two_pair = 3
    one_pair = 2
    high_card = 1

    def __lt__(self, other):
        """Defines the "less than" comparing between values

        Args:
            other (PokerHandType): other card value

        Returns:
            int: returns the smaller value
        """
        return self.value < other.value

    def __eq__(self, other):
        """Defines the "equal" comparing between values

        Args:
            other (PokerHandType): other card value

        Returns:
            int: returns the equal value
        """
        return self.value == other.value

    def __str__(self):
        """Returns a readable poker hand type
        """
        if self.name == "straight_flush":
            return "Straight flush"
        elif self.name == "four_of_a_kind":
            return "Four of a kind"
        elif self.name == "full_house":
            return "Full house"
        elif self.name == "flush":
            return "Flush"
        elif self.name == "straight":
            return "Straight"
        elif self.name == "three_of_a_kind":
            return "Three of a kind"
        elif self.name == "two_pair":
            return "Two pair"
        elif self.name == "one_pair":
            return "One pair"
        elif self.name == "high_card":
            return "High card"


class PokerHand:
    """Class representing a poker hand

    Args:
        cards (list): list of cards
    """

    def __init__(self, cards):
        functions = [self.check_straight_flush, self.check_four_of_a_kind,
                     self.check_full_house, self.check_flush, self.check_straight,
                     self.check_three_of_a_kind, self.check_two_pair,
                     self.check_one_pair, self.check_high_card]

        # Checks the best possible poker hand from best to worst
        for function in functions:
            result = function(cards)
            if result is not None:
                self.hand_type, self.values = result
                break

    @staticmethod
    def check_straight_flush(cards):
        """Checks for the best straight flush in a list of cards (may be more than just 5)

        Args:
            cards (list): A list of playing cards

        Returns:
            PokerHandType, tuple: None if no straight flush is found,
            else a PokerhandType value and the value of the top card.
        """
        if len(cards) >= 5:
            vals = [(c.get_value(), c.suit) for c in cards] \
                   + [(1, c.suit) for c in cards if c.get_value() == 14]  # Add the aces!
            for c in reversed(cards):  # Starting point (high card)
                # Check if we have the value - k in the set of cards:
                found_straight = True
                for k in range(1, 5):
                    if (c.get_value() - k, c.suit) not in vals:
                        found_straight = False
                        break
                if found_straight:
                    return PokerHandType.straight_flush, (c.get_value())

    @staticmethod
    def check_four_of_a_kind(cards):
        """Checks for the best straight flush in a list of cards (may be more than just 5)

        Args:
            cards (list): A list of playing cards

        Returns:
            PokerHandType, tuple: None if no straight flush is found,
            else a PokerhandType value and a tuple
            with the value of the four of a kind card and the highest card left.
        """
        if len(cards) >= 4:
            values = []
            for c in cards:
                values.append(c.get_value())
            for value in values:
                if values.count(value) == 4:
                    kicker_cards = [x for x in values if x != value]
                    return PokerHandType.four_of_a_kind, (value, sorted(kicker_cards, reverse=True)[:1])

    @staticmethod
    def check_full_house(cards):
        """
        Checks for the best full house in a list of cards (may be more than just 5)

        Args:
            cards: A list of playing cards

        Returns:
            PokerHandType, tuple: None if no full house is found,
            else a PokerhandType value and the values of the cards.
        """
        if len(cards) >= 5:
            value_count = Counter()
            for c in cards:
                value_count[c.get_value()] += 1
            # Find the card ranks that have at least three of a kind
            threes = [v[0] for v in value_count.items() if v[1] >= 3]
            threes.sort()
            # Find the card ranks that have at least a pair
            twos = [v[0] for v in value_count.items() if v[1] >= 2]
            twos.sort()

            # Threes are dominant in full house, lets check that value first:
            for three in reversed(threes):
                for two in reversed(twos):
                    if two != three:
                        return PokerHandType.full_house, (three, two)

    @staticmethod
    def check_flush(cards):
        """Checks for the best flush in a list of cards (may be more than just 5)

        Args:
            cards (list): A list of playing cards

        Returns:
            PokerHandType, tuple: None if no flush is found, else a PokerHandType value and a tuple
             with the five highest cards in the flush.
        """
        if len(cards) >= 5:
            suits = [c.suit for c in cards]
            for flush in suits:
                if suits.count(flush) >= 5:
                    flush_cards = [x for x in cards if x.suit == flush]
                    return PokerHandType.flush, (sorted(flush_cards, reverse=True))[:5]

    @staticmethod
    def check_straight(cards):
        """Checks for the best straight in a list of cards (may be more than just 5)

        Args:
            cards (list): A list of playing cards

        Returns:
            PokerHandType, int: None if no straight is found,
            else a PokerHandType value with the value of the top card.
        """
        if len(cards) >= 5:
            vals = [c.get_value() for c in cards] \
                   + [1 for c in cards if c.get_value() == 14]  # Add the aces!
            for c in reversed(cards):  # Starting point (high card)
                # Check if we have the value - k in the set of cards:
                found_straight = True
                for k in range(1, 5):
                    if c.get_value() - k not in vals:
                        found_straight = False
                        break
                if found_straight:
                    return PokerHandType.straight, (c.get_value())

    @staticmethod
    def check_three_of_a_kind(cards):
        """Checks for the best three of a kind in a list of cards (may be more than just 5)

        Args:
            cards (list): A list of playing cards

        Returns:
            PokerHandType, tuple: None if no three of a kind is found,
             else a PokerHandType value with a tuple of the highest remaining cards.
        """

        values = []
        for c in cards:
            values.append(c.get_value())
        for value in values:
            if values.count(value) == 3:
                kicker_cards = [x for x in values if x != value]
                return PokerHandType.three_of_a_kind, (value, sorted(kicker_cards, reverse=True)[:2])

    @staticmethod
    def check_two_pair(cards):
        """Checks for the best two pairs in a list of cards (may be more than just 5)

        Args:
            cards (list): A list of playing cards

        Returns:
            PokerHandType, tuple None if no two pair is found,
             else a PokerHandType object with a tuple of the pair values and the highest remaining card.
        """
        if len(cards) >= 5:
            values = [c.get_value() for c in cards]
            counted_cards = Counter(values)
            two_pair, count = zip(*counted_cards.most_common(2))
            if count == (2, 2):
                kicker_card = sorted([x for x in values if x != two_pair[0] and x != two_pair[1]], reverse=True)[:1]
                return PokerHandType.two_pair, (sorted([two_pair[0], two_pair[1]]), kicker_card)

    @staticmethod
    def check_one_pair(cards):
        """Checks for the best pair in a list of cards (may be more than just 5)

        Args:
            cards (list): A list of playing cards

        Returns:
            PokerHandType, tuple: None if no pair is found,
            else a PokerHandType value with a tuple of the highest remaining cards.
        """

        values = [c.get_value() for c in cards]
        for value in values:
            if values.count(value) == 2:
                kicker_cards = [x for x in values if x != value]
                return PokerHandType.one_pair, (value, sorted(kicker_cards, reverse=True)[:3])

    @staticmethod
    def check_high_card(cards):
        """Checks for the highest in a list of cards (may be more than just 5)

        Args:
            cards (list): A list of playing cards

        Returns:
            PokerHandType, tuple: a PokerHandType value
            with a tuple of the five highest cards.
        """

        values = [c.get_value() for c in cards]
        return PokerHandType.high_card, (sorted(values, reverse=True)[:5])

    def __str__(self):
        """Prints out the different hands nicely
        """
        if self.hand_type == PokerHandType.straight_flush:
            return f"{self.hand_type} with highest card {self.values}"
        elif self.hand_type == PokerHandType.straight:
            return f"{self.hand_type} with highest card {self.values}"
        elif self.hand_type == PokerHandType.one_pair:
            return f"{self.hand_type} with {self.values[0]} and the highest card {self.values[1][0]}"
        return f"{self.hand_type} with {self.values[0]}"

    def __lt__(self, other):
        """Defines the "less than" comparing between values

        Args:
            other (PokerHand, list): other card value

        Returns:
            PokerHand, int: returns the smaller value
        """
        return (self.hand_type, self.values) < (other.hand_type, other.values)

    def __eq__(self, other):
        return (self.hand_type, self.values) == (other.hand_type, other.values)


class StandardDeck:
    """Creates a standard deck of cards (52 cards, 4 suits) using the subclasses of PlayingCard
    """

    def __init__(self):
        self.cards = []
        for suit in Suit:
            for value in range(2, 11):
                self.cards.append(NumberedCard(value, suit))
            self.cards.append(KingCard(suit))
            self.cards.append(QueenCard(suit))
            self.cards.append(JackCard(suit))
            self.cards.append(AceCard(suit))

    def shuffle(self):
        """Shuffles the deck"""
        random.shuffle(self.cards)

    def draw(self):
        """Draw the top card from the deck"""
        return self.cards.pop(0)

    def __len__(self):
        """
        Returns:
            int: returns the length of the cards
        """
        return len(self.cards)

    def __str__(self):
        return str(self.cards)

    def __lt__(self, other):
        return self.cards < other.cards

    def __eq__(self, other):
        return self.cards == other.cards
