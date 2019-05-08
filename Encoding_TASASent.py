'''
This file initiate vectors for words and constuct Memory with TASASent corpus
The Word vectors is stored in "Words_tasaSent.csv"
The Memory matrix is stored in "Memory_storage_tasaSent.csv)"
'''
import os
import re
import pandas as pd
import numpy as np
import math

#### Set parameters
N_dimension = 2000


corpus = open("tasaSentDocs.txt","r").read()
corpus = re.sub("[^\w]null[^\w]"," ",corpus)
corpus = re.sub("[^\w]nan[^\w]"," ",corpus)
unique_words = list(set(re.sub("[^\w]"," ",corpus).split()))



#############################
#### Construct the environmental word vectors from a Gaussian
#### with mean = 0 and sd = 1/sqrt(n)
#############################


unique_words = list(set(re.sub("[^\w]"," ",corpus).split()))
matrix=np.random.normal(loc = 0, scale = 1/math.sqrt(N_dimension),
                           size = (len(unique_words),N_dimension))
Words = pd.DataFrame(matrix, index = unique_words)
Words.to_csv(os.getcwd()+'/Words_tasaSent.csv',index=True)

print("Words Vectors are Created")



#############################
#### Construct Memory 
#### based on Words Vectors
#############################

Sentences = corpus.split("\n")

#### No sentences greater than 20 words in length were included
Sentences = [sent.strip() for sent in Sentences if len(sent.split()) <= 20]
Sentences = [re.findall('[\w]+',sent) for sent in Sentences]
Sentences = [sent for sent in Sentences if len(sent) > 0]
Sentences = [[lemmatizer.lemmatize(word) for word in sent if word not in stopwords] for sent in Sentences]


Memory = np.zeros((len(Sentences), N_dimension))

for i in range(len(Sentences)):
   if i%10000==0:
      print(i)
   Tmp = Sentences[i]
   for j in range(len(Tmp)):
      W_Representation = Words.loc[Tmp[j]]
      Memory[i] = Memory[i]+W_Representation
      
np.savetxt('Memory_storage_tasaSent.csv', Memory, delimiter = ',')
print("Memory matrix is Created")
