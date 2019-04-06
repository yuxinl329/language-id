import csv
import codecs

languages = set()
count = 0

with codecs.open('./data/train/sentences.csv', 'r', encoding='utf-8', errors='ignore') as csvfile:
    readCSV = csv.reader(csvfile, delimiter='\t')
    for row in readCSV:
        count += 1
        if (row[1] != '\\N') and (row[1] != 'toki') and (row[1] != 'cycl'):
            languages.add(row[1])
            filename = './data/train/languages/' + row[1] + '.txt'
            with codecs.open(filename, 'a', encoding='utf-8', errors='ignore') as file:
                file.write(row[2] + '\n')

        num = float("%0.2f" % (count / 7429494 * 100))
        if (count % 50000 == 0):
            print(str(num) + '%')

with codecs.open('./data/train/train_labels.txt', 'w', encoding='utf-8', errors='ignore') as f:
    for l in languages:
        f.write(l + '\n')
