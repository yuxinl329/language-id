wimport math, random
import glob

################################################################################
# Part 0: Utility Functions
################################################################################

LANGUAGE_CODES = []

def create_language_code():
    with codecs.open('./data/train/train_labels.txt', 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            LANGUAGE_CODES.add(line[:3])

def start_pad(n):
    ''' Returns a padding string of length n to append to the front of text
        as a pre-processing step to building n-grams '''
    return '~' * n

def ngrams(n, text):
    ''' Returns the ngrams of the text as tuples where the first element is
        the length-n context and the second is the character '''
    input = start_pad(n) + text
    ngrams = []
    for i in range(0, len(input) - n):
        ngrams.append((input[i : i + n], input[i + n]))
    return ngrams

def create_ngram_model(model_class, path, n=2, k=0):
    ''' Creates and returns a new n-gram model trained on the city names
        found in the path file '''
    model = model_class(n, k)
    with open(path, encoding='utf-8', errors='ignore') as f:
        model.update(f.read())
    return model

def create_ngram_model_lines(model_class, path, n=2, k=0):
    ''' Creates and returns a new n-gram model trained on the city names
        found in the path file '''
    model = model_class(n, k)
    with open(path, encoding='utf-8', errors='ignore') as f:
        for line in f:
            model.update(line.strip())
    return model

################################################################################
# Part 1: Basic N-Gram Model
################################################################################

class NgramModel(object):
    ''' A basic n-gram model using add-k smoothing '''

    def __init__(self, n, k):
        self.n = n
        self.k = k
        self.ngrams = {}

    def get_vocab(self):
        ''' Returns the set of characters in the vocab '''
        vocab = set()
        for i in self.ngrams.keys():
            if i[1] not in vocab:
                vocab.add(i[1])
        return vocab

    def update(self, text):
        for (a, b) in ngrams(self.n, text):
            if (a, b) in self.ngrams.keys():
                self.ngrams[(a, b)] = self.ngrams[(a, b)] + 1
            else: 
                self.ngrams[(a, b)] = 1;

    def prob(self, context, char):
        ''' Returns the probability of char appearing after context '''
        size = len(self.get_vocab()) * 1.0
        countContext = 0.0
        countMatch = 0.0

        for (a, b) in self.ngrams.keys():
            if a == context:
                countContext += float(self.ngrams[(a, b)])
                if b == char:
                    countMatch += float(self.ngrams[(a, b)])
        if countContext == 0:
            return 1.0 / size
        else:
            return (float(countMatch) + self.k) / (float(countContext) + size * self.k)

    def perplexity(self, text):
        ''' Returns the perplexity of text based on the n-grams learned by
            this model '''
        pad = '~' * max(0, self.n - len(text))
        pad_text = pad + text

        x = 0.0
        for i in range(0, len(text)):
            currContext = start_pad(self.n - i) + pad_text[0:i]
            currContext = currContext[len(currContext)-self.n:len(currContext)]
            currChar = pad_text[i]
            p = self.prob(currContext, currChar)
            if p == 0:
                return float('inf')
            else: 
                x += math.log10(1 / p)
        return pow(10, x / len(text))

################################################################################
# Part 3: Your N-Gram Model Experimentation
################################################################################

if __name__ == '__main__':
    create_language_code()
    
    models = []
    labels = []
    
    for language in LANGUAGE_CODES:
        m = NgramModel(1, 1)
        filename = '.data/train/languages/' + LANGUAGE_CODE '.txt'
        with codecs.open(filename, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                m.update(line)
        models.add(m)

    print('Model Training Complete')

    with codecs.open('./data/test/test_sentences.txt', 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            probability = []
            for m in models:
                probabilty.add(m.prob(line))
            index = probability.index(max(probability))
            labels.add(LANGUAGE_CODE[index])

    count = 0
    correct = 0
    with codecs.open('./data/test/test_labels.txt', 'r', encoding='utf-8', errors='ignore') as f:
        for line in f:
            if line == labels[count]:
                correct += 1
            count += 1

    print(float("%0.2f" % (correct / count)))
