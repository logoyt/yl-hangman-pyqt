from PyQt5 import QtWidgets, uic
from PyQt5.Qt import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.QtWidgets import QTableWidgetItem
import sys

from db import Database
from utility import *

RED_BG = 'background-color: #ff8484'
GREEN_BG = 'background-color: #90ee90'

BUTTONS = {ALPHABET[i]: f'l{i + 1}' for i in range(len(ALPHABET))}


class Game(QMainWindow):
    _pic = 'resources/hangman{}.png' # 00-10
    _lives = 10
    def __init__(self, parent=None, word=None):
        if word not in Database().get_all_words():
            word = Database().get_random_word()
        super().__init__()
        uic.loadUi('ui/game.ui', self)
        self.parent = parent
        for button in BUTTONS.values():
            getattr(self, button).clicked.connect(self.press)
        self.lives = Game._lives

        self.secret_word = word[0].upper().replace('Ё', 'E')
        self.hint_text = word[1]
        self.guessed_word = '-' * len(word[0])
        
        self.theme.setText(f'Тема: {word[2]}')
        self.update()

    def update_pic(self):
        if self.lives not in range(0, Game._lives + 1):
            return
        pic_name = f'{Game._lives - self.lives:0>2}'
        pic = QPixmap(Game._pic.format(pic_name))
        self.pic_hangman.setPixmap(pic)

    def update_lives(self):
        text = f'Попыток осталось: {self.lives}'
        self.lives_left.setText(text)

    def update(self):
        self.update_pic()
        self.update_lives()
        self.word.setText(self.guessed_word)

        if self.guessed_word == self.secret_word or self.lives <= 0:
            for button in BUTTONS.values():
                getattr(self, button).setEnabled(False)
            if self.lives <= 0:
                self.result.setText('Вы проиграли :(')
            else:
                self.result.setText('Вы угадали слово, ура!')
            self.statusBar().showMessage('Закройте окно, чтобы вернуться в меню.')

    def closeEvent(self, event):
        if self.parent:
            self.parent.show()
        event.accept()

    def press(self):
        letter = self.sender().text()[0]
        if letter in self.secret_word:
            self.sender().setStyleSheet(GREEN_BG)
            self.reveal_letter(letter)
        else:
            self.sender().setStyleSheet(RED_BG)
            self.lives -= 1
            if Game._lives - self.lives == 3:
                self.reveal_hint()
        getattr(self, BUTTONS[letter]).setEnabled(False)
        self.update()

    def reveal_letter(self, letter):
        for i, l in enumerate(self.secret_word):
            if l == letter:
                self.guessed_word = self.guessed_word[:i] + letter + self.guessed_word[i+1:]

    def reveal_hint(self):
        self.hint.setText(self.hint_text)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = Game()
    win.show()
    # win.close()
    sys.exit(app.exec_())
