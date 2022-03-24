from PyQt5.QtCore import QObject, pyqtSignal
import cardlib as cl
from abc import abstractmethod


class CardModel(QObject):
    """ Base class that describes what is expected from the CardView widget """

    new_cards = pyqtSignal()  #: Signal should be emited when cards change.

    @abstractmethod
    def __iter__(self):
        """Returns an iterator of card objects"""

    @abstractmethod
    def flipped(self):
        """Returns true of cards should be drawn face down"""


class HandModel(cl.Hand, CardModel):
    """Class for a model of the hand"""

    def __init__(self):
        cl.Hand.__init__(self)
        CardModel.__init__(self)
        # Additional state needed by the UI
        self.flipped_cards = False

    def __iter__(self):
        return iter(self.cards)

    def flip(self):
        # Flips over the cards (to hide them)
        self.flipped_cards = not self.flipped_cards
        self.new_cards.emit()  # something changed, better emit the signal!

    def flipped(self):
        # This model only flips all or no cards, so we don't care about the index.
        # Might be different for other games though!
        return self.flipped_cards

    def add_card(self, card):
        super().add_card(card)
        self.new_cards.emit()  # something changed, better emit the signal!

    def fold(self):
        self.drop_cards([0, 1])  # Drops the two first cards
        self.new_cards.emit()


class PlayerModel(QObject):
    """Class defining the player and its attributes during wins, losses, bets and folds"""
    update_data = pyqtSignal()

    def __init__(self, name: str, hand: HandModel):
        super().__init__()
        self.name = name
        self.money = 1000
        self.hand = hand
        self.total_bet = 0
        self.has_folded = False
        self.has_called = False
        self.is_all_in = False

    def win(self, amount):
        """Adds and updates the current amount to the players money and resets its total bet"""
        self.money += amount
        self.total_bet = 0
        self.update_data.emit()

    def loss(self):
        """Resets the players total bet and updates the data"""
        self.total_bet = 0
        self.update_data.emit()

    def fold(self):
        """Defines that the player has folded and removes its cards"""
        self.hand.fold()
        self.has_folded = True
        self.update_data.emit()

    def bet(self, amount):
        """Subtracts the bet amount from the players total money and updates"""
        self.money -= amount
        self.total_bet += amount
        self.update_data.emit()


class GameState(QObject):
    """Class representing the Texas Hold'em poker game"""
    update_state = pyqtSignal()
    game_message = pyqtSignal((str,))

    def __init__(self):
        super().__init__()
        self.call_count = None
        self.names = ["Rikard", "Peter"]  # Hard-coded names
        self.running = False
        self.pot = 0
        self.player_turn = 0
        self.bets = [0]
        self.flop = HandModel()
        self.players = [PlayerModel(name, HandModel()) for name in self.names]
        self.deck = cl.StandardDeck()
        self.start()

    def deal(self):
        """Deals two cards to each player and three to the flop"""
        for ind in range(3):
            self.flop.add_card(self.deck.draw())
        for player in self.players:
            for ind in range(2):
                player.hand.add_card(self.deck.draw())
        self.update_state.emit()

    def bet(self, amount):
        """Handles the bets and its logic
        :param amount: The bet amount
        """
        player = self.players[self.player_turn]

        if player.money == 0:
            self.game_message.emit(f"Not enough money!")

        if 0 < amount <= player.money and amount > self.bets[-1]:
            if amount == player.money:
                player.is_all_in = True
            self.pot += amount
            player.bet(amount)
            self.bets.append(amount)
            for players in self.players:
                players.has_called = False
            player.has_called = True

        self.next_player()
        self.update_state.emit()

    def call(self):
        """Handles the call logic"""

        player = self.players[self.player_turn]

        if not player.is_all_in or self.bets[-1] == 0:
            if player.money == 0:
                self.game_message.emit(f"Not enough money!")
                return  # Quits the function so a faulty call doesn't happen
            elif self.bets[-1] == 0:
                return

            if self.bets[-1] > 0:  # Checks from a list of previous bets and uses the last bet
                if player.money > self.bets[-1]:
                    player.bet(self.bets[-1])
                    self.bets.append(self.bets[-1])
                    self.pot += self.bets[-1]
                    player.has_called = True

                else:  # Call an all-in
                    self.pot += player.money
                    player.bet(player.money)
                    player.has_called = True
                    player.is_all_in = True
        else:
            player.has_called = True

        self.next_player()
        self.update_state.emit()

    def fold(self):
        """Defines how the model handles if a player folds"""

        self.players[self.player_turn].fold()
        remaining_players = [player for player in self.players if not player.has_folded]
        if len(remaining_players) <= 1:
            self.winner()
            return

        self.next_player()
        self.update_state()

    def start(self):
        """Starts the Texas Hold'em game"""

        if self.running:
            self.game_message.emit("Game already running")

        self.running = True
        self.deck.shuffle()
        self.deal()
        self.flip_cards()

    def next_game(self):
        """Resets and starts a new game of Texas Hold'em"""

        self.player_turn = (self.player_turn + 1) % len(self.players)
        for player in self.players:
            player.hand.cards.clear()
            player.is_all_in = False
            player.has_called = False
        self.bets = [0]
        self.running = False
        self.deck = cl.StandardDeck()
        self.flop.cards.clear()
        self.update_state.emit()
        self.start()

    def next_player(self):
        """Handles the switch to the next player"""

        self.flip_cards()
        self.player_turn = (self.player_turn + 1) % len(self.players)
        # Checks if all players have called or folded
        proceed = all([player.has_folded or player.has_called for player in self.players])

        if proceed and len(self.flop.cards) < 5:
            self.flop.add_card(self.deck.draw())
            for player in self.players: player.has_called = False
            return
        if proceed and len(self.flop.cards) >= 5:
            for player in self.players: player.has_called = False
            self.winner()

    def flip_cards(self):
        """Flips all un-flipped cards"""
        for player in self.players:
            if not player.hand.flipped():
                player.hand.flip()

    def winner(self):
        """Calculates and informs who the winner is"""
        hands = []
        for player in self.players: hands.append(player.hand.best_poker_hand(self.flop.cards))
        winner = hands.index(max(hands))
        for not_winner in self.players:
            if not_winner == self.players[winner]:
                pass
            not_winner.loss()

        self.players[winner].win(self.pot)
        self.pot = 0
        self.game_message.emit(f"{self.players[winner].name} Won the round with the hand: "
                               f"{hands[winner]}")
        self.next_game()
