import csv
import codecs

languages = set()

with codecs.open('sentences.csv', 'r', encoding='utf-8', errors='ignore') as csvfile:
    readCSV = csv.reader(csvfile, delimiter='\n')
    for row in readCSV:
        split_words = row[0].split('\t')
        languages.add(split_words[1])

with codecs.open('LanideNN_testset.txt', 'r', encoding='utf-8', errors='ignore') as file1:
    with codecs.open('testSet.txt', 'w', encoding='utf-8', errors='ignore') as file2:
        for line in file1:
            if line[:3] in languages:
                file2.write(line)
            elif line[:3] == 'zho':
                file2.write('cmn' + line[3:])

