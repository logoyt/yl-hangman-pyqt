files = [
    'db',
    'game',
    'main',
    'utility',
    'words_table'
]

total = 0
for file in files:
    count = 0
    with open(f'{file}.py') as f:
        for line in f:
            if line.strip():
                if not line.strip().startswith('#'):
                    count += 1
    if file == 'db': # вычитаю словарь слов
        count -= 15
        print(f'{file}-15', count)
    else:
        print(file, count)
    total += count
print(f'{total=}')

'''
db-15 172
game 76
main 70
utility 13
words_table 34
total=365
'''
