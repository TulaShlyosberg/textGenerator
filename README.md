# textGenerator

## Описание
Проект состоит из двух файлов train.py и generate.py

### train.py

Запустите в командной строке файл train.py, чтобы обучить генератор на определенном корпусе текстов. При этом используются аргументы:

*--model* - имя файла, куда записываеся модель  
*--lc* - приводит текст к нижнему регистру  
*--input-dir* - каталог с текстами для обучения  
*--N* - количество слов в N-грамме  

Вероятность следования за данными *N* словами следущего определяется как вероятность встерить данное слово после данных *N* слов в текстах для обучения

### generate.py

Запустите в командной строке generate.py, чтобы сгенирировать текст, с аргументами:

*--model* - имя файла, куда записывалась модель  
*--seed* - начальное слово  
*--length* - количество слов в тексте  
*--output* - имя файла, куда записывается результат (при отстутствии выводится в консоль)  