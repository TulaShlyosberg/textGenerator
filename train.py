import os
import argparse
import sys
from collections import defaultdict
from collections import deque


# Процедура, удаляющая неалфавитные символы, могущие приклеиться к слову
def delete_not_alphabet(word):
    non_alphabet_symb = {'—', '.', ',', ':', '-', ';',
                         '!', '?', '%', ']', '[', '(', 
                         ')', '…', '[', '#', '@', '&', 
                         '$'}
    while word[-1] in non_alphabet_symb or word[-1].isdigit():
        word = word[:-1]
        if word == '':
            return word
    while word[0] in non_alphabet_symb or word[-1].isdigit():
        word = word[1:]
        if word == '':
            return word
    return word


# возвращает True, если word слово или два слова через дефис
def is_word(word):
    if word == '':
        return False
    if word.isalpha():
        return True
    hyphen = word.split('-')
    if len(hyphen) == 2 and hyphen[0].isalpha() and hyphen[1].isalpha():
        return True
    return False


# Процедура, обновляющая модель
def update_model(frequency, sum, s, lc, N):
    if lc:
        s = s.lower()
    words = s.split()
    window = ('',)*N  # ключ-N-грамма
    for word in words:        
        word = word.strip()
        word = delete_not_alphabet(word)  # Очищаем от неалфавитных символов
        if is_word(word):
            # Корректируем частоты
            if window[0] != '':
                sum[window] += 1
                frequency[window][word] += 1
                for i in range(1,N):
                    gramm = window[:i]
                    sum[gramm] += 1
                    frequency[gramm][window[i]] += 1
            window = window[1:] + (word,)


# Процедура, записывающая модель в файл
def write_model(filename, frequency, sum, N):
    with open(filename, "w") as model:
        model.write("{}\n".format(N))
        for key, record in frequency.items():
            model.write('&' + '_'.join(key) + '#' + str(sum[key]) + '\n')
            for j in record.keys():
                # Пары слово-частота разделяем собакой
                # А частоту от слова - решеткой
                model.write(j + '#' + str(record[j]) + '@')
            model.write('\n')


# Читаем аргументы программы из командной строки
def get_arguments():    
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', help='путь к файлу, в который сохраняется модель', required=True)
    parser.add_argument('--lc', action='store_true', help='привести текст к нижнему регистру')
    parser.add_argument('--input-dir', action='store', nargs='?', 
                       const = '', default='', help='каталог с текстом для обучения')
    parser.add_argument('--N', required=True, type=int, help='количество слов в N-грамме')
    return parser.parse_args()


def main():    
    args = get_arguments()
    N = args.N

    # Словарь, каждой N-грамме сопоставляющий словарь из пар
    # последователь-количество встреч последователя после данной N-граммы
    frequency = defaultdict(lambda : defaultdict(int))

    # Количество встреч данной N-граммы
    sum = defaultdict(int)
    # Если аргументы --input-dir не заданы, считываем из консоли
    if (args.input_dir == ''):
        for s in sys.stdin:
            update_model(frequency, sum, s, args.lc, N)
    else:
        input_dir = os.listdir(args.input_dir) # Все вложенные файлы и директории помещаем в список
        for file_name in input_dir:
            path = os.path.join(args.input_dir, file_name)
            if os.path.isfile(path):
                with open(path, 'r') as fin:
                    for s in fin:
                        update_model(frequency, sum, s, args.lc, N)

    # Записываем модель
    write_model(args.model, frequency, sum, N)


if __name__ == '__main__':
    main()
