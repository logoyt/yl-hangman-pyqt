import sqlite3
import os
import random as r

from utility import *

CREATE_THEMES = '''
    CREATE TABLE themes (
        id INTEGER PRIMARY KEY,
        name VARCHAR
    )
'''

CREATE_WORDS = '''
    CREATE TABLE words (
        id INTEGER PRIMARY KEY,
        word VARCHAR,
        hint VARCHAR
    )
'''

CREATE_WORDS_TO_THEMES = '''
    CREATE TABLE words_to_themes (
        id INTEGER PRIMARY KEY,
        theme INTEGER REFERENCES themes(id),
        word INTEGER REFERENCES words(id)
    )
'''

INSERT = '''
    INSERT INTO {table} {columns}
    VALUES {data}
'''

GET_WORDS_BY_THEME = """
    SELECT w.word, w.hint, t.name
    FROM words as w
    INNER JOIN words_to_themes as wt
        on w.id = wt.word
    INNER JOIN themes as t
        on wt.theme = t.id
    WHERE t.name = '{theme}'
"""

GET_ALL_WORDS = """
    SELECT w.word, w.hint, t.name
    FROM words as w
    INNER JOIN words_to_themes as wt
        on w.id = wt.word
    INNER JOIN themes as t
        on wt.theme = t.id
"""

CREATE_TABLES = [
    CREATE_THEMES,
    CREATE_WORDS,
    CREATE_WORDS_TO_THEMES,
]

BASIC_WORDS = {
    'программирование': [
        ('рекурсия', 'матрёшка'),
        ('полиморфизм', 'принцип ООП'),
        ('наследование', 'принцип ООП'),
        ('инкапсуляция', 'принцип ООП'),
    ],
    'американские сериалы': [
        ('менталист', 'Патрик Джейн'),
        ('сообщество', 'ситком о студенчестве'),
        ('воздействие', 'современные Робин Гуды'),
        ('клиника', 'лучший медицинский ситком на планете'),
        ('ведьмак', 'основан на серии польских романов'),
        ('люцифер', 'повелитель Ада в Лос-Анджелесе'),
    ],
}


class Database(metaclass=Singleton):
    _PATH = 'words_db.sqlite'
    def __init__(self):
        if os.path.exists(self._PATH):
            self.db = sqlite3.connect(self._PATH)
        else:
            self.db = sqlite3.connect(self._PATH)
            self.create_new_db()

    def commit(self):
        self.db.commit()

    def close(self, save=True):
        if save:
            self.commit()
        self.db.close()

    def create_new_db(self):
        cur = self.db.cursor()
        for query in CREATE_TABLES:
            cur.execute(query)
        self.fill(BASIC_WORDS)

    def fill(self, dict_):
        cur = self.db.cursor()

        # добавляем темы
        columns = '(name)'
        themes = ', '.join([f"('{theme}')" for theme in dict_.keys()])
        query = INSERT.format(
            table='themes', columns=columns,
            data=themes
        )
        # print(query)
        cur.execute(query)

        # добавляем слова
        columns = '(word, hint)'
        words = []
        for theme in dict_.keys():
            words.extend(dict_.get(theme))
        query = INSERT.format(
            table='words', columns=columns,
            data=str(words)[1:-1]
        )
        # print(query)
        cur.execute(query)

        # соединяем слова и темы
        for theme in dict_.keys():
            theme_id = self.get_theme_id(theme)
            for word in dict_.get(theme):
                word_id = self.get_word_id(word)
                query = INSERT.format(
                    table='words_to_themes', columns='(theme, word)',
                    data=f"('{theme_id}', '{word_id}')"
                )
                cur.execute(query)

        self.commit()

    def get_theme_id(self, theme):
        cur = self.db.cursor()
        theme_id = cur.execute(f"""
            SELECT id FROM themes
            WHERE name = '{theme}'
        """).fetchone()[0]
        return theme_id

    def get_word_id(self, word):
        cur = self.db.cursor()
        word_id = cur.execute(f"""
            SELECT id FROM words
            WHERE word = '{word[0]}'
        """).fetchone()[0]
        return word_id

    def get_themes(self):
        cur = self.db.cursor()
        themes = cur.execute(f"""
            SELECT name FROM themes
        """).fetchall()
        return [theme[0] for theme in themes]

    def get_random_theme(self):
        return r.choice(self.get_themes())

    def get_words(self, theme=None):
        cur = self.db.cursor()

        if theme not in self.get_themes():
            theme = self.get_random_theme()

        words = cur.execute(
            GET_WORDS_BY_THEME.format(theme=theme)
        ).fetchall()

        return words

    def get_all_words(self):
        cur = self.db.cursor()

        words = cur.execute(
            GET_ALL_WORDS
        ).fetchall()

        return words

    def get_random_word(self, theme=None):
        return r.choice(self.get_words(theme))

    def add_theme(self, theme):
        theme = clear_word(theme)
        if not theme:
            return
        if theme not in self.get_themes():
            cur = self.db.cursor()
            query = INSERT.format(
                table='themes', columns='(name)',
                data=f"('{theme}')"
            )
            cur.execute(query)
            self.commit()

    def add_word(self, theme, word, hint):
        theme = clear_word(theme)
        self.add_theme(theme)
        word = clear_word(word)
        if not word:
            return
        words = [word_[0] for word_ in self.get_all_words()]
        if word not in words:
            cur = self.db.cursor()
            query = INSERT.format(
                table='words', columns='(word, hint)',
                data=f"('{word}', '{hint}')"
            )
            cur.execute(query)
            theme_id = self.get_theme_id(theme)
            word_id = self.get_word_id((word, ))
            query = INSERT.format(
                table='words_to_themes', columns='(theme, word)',
                data=f"('{theme_id}', '{word_id}')"
            )
            cur.execute(query)
            self.commit()


if __name__ == "__main__":
    Database()
