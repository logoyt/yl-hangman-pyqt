# Виселица

## Правила
Пользователь выбирает категорию, ему из этой категории загадывается слово.
Чтобы угадать слово, нужно открыть в нём все буквы. 
Сначала пользователь видит только количество букв в слове, спустя три ошибки появляется подсказка.
Всего 10 попыток.

## Запускать нужно main.py. Появится меню:
1. Начать игру
    диалоговое окно предложит выбрать категорию, после чего начнётся игра.
2. Добавить слово
    добавляет в базу данных слово, которое введёт пользователь.
    если указанной категории раньше не было, она будет создана.
3. Открыть таблицу слов
    открывается таблица всех слов, категорий и подсказок

## Файлы
db.py - база данных
game.py - сама игра. можно запускать отдельно
main.py - меню, описанное выше
utility.py - вспомогательный код
words_table.py - таблица слов

337 строчек кода.

Enjoy