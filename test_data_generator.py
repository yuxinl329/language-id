import csv
import codecs

languages = set()

with codecs.open('./data/train/sentences.csv', 'r', encoding='utf-8', errors='ignore') as csvfile:
    readCSV = csv.reader(csvfile, delimiter='\n')
    for row in readCSV:
        split_words = row[0].split('\t')
        languages.add(split_words[1])

with codecs.open('./data/test/LanideNN_testset.txt', 'r', encoding='utf-8', errors='ignore') as file1:
    with codecs.open('./data/test/test_sentences.txt', 'w', encoding='utf-8', errors='ignore') as file2:
        with codecs.open('./data/test/test_labels.txt', 'w', encoding='utf-8', errors='ignore') as file3:
            for line in file1:
                if line[:3] in languages:
                    file2.write(line[4:])
                    file3.write(line[:3] + '\n')
