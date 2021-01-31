import nltk
import sys
import re
import math
# from nltk.tokenize import word_tokenize

def unigram_vocabulary(unigrams):
    return len(unigrams)


def total_unigrams(unigrams):
    cnt = 0

    for i in unigrams:
        cnt = unigrams[i] + cnt

    return cnt


def bigram_vocabulary(bigrams):
    cnt = 0

    for i in bigrams:
        cnt = len(bigrams[i]) + cnt

    return cnt


def trigram_vocabulary(trigrams):
    cnt = 0

    for i in trigrams:
        for j in trigrams[i]:
            cnt = len(trigrams[i][j]) + cnt

    return cnt

# def quadgram_vocabulary(quadgrams):
#     cnt = 0

#     for i in quadgrams:
#         for j in quadgrams[i]:
#             for k in quadgrams[i][j]:
#                 cnt = len(quadgrams[i][j][k]) + cnt
    
#     return cnt

#----------------------------------------------------------------------------------------------------------------

def kneser_ney_trigrams(quadgrams, input_sentence, unigrams, bigrams, trigrams):
    d = 0.75        
    cur = 0

    quad_vocabulary = 0
    for i in quadgrams:
        for i1 in quadgrams[i]:
            for i2 in quadgrams[i][i1]:
                quad_vocabulary +=len(quadgrams[i][i1][i2]) 
    # vocabulary = trigram_vocabulary(trigrams)
    bi_vocabulary = 0
    for i in bigrams:
        bi_vocabulary +=len(bigrams[i])

    uni_vocabulary = len(unigrams)
    
    tot_unigrams = 0
    for i in unigrams:
        tot_unigrams += unigrams[i]

    for sentence in input_sentence:
        # length = len(sentence)

        for i in range(3, len(sentence)):

            if sentence[i-1] in unigrams and sentence[i-2] in unigrams and sentence[i-3] in unigrams and sentence[i-1] in bigrams[sentence[i-2]] and sentence[i-2] in bigrams[sentence[i-3]] and sentence[i-1] in trigrams[sentence[i-3]][sentence[i-2]]:
            # else:
                tot1_den = 0

                tot2 = 0
                tot1 = 0

                if sentence[i] not in quadgrams[sentence[i-3]][sentence[i-2]][sentence[i-1]]:
                    p0 = 0
                else:
                    p0 = float(max(quadgrams[sentence[i-3]][sentence[i-2]][sentence[i-1]][sentence[i]] - d, 0)) / float(trigrams[sentence[i-3]][sentence[i-2]][sentence[i-1]])
                    print("22")
                    

                # den = trigrams[sentence[i-3]][sentence[i-2]][sentence[i-1]]

                # p0 = cnt/den

                lam0 = (float(d/trigrams[sentence[i-3]][sentence[i - 2]][sentence[i - 1]]) * float(len(quadgrams[sentence[i-3]][sentence[i - 2]][sentence[i - 1]])))

                if sentence[i] in trigrams[sentence[i-2]][sentence[i-1]]:
                    p = float(max(trigrams[sentence[i-2]][sentence[i-1]][sentence[i]] - d, 0)) / float(bigrams[sentence[i-2]][sentence[i-1]]) 
                    print("!1")
                else:
                    p = float(0)

                # den = bigrams[sentence[i-2]][sentence[i-1]]

                # p = cnt/den

                lam1 = (float(d/bigrams[sentence[i - 2]][sentence[i - 1]]) * float(len(trigrams[sentence[i - 2]][sentence[i - 1]])))
                
                
                for j in trigrams :
                    if sentence[i-1] in trigrams[j]:
                        tot1_den += len(trigrams[j][sentence[i - 1]])

                
                for j in trigrams:
                    if sentence[i - 1] in trigrams[j]:
                        if sentence[i] in trigrams[j][sentence[i - 1]]:
                            tot1 += 1

                        # tot1_den = len(trigrams[j][sentence[i - 1]]) + tot1_den
                

                p2 = float(max(tot1 - d, 0))/float(tot1_den)

                lam2 = (float(d/unigrams[sentence[i - 1]]) * float(len(bigrams[sentence[i - 1]])))

                

                for j in bigrams:
                    if sentence[i] in bigrams[j]:
                        tot2 += 1 

                p3 = float(max(tot2 - d, 0))/float(bi_vocabulary)
                lam3 = (float(d/tot_unigrams)*float(uni_vocabulary))
                p3 = lam3/uni_vocabulary + p3
                print(p3)
                p2 += lam2*p3
                p += lam1*p2
                p0 += lam0*p

                cur += math.log(p0)
            
            else:
                prob = (d/tot_unigrams)*(uni_vocabulary/quad_vocabulary)
                cur += math.log(prob)
    # perplexity = pow(math.exp(cur) , -1*(1/(len(sent))))/
    return math.exp(cur)

