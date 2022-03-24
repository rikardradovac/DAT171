import pokerview as pw
import playermodel as pm
from PyQt5.QtWidgets import *
import sys

# This program is used to start the Texas Hold'em game pokerview and pokermodel

app = QApplication(sys.argv)

box = QVBoxLayout()
box.addWidget(pw.GameView(pm.GameState()))
game_view = QGroupBox()

game_view.setLayout(box)
game_view.show()

app.exec_()
