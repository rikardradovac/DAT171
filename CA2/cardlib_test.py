from enum import Enum
import pytest

from cardlib import *


# This test assumes you call your suit class "Suit" and the suits "Hearts and "Spades"
def test_cards():
    h5 = NumberedCard(4, Suit.Hearts)
    assert isinstance(h5.suit, Enum)

    sk = KingCard(Suit.Spades)
    assert sk.get_value() == 13

    assert h5 < sk
    assert h5 == h5

    #tests to print out a card
    assert str(sk) == "King ♠"


# This test assumes you call your shuffle method "shuffle" and the method to draw a card "draw"
def test_deck():
    d = StandardDeck()
    c1 = d.draw()
    c2 = d.draw()
    assert not c1 == c2

    d2 = StandardDeck()
    d2.shuffle()
    c3 = d2.draw()
    c4 = d2.draw()
    assert not ((c3, c4) == (c1, c2))
    assert len(d) == len(d2)
    assert d != d2



# This test builds on the assumptions above and assumes you store the cards in the hand in the list "cards",
# and that your sorting method is called "sort" and sorts in increasing order
def test_hand():
    h = Hand()
    assert len(h.cards) == 0
    d = StandardDeck()
    d.shuffle()
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    h.add_card(d.draw())
    assert len(h.cards) == 5

    h.sort()
    for i in range(4):
        assert h.cards[i] < h.cards[i + 1] or h.cards[i] == h.cards[i + 1]

    cards = h.cards.copy()
    h.drop_cards([3, 0, 1])
    assert len(h.cards) == 2
    assert h.cards[0] == cards[2]
    assert h.cards[1] == cards[4]


# This test builds on the assumptions above. Add your type and data for the commented out tests
# and uncomment them!
def test_pokerhands():
    h1 = Hand()
    h1.add_card(QueenCard(Suit.Diamonds))
    h1.add_card(KingCard(Suit.Hearts))

    h2 = Hand()
    h2.add_card(QueenCard(Suit.Hearts))
    h2.add_card(AceCard(Suit.Hearts))

    cl = [NumberedCard(10, Suit.Diamonds), NumberedCard(9, Suit.Diamonds),
          NumberedCard(8, Suit.Clubs), NumberedCard(6, Suit.Spades)]

    ph1 = h1.best_poker_hand(cl)
    assert isinstance(ph1, PokerHand)
    ph2 = h2.best_poker_hand(cl)
    # assert # Check ph1 handtype class and data here>
    # assert # Check ph2 handtype class and data here>

    assert ph1 < ph2

    cl.pop(0)
    cl.append(QueenCard(Suit.Spades))
    ph3 = h1.best_poker_hand(cl)
    ph4 = h2.best_poker_hand(cl)
    assert ph3 < ph4
    assert ph1 < ph2

    # assert # Check ph3 handtype class and data here>
    # assert # Check ph4 handtype class and data here>


def test_comparison():
    """
    Compares different hands with different valued cards and checks different decks with each other
    """
    p1 = Hand()
    p2 = Hand()
    p1.add_card(QueenCard(Suit.Spades))
    p2.add_card(QueenCard(Suit.Hearts))

    assert p1 > p2  # Suits matter when checking two cards

    p1.add_card(KingCard(Suit.Spades))
    p2.add_card(JackCard(Suit.Hearts))

    assert p1 > p2  # More cards result in tuple comparing

    p1 = Hand()
    p2 = Hand()

    p1.add_card(QueenCard(Suit.Hearts))
    p2.add_card(QueenCard(Suit.Hearts))
    p1.add_card(KingCard(Suit.Hearts))
    p2.add_card(KingCard(Suit.Hearts))
    p1.add_card(AceCard(Suit.Hearts))
    p2.add_card(AceCard(Suit.Hearts))

    assert p1 == p2  # Tests comparing exactly the same hands (only possible with two or more decks)


    # Testing a flush and determening the winning hand between two hands with flush (highest card in the flush wins)

    f = Hand()
    f.add_card(KingCard(Suit.Spades))
    f.add_card(NumberedCard(2, Suit.Spades))

    f2 = Hand()
    f2.add_card(NumberedCard(10, Suit.Spades))
    f2.add_card(NumberedCard(4, Suit.Spades))
    table = [NumberedCard(3, Suit.Spades), NumberedCard(7, Suit.Spades), NumberedCard(6, Suit.Spades),
             NumberedCard(9, Suit.Hearts), AceCard(Suit.Clubs)]

    p3 = f.best_poker_hand(table)
    p4 = f2.best_poker_hand(table)

    assert p3 > p4  # Only takes the active flush cards into account (not the ace on the table)

    f = Hand()
    f.add_card(KingCard(Suit.Spades))
    f.add_card(KingCard(Suit.Hearts))

    f2 = Hand()
    f2.add_card(NumberedCard(10, Suit.Spades))
    f2.add_card(NumberedCard(10, Suit.Spades))
    table = [NumberedCard(3, Suit.Clubs), NumberedCard(3, Suit.Diamonds), NumberedCard(6, Suit.Spades),
             NumberedCard(9, Suit.Hearts), AceCard(Suit.Clubs)]

    p3 = f.best_poker_hand(table)
    p4 = f2.best_poker_hand(table)

    assert p3 > p4 #highest pair in two pair (pair with 3 is the same but p3 has also a pair with kings)

    f = Hand()
    f.add_card(NumberedCard(5, Suit.Spades))
    f.add_card(AceCard(Suit.Hearts))

    f2 = Hand()
    f2.add_card(NumberedCard(10, Suit.Spades))
    f2.add_card(NumberedCard(4, Suit.Spades))
    table = [KingCard(Suit.Clubs), KingCard(Suit.Diamonds), KingCard(Suit.Spades),
             NumberedCard(2, Suit.Hearts), NumberedCard(3, Suit.Spades)]

    p3 = f.best_poker_hand(table)
    p4 = f2.best_poker_hand(table)

    assert p3 > p4

def test_same_hand():
    """Tests two of the same hands (full house in this case) and compares which one has a higher one"""
    p1 = Hand()
    p1.add_card(NumberedCard(3, Suit.Diamonds))
    p1.add_card(KingCard(Suit.Hearts))
    table = [KingCard(Suit.Hearts), NumberedCard(3, Suit.Clubs), NumberedCard(3, Suit.Diamonds),
             NumberedCard(8, Suit.Clubs), NumberedCard(8, Suit.Clubs)]

    p2 = Hand()
    p2.add_card(NumberedCard(8, Suit.Clubs))
    p2.add_card(KingCard(Suit.Hearts))

    c = p2.best_poker_hand(table)
    b = (p1.best_poker_hand(table))

    # Checks if player 1 has a lower full house than player 2
    assert b < c
    assert c > b

    p3 = Hand()
    p3.add_card(NumberedCard(8, Suit.Clubs))
    p3.add_card(KingCard(Suit.Hearts))

    p4 = Hand()
    p4.add_card(NumberedCard(8, Suit.Clubs))
    p4.add_card(KingCard(Suit.Hearts))

    b = p3.best_poker_hand(table)
    c = (p4.best_poker_hand(table))

    assert b == c




