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
                    if not line.strip().startswith('import'):
                        if not line.strip().startswith('from'):
                            count += 1
    if file == 'db': # вычитаю словарь слов
        count -= 15
        print(f'{file}-15', count)
    else:
        print(file, count)
    total += count
print(f'{total=}')

'''
db-15 168
game 68
main 61
utility 12
words_table 28
total=337
'''