# n = sys.argv[1]
type = sys.argv[1]
# filepath = 

file = open(sys.argv[2])
corpus = file.read()
corpus = corpus.lower()
corpus = re.sub(' +', ' ', corpus)
corpus = re.sub('[^a-zA-Z \n]+', '', corpus)
corpus = re.sub('-+', ' ', corpus)

# cleaned_corpus = clean(corpus)
# sentences = sentencizer(cleaned_corpus)
sentences = []
temper = corpus.split("\n")
for senten in temper:
    if senten.strip():
        sentences.append(senten.strip())
# print (sentences)
# print(sentences)
sentences = [s.split(' ') for s in sentences]
# print (sentences)

# unigrams = get_unigrams(sentences)
unigrams = {}
for sentence in sentences:
    for word in sentence:
        if word not in unigrams:
            unigrams[word] = 1
        else:
            unigrams[word] += 1

# bigrams = get_bigrams(sentences)
bigrams = {}
for sentence in sentences:
    length = len(sentence)
    for i in range(0,length - 1):
        if sentence[i] not in bigrams:
            bigrams[sentence[i]] = {}
        if sentence[i+1] not in bigrams[sentence[i]]:
            bigrams[sentence[i]][sentence[i+1]] = 1
        else:
            bigrams[sentence[i]][sentence[i+1]] += 1

# trigrams = get_trigrams(sentences)
trigrams = {}
for sentence in sentences:
    length = len(sentence)

    for i in range(0,length - 2):
        if sentence[i] not in trigrams:
            trigrams[sentence[i]] = {}

        if sentence[i+1] not in trigrams[sentence[i]]:
            trigrams[sentence[i]][sentence[i+1]] = {}

        if sentence[i+2] not in trigrams[sentence[i]][sentence[i+1]]:
            trigrams[sentence[i]][sentence[i+1]][sentence[i+2]] = 1

        else:
            trigrams[sentence[i]][sentence[i+1]][sentence[i+2]] += 1

# quadgrams = get_quadgrams(sentences)
quadgrams = {}
for sentence in sentences:
    length = len(sentence)

    for i in range(0,length - 3):
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
# print(quadgrams)
# print(trigrams)

# print(unigrams)
# print()
# print(bigrams)
# print()
# print(trigrams)

# print("input sentence:", end=" ")
senti = input("input a sentence: ")

sent = []

# senti = clean(senti)
senti = senti.lower()
senti = re.sub(' +', ' ', senti)
senti = re.sub('[^a-zA-Z \n]+', '', senti)
senti = re.sub('-+', ' ', senti)

if senti.strip():
    sent.append(senti.strip())
print(sent)
# sent = sentencizer(sent)
# lolol = sent[0]
# sent[0] = lolol.split(' ')
sent = [s.split(' ') for s in sent]
print (sent)

# print(sent)
if sent:

    # if n == "1" and type == "k":
    #     print(kneser_ney_unigrams(unigrams, sent))

    # elif n == "2" and type == "k":
    #     print(kneser_ney_bigrams(bigrams, sent, unigrams))

    # elif n == "3" and type == "k":
    final_probab = kneser_ney_trigrams(quadgrams, sent, unigrams, bigrams, trigrams)
    perplexity = pow(final_probab , ( -1/len(sent[0]) ))
    print(len(sent[0]))
    print(perplexity)
    print ( final_probab)
    # print(unigrams)
    # for i in bigrams:
    #     print(bigrams[i])
    # elif n == "1" and type == "w":
    #     print(witten_bell_unigrams(unigrams, sent))

    # elif n == "2" and type == "w":
    #     print(witten_bell_bigrams(bigrams, sent, unigrams))

    # elif n == "3" and type == "w":
    #     print(witten_bell_trigrams(trigrams, sent, unigrams, bigrams))
