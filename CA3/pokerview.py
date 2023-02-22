from PyQt5.QtGui import *
from PyQt5.QtSvg import *
from PyQt5.QtWidgets import *
import playermodel as pm


class TableScene(QGraphicsScene):
    """ A scene with a table cloth background """

    def __init__(self):
        super().__init__()
        self.tile = QPixmap('cards/table.png')
        self.setBackgroundBrush(QBrush(self.tile))


class CardItem(QGraphicsSvgItem):
    """ A simple overloaded QGraphicsSvgItem that also stores the card position """

    def __init__(self, renderer, position):
        super().__init__()
        self.setSharedRenderer(renderer)
        self.position = position


def read_cards():
    """
    Reads all the 52 cards from files.
    :return: Dictionary of SVG renderers
    """
    all_cards = dict()  # Dictionaries let us have convenient mappings between cards and their images
    for suit_file, suit in zip('HSCD', range(1, 5)):  # Check the order of the suits here!!!
        for value_file, value in zip(['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A'], range(2, 15)):
            file = value_file + suit_file
            key = (value, suit)  # I'm choosing this tuple to be the key for this dictionary
            all_cards[key] = QSvgRenderer('cards/' + file + '.svg')
    return all_cards


class CardView(QGraphicsView):
    """ A View widget that represents the table area displaying a players cards. """

    # We read all the card graphics as static class variables
    back_card = QSvgRenderer('cards/Red_Back_2.svg')
    all_cards = read_cards()

    def __init__(self, card_model: pm.CardModel, card_spacing: int = 250, padding: int = 10):
        """
        Initializes the view to display the content of the given model
        :param pm.cards_model: A model that represents a set of cards. Needs to support the CardModel interface.
        :param card_spacing: Spacing between the visualized cards.
        :param padding: Padding of table area around the visualized cards.
        """
        self.scene = TableScene()
        super().__init__(self.scene)

        self.card_spacing = card_spacing
        self.padding = padding
        self.model = card_model
        card_model.new_cards.connect(self.change_cards)
        self.change_cards()

    def change_cards(self):
        # Add the cards from scratch
        self.scene.clear()
        for i, card in enumerate(self.model):
            # The ID of the card in the dictionary of images is a tuple with (value, suit), both integers
            graphics_key = (card.get_value(), card.suit.value)
            renderer = self.back_card if self.model.flipped() else self.all_cards[graphics_key]
            c = CardItem(renderer, i)

            # Shadow effects are cool!
            shadow = QGraphicsDropShadowEffect(c)
            shadow.setBlurRadius(10.)
            shadow.setOffset(5, 5)
            shadow.setColor(QColor(0, 0, 0, 180))  # Semi-transparent black!
            c.setGraphicsEffect(shadow)

            # Place the cards on the default positions
            c.setPos(c.position * self.card_spacing, 0)
            self.scene.addItem(c)

        self.update_view()

    def update_view(self):
        scale = (self.viewport().height() - 2 * self.padding) / 313
        self.resetTransform()
        self.scale(scale, scale)
        # Put the scene bounding box
        self.setSceneRect(-self.padding // scale, -self.padding // scale,
                          self.viewport().width() // scale, self.viewport().height() // scale)

    def resizeEvent(self, painter):
        # This method is called when the window is resized.
        # If the widget is resize, we gotta adjust the card sizes.
        # QGraphicsView automatically re-paints everything when we modify the scene.
        self.update_view()
        super().resizeEvent(painter)


class PlayerView(QWidget):
    """A widget view ara representing the players content"""
    def __init__(self, player: pm.HandModel):
        super().__init__()
        """Initializes the content which to display
        :param player: A player object with set attributes
        """

        player_info = QGroupBox("PLAYER")
        self.player = player
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()

        self.money = QLabel(f"{player.money}")
        self.bet = QLabel(f"Bet: {player.total_bet}")

        # Adds all widgets to the vertical box in correct order
        vbox.addWidget(CardView(player.hand))
        vbox.addWidget(QLabel(player.name))
        vbox.addWidget(self.money)
        vbox.addWidget(self.bet)

        player_info.setLayout(vbox)
        hbox.addWidget(player_info)

        self.setLayout(hbox)
        self.setMinimumWidth(600)
        self.player.update_data.connect(self.update)
        self.update()

    def update(self):
        """Updates the displayed values based on changes during the game"""
        self.money.setText(f"{self.player.money}")
        self.bet.setText(f"Bet: {self.player.total_bet}")


class ChoiceView(QWidget):
    """Widget representing the choice view"""
    def __init__(self, game_model: pm.GameState):
        super().__init__()
        """Initializes the choice view by using a model as support
        :param game_model: A game model representing a Texas Hold'em game
        """
        self.model = game_model
        self.player = self.model.players[self.model.player_turn]

        vbox = QVBoxLayout()
        self.current_player = QLabel(f"Current player: {self.player.name}")
        self.pot_label = QLabel(f"Pot: {self.model.pot}")

        # Creates all the different buttons
        flip_button = QPushButton("Flip cards")
        call_button = QPushButton("Call")
        bet_button = QPushButton("Bet")
        fold_button = QPushButton("Fold")

        # Connects all buttons to each corresponding function
        flip_button.clicked.connect(self.flip)
        call_button.clicked.connect(self.call)
        bet_button.clicked.connect(self.bet)
        fold_button.clicked.connect(self.fold)

        # Adds all buttons and labels to the vertical box layout
        vbox.addWidget(flip_button)
        vbox.addWidget(call_button)
        vbox.addWidget(bet_button)
        vbox.addWidget(fold_button)
        vbox.addWidget(self.current_player)
        vbox.addWidget(self.pot_label)

        self.setLayout(vbox)

    def flip(self):
        """Connects the flip button to the model"""
        self.model.players[self.model.player_turn].hand.flip()

    def call(self):
        """Connects the call button to the model and updates the view"""
        self.model.call()
        self.update()

    def bet(self):
        """Connects the bet button to the model and updates the view"""
        bet, ok = QInputDialog.getInt(self.parent(), "Bet amount", "")
        self.model.bet(bet)
        self.update()

    def fold(self):
        """Connects the call button to the model and updates the view"""
        self.model.fold()
        self.update()

    def update(self):
        """Updates the views"""
        self.player = self.model.players[self.model.player_turn]
        self.pot_label.setText(f"Pot: {self.model.pot}")
        self.current_player.setText(f"Current player: {self.player.name}")


class GameView(QWidget):
    """Widget displaying the whole game view with two players"""
    def __init__(self, model: pm.GameState):
        super().__init__()
        """Initializes the game view for two players
        :param model: The game model representing Texas Hold'em
        """
        self.model = model
        game_box = QGroupBox()
        vbox = QVBoxLayout()
        hbox = QHBoxLayout()
        self.flop = CardView(self.model.flop)

        # Adds two players and the flop in the correct order
        hbox.addWidget(PlayerView(self.model.players[0]))
        hbox.addWidget(ChoiceView(self.model))
        hbox.addWidget(PlayerView(self.model.players[1]))

        # Sets the correct layouts
        game_box.setLayout(hbox)
        vbox.addWidget(game_box)
        vbox.addWidget(self.flop)
        self.setLayout(vbox)

        self.model.game_message.connect(self.alert_user)
        self.model.update_state.connect(self.update)

    @staticmethod
    def alert_user(text):
        """Alerts the user with a popup message-box"""
        box = QMessageBox()
        box.setText(text)
        box.exec_()

    def update(self):
        """Updates the flop when new cards are added"""
        self.flop.update_view()
