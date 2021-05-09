from PyQt5 import QtWidgets, uic
from PyQt5.Qt import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5.QtWidgets import QTableWidgetItem, QHeaderView
import sys

from db import Database


class TableWords(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        uic.loadUi('ui/table-words.ui', self)
        self.parent = parent
        self.fill()

    def fill(self):
        words = Database().get_all_words()
        self.table.setRowCount(len(words))
        self.table.setColumnCount(len(words[0]))
        self.table.setHorizontalHeaderLabels([
            'Слово', 'Подсказка', 'Категория'
        ])
        for j, line in enumerate(words):
            for i, name in enumerate(line):
                self.table.setItem(j, i, QTableWidgetItem(str(name)))
        self.table.horizontalHeader().setSectionResizeMode(
            QHeaderView.ResizeToContents
        )
        
    def closeEvent(self, event):
        if self.parent:
            self.parent.show()
        event.accept()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = TableWords()
    win.show()
    # win.close()
    sys.exit(app.exec_())
