from PyQt5 import QtWidgets, uic
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem, QDialog, QInputDialog
import sys

from db import Database
from game import Game
from utility import *
from words_table import TableWords


class Menu(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/menu.ui', self)
        self.start.clicked.connect(self.game_start)
        self.add_word.clicked.connect(self.word_add)
        self.quit.clicked.connect(self.exit)
        self.open_table.clicked.connect(self.table_open)

    def game_start(self):
        self.clear_statusBar()
        theme = DialogStart().run()
        if theme:
            word = Database().get_random_word(theme)
            self.game = Game(self, word)
            self.game.show()
            self.hide()

    def word_add(self):
        self.clear_statusBar()
        theme, word, hint = DialogAddWord().run()
        if theme and word:
            Database().add_word(theme, word, hint)
        else:
            self.statusBar().showMessage('Не удалось добавить слово')

    def clear_statusBar(self):
        self.statusBar().showMessage('')

    def exit(self):
        Database().close()
        sys.exit()

    def table_open(self):
        self.clear_statusBar()
        self.table = TableWords(self)
        self.table.show()
        self.hide()


class DialogStart(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/dialog-start.ui', self)
        themes = ['случайная'] + Database().get_themes()
        self.themes.addItems(themes)

    def run(self):
        if self.exec_() == QDialog.Accepted:
            theme = self.themes.currentText()
            return theme


class DialogAddWord(QDialog):
    def __init__(self):
        super().__init__()
        uic.loadUi('ui/dialog-add-word.ui', self)
        themes = Database().get_themes()
        self.themes.addItems(themes)

    def run(self):
        if self.exec_() == QDialog.Accepted:
            theme = clear_word(self.themes.currentText())
            word = clear_word(self.word.text())
            hint = self.hint.text()
            return theme, word, hint
        return None, None, None


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Menu()
    win.show()
    # win.close()
    sys.exit(app.exec_())
