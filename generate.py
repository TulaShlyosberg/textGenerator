import argparse
import numpy as np


# Считываем модель из файла
def read_model(filename):
    # Словарь N-грамма - вероятности всех ее последователей
    probability = dict()
    with open(filename, "r") as model:
        N = int(model.readline())
        keys = [dict()]*N    # i-ый словарь - начало некоторой (i+1)-граммы, N-ый - сами N-граммы
        for line in model:
            if line[0] == '&':
                key, sum = line[1:].split('#')
                key = tuple(key.split('_'))
                index = len(key) - 1 
                keys[index][key] = list()
                probability[key] = list()
            else:
                # т.к. строка последователей заканчивается на @,
                # исключаем из списка split последний (пустой) элемент
                pairs = [ j.split('#') for j in line.split('@')][:-1]
                for pair in pairs:
                    keys[index][key].append(pair[0])
                    probability[key].append(float(pair[1])/float(sum))
    return keys, probability, N


 # Считываем аргументы программы
def get_arguments():   
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', action='store', help='файл модели', required=True)
    parser.add_argument('--seed', action='store', help='начальное слово')
    parser.add_argument('--length', action='store', help='длина последовательности',
                       type=int, required=True)
    parser.add_argument('--output', action='store', 
                         help='путь к файлу, куда записываем модель')
    return parser.parse_args()


# Генерируем строку на основе модели
def generate_result_string(keys, probability, N, seed, length):
    once_word_keys = [i[0] for i in keys[0].keys()]   # начала N-грамм
    if seed is None:
        first_word = np.random.choice(once_word_keys, 1)[0]
    else:
        first_word = seed
    result = ''

    window = ('',)*N
    # Для каждой N-граммы случайно выбираем ее последователя
    for i in range(length):
        window = window[1:] + (first_word,)
        result += first_word + ' '
        # Находим крайнее правое вхождение '' в window
        j = 0
        while j < N and window[j] == '':
            j += 1
        
        # Для i-граммы, i < N, случайно выбираем (i+1)-грамму, которая содержит эту i-грамму
        # Для N-граммы случайно выбираем последователя
        temp = window[j:]
        index = N - j - 1
        if temp in keys[index].keys():
            first_word = np.random.choice(keys[index][temp], 1, probability[temp])[0]
            continue
        # Если у N-граммы нет последователя, генерируем новое случайное слово
        window = ('',)*N
        first_word = np.random.choice(once_word_keys, 1)[0]
    return result


def main():
    args = get_arguments()
    keys, probability, N = read_model(args.model)
    result = generate_result_string(keys, probability, N, args.seed, args.length)

    # В зависимости от аргумента --output
    # Записываем результат в файл или консоль
    if args.output is not None:
        with open(args.output, 'w') as fout:
            fout.write(result)
    else:
        print(result)

if __name__ == '__main__':
    main()