# from main import *
import main
import re
import random
# f = open("./parallel/IITB.en-hi.en","rt")
# g = open("./parallel/IITB.en-hi.hi","rt")
# h = open("input_english.txt","w")
# j = open("input_hindi.txt","w")

# data_english = f.read()
# data_hindi = g.read()
# sentences_english = []
# data_english_list = []
# sentences_hindi = []
# data_hindi_list = []

# data_english_list = data_english.split("\n")
# data_hindi_list = data_hindi.split("\n")

# for i in range(500):
#     temp = random.randint(0,1561840)
#     sentences_english.append(data_english_list[temp])
#     sentences_hindi.append(data_hindi_list[temp])

# for i in range(len(sentences_english)):
#     if len(sentences_english[i].strip())<100 and len(sentences_english[i].strip())>20:
#         h.write(sentences_english[i]+"\n")
#         j.write(sentences_hindi[i]+"\n")

output_english = open("output_english.txt","w")

file_e = open("input_english.txt","rt")
input_english = file_e.read()
input_english = input_english.lower()
input_english = re.sub(' +', ' ', input_english)
input_english = re.sub('[^a-zA-Z \n]+', '', input_english)
input_english = re.sub('-+', ' ', input_english)
input_english_list = []
input_english_list = input_english.split("\n")
file_h = open("input_hindi.txt","rt")
input_hindi = file_h.read()
input_hindi_list = []
input_hindi_list = input_hindi.split("\n")

output_postags_english = []



for i in range(len(input_english_list)-1):
    # if len(input_english_list[i].strip()) < 100 and len(input_english_list[i].strip()) > 20:
    #     print(input_english_list[i])
    #     print(input_hindi_list[i])
    #     print(len(input_english_list[i].strip()))
    print(input_english_list[i])
    doc = main.nlp_en(input_english_list[i])
    output_postags_english.append(main.get_pos_tags(doc,1))
    # output_english.write(main.get_pos_tags)
    # print >> output_english,main.get_pos_tags
print(output_postags_english)