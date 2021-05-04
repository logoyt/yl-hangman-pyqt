import re

ALPHABET = ''.join([chr(i) for i in range(ord('А'), ord('Я') + 1)])


class Singleton(type):
    _instances = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


def clear_word(word):
    if word:
        word = word.split()[0].lower().replace('ё', 'е')
        word = re.sub('[^а-я]+', '', word)
    return word
