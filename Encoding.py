#######################################
#Construct Memory based on tasaSentDocs
#######################################

import re
import os
import pandas as pd
import numpy as np
from numpy import dot
from numpy.linalg import norm
import math
import nltk
from nltk.corpus import stopwords, wordnet
from nltk.stem import WordNetLemmatizer

#### Set parameters
N_dimension = 2000
Tau = 3
Forgetting_rate = 0
       
#### Get unique words in the corpus
lemmatizer = WordNetLemmatizer()
stopwords = stopwords.words("english")


#######################################
#Construct Memory based on tasaSentDocs
#######################################

#### Name the corpus
corpus = open("tasaSentDocs.txt","r").read()

unique_words = list(set(re.sub("[^\w]"," ",corpus).split()))
unique_words = list(set([word for word in unique_words if word not in stopwords]))
unique_words= list(set([lemmatizer.lemmatize(word) for word in unique_words]))

#### Construct the environmental word vectors from a Gaussian with mean = 0 and sd = 1/sqrt(n)
matrix=np.random.normal(loc = 0, scale = 1/math.sqrt(N_dimension),
                           size = (len(unique_words),N_dimension))
Words = pd.DataFrame(matrix, index = unique_words)
Words.to_csv(os.getcwd()+'/Words_tasaSent.csv',index=True)


#### Get all exemplar-sentences in the corpus
Sentences = corpus.split("\n")

#### No sentences greater than 20 words in length were included
Sentences = [sent.strip() for sent in Sentences if len(sent.split()) <= 20]
Sentences = [re.findall('[\w]+',sent) for sent in Sentences]
Sentences = [sent for sent in Sentences if len(sent) > 0]
Sentences = [[lemmatizer.lemmatize(word) for word in sent if word not in stopwords] for sent in Sentences]

#### Create RPs to encode sequential information in semantic space

max_lengths =20
RPs= []
for word_position in range(max_lengths):
   RPs.append(np.random.permutation(range(2000)))

#### Construct exemplar-sentence record of the corpus

WITH ORDERINFORMATION
Memory = np.zeros((len(Sentences), N_dimension))

for i in range(len(Sentences)):
   if i%10000==0:
      print(i)
   Tmp = Sentences[i]
   for j in range(len(Tmp)):
      W_Representation = Words.loc[Tmp[j]]
      W_Permuted = np.array(W_Representation[RPs[j]])
      Memory[i] = Memory[i]+W_Permuted 요까지 돌림.. 

print("========Instance Memory is constructed!========")
np.savetxt('orderedMemory_storage_tasaSent.csv', Memory, delimiter = ',')


#Memory = np.array(pd.read_csv("orderedMemory_storage_tasaSent.csv",header = None))
'WITHOUT ORDER INFORMATION

Memory = np.zeros((len(Sentences), N_dimension))

for i in range(len(Sentences)):
   if i%10000==0:
      print(i)
   Tmp = Sentences[i]
   for j in range(len(Tmp)):
      W_Representation = Words.loc[Tmp[j]]
      Memory[i] = Memory[i]+W_Representation

print("========Instance Memory is constructed!========")
np.savetxt('Memory_storage_tasaSent.csv', Memory, delimiter = ',')

Words = pd.read_csv('Words_tasaSent.csv',header = None)
Memory = np.array(pd.read_csv("Memory_storage_tasaSent.csv",header = None))


#######################################
#Construct Memory based on tasaParaDocs
#######################################

corpus = open("tasaDocsPara.txt","r").read()
corpus = re.sub("[^\w]null[^\w]"," ",corpus)
corpus = re.sub("[^\w]nan[^\w]"," ",corpus)

unique_words = list(set(re.sub("[^\w]"," ",corpus).split()))

matrix=np.random.normal(loc = 0, scale = 1/math.sqrt(N_dimension),
                           size = (len(unique_words),N_dimension))
Words = pd.DataFrame(matrix, index = unique_words)
Words.to_csv(os.getcwd()+'/Words_tasaPara.csv',index=True)

print("Words Document is Created")

Paras = corpus.split("\n")
Memory = np.zeros((len(Paras), N_dimension))
for i in range(len(Paras)):
   Tmp = Paras[i].split(" ")
   if len(Tmp) > 0:
      for j in range(len(Tmp)):
         W_Representation = Words.loc[Tmp[j]]
         #W_Permuted = np.array(W_Representation[RPs[j]])
         Memory[i] = Memory[i]+W_Representation
np.savetxt('Memory_storage_tasaPara.csv', Memory, delimiter = ',')

#Words = pd.read_csv('Words_tasaPara.csv',header = None)
#Words = Words.loc[1:].set_index(0)
#Memory = np.array(pd.read_csv("Memory_storage_tasaPara.csv",header = None))

