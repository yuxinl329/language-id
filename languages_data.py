import csv
import codecs

languages = set()
count = 0

with codecs.open('sentences.csv', 'r', encoding='utf-8', errors='ignore') as csvfile:
    readCSV = csv.reader(csvfile, delimiter='\n')
    for row in readCSV:
        count += 1
        split_words = row[0].split('\t')
        languages.add(split_words[1])
        filename = './languages/' + split_words[1] + '.txt'
        with codecs.open(filename, 'a', encoding='utf-8', errors='ignore') as file:
            file.write(split_words[2] + '\n')
        num = float("%0.2f" % (count / 7429494 * 100))
        if (count % 50000 == 0):
            print(str(num) + '%')
