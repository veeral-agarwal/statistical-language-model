# importing relavent libraries
from string import punctuation as punkts
import re


# loading data
file = open('brown.txt')# data file in argv[1]
data = file.read()
data = data.split('.')

#data cleaning 
import re
def clean(string):
    string = string.encode('ascii', 'ignore').decode('ascii')
    string = re.sub('^\[.*\]','',string)
    string = re.sub('^.*:','',string)
    string = string.strip()
    string = string.strip('\"')
    string = re.sub('\?+','?',string)
    string = re.sub('!+','!',string)
    string = re.sub('\.+','.',string)
    string = re.sub(' +',' ',string)
    string = re.sub('\(.*\)','',string)
    string = string.replace(':)','')
    string = string.replace(';)','')
    string = string.replace('*','')
    string = string.strip()
    return string


#cleaned data generation
for i in range(len(data)):
    data[i] = data[i].replace('\n',' ')
    data[i] = clean(data[i])
    data[i] = data[i] + '.'
cleaned = []
for i in range(len(data)):
    if len(data[i])>=10:
        cleaned.append(data[i])

#train tese split
train_data = cleaned[:35000]
valid_data = cleaned[35000:40000]
test_data = cleaned[40000:]

#tokenization (returns a list of strings) 
def tokenize(data):
    # tokenizes and returns a list of strings
    new_data = []
    for line in data:
        temp_line = ' '
        temp_line = line.lower()
        for x in punkts:
            temp_line = temp_line.replace(x,f' {x}')
        #new_line = re.sub(' +', ' ', new_line)
        temp_line = temp_line.strip()
        new_line = temp_line.split(' ')
        new_line = ['<s>']*3 + new_line + ['</s>']
        new_data.append(new_line)
    return new_data

#tokenization of train test and validation 
train_data = tokenize(train_data)
valid_data = tokenize(valid_data)
test_data = tokenize(test_data)

#counting total words
total_words = 0
for line in train_data:
    for word in line: 
        total_words += 1

#creating n-grams
def ngrams_generator(data):
    ngrams = [{} for i in range(5)]
    for n in [1,2,3,4]:
        for line in data:
            for i in range(len(line)-n):
                temp_gram = line[i:i+n]
                temp_gram_str = ' '.join(temp_gram)
                if temp_gram_str in ngrams[n]:
                    ngrams[n][temp_gram_str] += 1
                else:
                    ngrams[n][temp_gram_str] = 1
    return ngrams

ngrams = ngrams_generator(train_data)

def word_types(context, n):
    count = 0
    for words in ngrams[n].keys():
        if words.startswith(context):
            count+=1
    return count

totalent = [0]*5
for i in range(5):
    totalent[i] = sum(ngrams[i].values())

#kneser
def kneser(sent):
    d = 0.75
    p = 1
    def do_calculations(i,n):
        context = ' '.join(sent[i-n+1:i])
        new_ngram = ' '.join(sent[i-n+1:i+1])
        if n == 1:
            if new_ngram in ngrams[n]:
                first_num = max(ngrams[n][new_ngram] - d, 0)
                first_dem = total_words
                first_elem = first_num/first_dem
            else:
                first_elem = 0
            second_elem = d/len(ngrams[n])
            return first_elem + second_elem
        if new_ngram in ngrams[n]:
            first_num = max(ngrams[n][new_ngram] - d, 0)
            first_dem = ngrams[n-1][context]
            first_elem = first_num/first_dem
        else:
            first_elem = 0
        if context in ngrams[n-1]:
            interpolator = (d/ngrams[n-1][context])*word_types(context, n)
            interpolated = do_calculations(i,n-1)
            second_elem = interpolator * interpolated
        else:
            interpolator = ((d*len(ngrams[n-1]))/totalent[n-1])
            interpolated = do_calculations(i,n-1)
            second_elem = interpolator * interpolated
        return first_elem + second_elem
    for i in range(3,len(sent)-1):
        p *= do_calculations(i,4)
    return (p ** (-1/len(sent)))

#wittenbell
def wittenbell(sent):
    d = 0.75
    p = 1
    def do_calculations(i,n):
        context = ' '.join(sent[i-n+1:i])
        new_ngram = ' '.join(sent[i-n+1:i+1])
        if n == 1:
            if new_ngram in ngrams[n]:
                first_num = ngrams[n][new_ngram]
                first_dem = total_words
                first_elem = first_num/first_dem
            else:
                first_elem = 0
            second_elem = d/len(ngrams[n])
            return first_elem + second_elem
        elif new_ngram in ngrams[n]:
            first_elem = ngrams[n][new_ngram]
        else:
            first_elem = 0
        if context in ngrams[n-1]:
            nplus = word_types(context, n)
            second_elem = ngrams[n-1][context]
        else:
            nplus = do_calculations(i,n-1)
            second_elem = ((d*len(ngrams[n-1]))/totalent[n-1])
        return (first_elem + nplus*do_calculations(i,n-1))/(second_elem + nplus)
    for i in range(3,len(sent)-1):
        p *= do_calculations(i,4)
    return (p ** (-1/len(sent)))

# enter outout file 
output_name = 'temp.txt' # change output filename here 
f = open(output_name,'w')
tot, c = 0, 0
for sent in valid_data[:100]:
    try:
        val = wittenbell(sent) # or kneser
        tot += val
        c += 1
        print(c)
        if c%10==0:
            print(val)
        temp = ' '.join(sent)+'\t'+str(val)+'\n'
        f.write(temp)
    except:
        print('f')
        
avg = tot/c
temp = "Average"+'\t'+str(avg)+'\n'
f.write(temp)
f.close()