import nltk
import sys
import re
import math
from nltk.tokenize import word_tokenize

def clean(corpus):
    cleaned_corpus = corpus.lower()
    cleaned_corpus = re.sub(' +', ' ', cleaned_corpus)
    cleaned_corpus = re.sub('-+', ' ', cleaned_corpus)
    cleaned_corpus = re.sub('[^a-zA-Z \n]+', '', cleaned_corpus)

    return cleaned_corpus


def sentencizer(text):
    temp = text.split("\n")

    sentences = []

    for s in temp:
        if s.strip():
            sentences.append(s.strip())
            # sentences.append("$ " + s.strip() + " #")

    return sentences

def get_unigrams(sentences):
    unigrams = {}

    for sentence in sentences:
        for word in sentence:

            if word not in unigrams:
                unigrams[word] = 1

            else:
                unigrams[word] += 1

    return unigrams


def get_bigrams(sentences):
    bigrams = {}

    for sentence in sentences:
        length = len(sentence)

        for i in range(length - 1):
            if sentence[i] not in bigrams:
                bigrams[sentence[i]] = {}

            if sentence[i+1] not in bigrams[sentence[i]]:
                bigrams[sentence[i]][sentence[i+1]] = 1

            else:
                bigrams[sentence[i]][sentence[i+1]] += 1

    return bigrams


def get_trigrams(sentences):
    trigrams = {}

    for sentence in sentences:
        length = len(sentence)

        for i in range(length - 2):
            if sentence[i] not in trigrams:
                trigrams[sentence[i]] = {}

            if sentence[i+1] not in trigrams[sentence[i]]:
                trigrams[sentence[i]][sentence[i+1]] = {}

            if sentence[i+2] not in trigrams[sentence[i]][sentence[i+1]]:
                trigrams[sentence[i]][sentence[i+1]][sentence[i+2]] = 1

            else:
                trigrams[sentence[i]][sentence[i+1]][sentence[i+2]] += 1

    return trigrams

def get_quadgrams(sentences):
    quadgrams = {}

    for sentence in sentences:
        length = len(sentence)

        for i in range(length - 3):
            if sentence[i] not in quadgrams:
                quadgrams[sentence[i]] = {}
            if sentence[i+1] not in quadgrams[sentence[i]]:
                quadgrams[sentence[i]][sentence[i+1]] = {}
            if sentence[i+2] not in quadgrams[sentence[i]][sentence[i+1]]:
                quadgrams[sentence[i]][sentence[i+1]][sentence[i+2]] = {}
            if sentence[i+3] not in quadgrams[sentence[i]][sentence[i+1]][sentence[i+2]]:
                quadgrams[sentence[i]][sentence[i+1]][sentence[i+2]][sentence[i+3]] = 1
            else:
                quadgrams[sentence[i]][sentence[i+1]][sentence[i+2]][sentence[i+3]] += 1

    return quadgrams

def unigram_vocabulary(unigrams):
    return len(unigrams)


def total_unigrams(unigrams):
    cnt = 0

    for i in unigrams:
        cnt += unigrams[i]

    return cnt


def bigram_vocabulary(bigrams):
    cnt = 0

    for i in bigrams:
        cnt += len(bigrams[i])

    return cnt


def trigram_vocabulary(trigrams):
    cnt = 0

    for i in trigrams:
        for j in trigrams[i]:
            cnt += len(trigrams[i][j])

    return cnt

def quadgram_vocabulary(quadgrams):
    cnt = 0

    for i in quadgrams:
        for j in quadgrams[i]:
            for k in quadgrams[i][j]:
                cnt += len(quadgrams[i][j][k])
    
    return cnt

def kneser_ney_trigrams(quadgrams, tokenized_inp, unigrams, bigrams):
    d = 0.75        
    cur = 0

    vocabulary = trigram_vocabulary(trigrams)
    bi_vocabulary = bigram_vocabulary(bigrams)
    uni_vocabulary = unigram_vocabulary(unigrams)
    tot_unigrams = total_unigrams(unigrams)

    for sentence in tokenized_inp:
        length = len(sentence)

        for i in range(3, length):
            if sentence[i-2] not in unigrams:
                prob = (d/tot_unigrams)*(uni_vocabulary/vocabulary)
                cur += math.log(prob)

            elif sentence[i-1] not in unigrams:
                prob = (d/tot_unigrams)*(uni_vocabulary/vocabulary)
                cur += math.log(prob)

            elif sentence[i-1] not in bigrams[sentence[i-2]]:
                prob = (d/tot_unigrams)*(uni_vocabulary/vocabulary)
                cur += math.log(prob)

            else:
                cnt = 0

                if sentence[i] in quadgrams[sentence[i-3]][sentence[i-2]][sentence[i-1]]:
                    cnt = max(quadgrams[sentence[i-3]][sentence[i-2]][sentence[i-1]][sentence[i]] - d, 0)

                den = trigrams[sentence[i-3]][sentence[i-2]][sentence[i-1]]

                p0 = cnt/den

                lambda0 = ((d/trigrams[sentence[i-3]][sentence[i - 2]][sentence[i - 1]]) *
                           len(quadgrams[sentence[i-3]][sentence[i - 2]][sentence[i - 1]]))

                cnt = 0

                if sentence[i] in trigrams[sentence[i-2]][sentence[i-1]]:
                    cnt = max(trigrams[sentence[i-2]][sentence[i-1]][sentence[i]] - d, 0)

                den = bigrams[sentence[i-2]][sentence[i-1]]

                p = cnt/den

                lambda1 = ((d/bigrams[sentence[i - 2]][sentence[i - 1]]) *
                           len(trigrams[sentence[i - 2]][sentence[i - 1]]))
                tot1 = 0
                tot1_den = 0

                for j in trigrams:
                    if sentence[i - 1] in trigrams[j]:
                        if sentence[i] in trigrams[j][sentence[i - 1]]:
                            tot1 += 1

                        tot1_den += len(trigrams[j][sentence[i - 1]])

                p2 = max(tot1 - d, 0)/tot1_den

                lambda2 = ((d/unigrams[sentence[i - 1]]) * len(bigrams[sentence[i - 1]]))

                tot2 = 0

                for j in bigrams:
                    if sentence[i] in bigrams[j]:
                        tot2 += 1

                p3 = max(tot2 - d, 0)/bi_vocabulary
                lambda3 = ((d/tot_unigrams)*uni_vocabulary)
                p3 += lambda3/uni_vocabulary
                print(p3)
                p2 += lambda2*p3
                p += lambda1*p2
                p0 += lambda0*p

                cur += math.log(p)

    return math.exp(cur)

n = sys.argv[1]
type = sys.argv[2]
path = sys.argv[3]

file = open(path)
corpus = file.read()
cleaned_corpus = clean(corpus)
sentences = sentencizer(cleaned_corpus)
print (sentences)
# print(sentences)
sentences = [nltk.word_tokenize(s) for s in sentences]
# print (sentences)

unigrams = get_unigrams(sentences)
bigrams = get_bigrams(sentences)
trigrams = get_trigrams(sentences)
quadgrams = get_quadgrams(sentences)
# print(quadgrams)
# print(trigrams)

# print(unigrams)
# print()
# print(bigrams)
# print()
# print(trigrams)

print("input sentence:", end=" ")
senti = input()

sent = []

senti = clean(senti)
if senti.strip():
    sent.append(senti.strip())
print(sent)
# sent = sentencizer(sent)
sent = [nltk.word_tokenize(s) for s in sent]
print (sent)

# print(sent)
if sent:

    # if n == "1" and type == "k":
    #     print(kneser_ney_unigrams(unigrams, sent))

    # elif n == "2" and type == "k":
    #     print(kneser_ney_bigrams(bigrams, sent, unigrams))

    # elif n == "3" and type == "k":
    print(kneser_ney_trigrams(quadgrams, sent, unigrams, bigrams))

    # elif n == "1" and type == "w":
    #     print(witten_bell_unigrams(unigrams, sent))

    # elif n == "2" and type == "w":
    #     print(witten_bell_bigrams(bigrams, sent, unigrams))

    # elif n == "3" and type == "w":
    #     print(witten_bell_trigrams(trigrams, sent, unigrams, bigrams))
