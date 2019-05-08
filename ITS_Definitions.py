'''
This file includes definitions required to retrieval process of ITS
'''

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

######################################
####         DEFINNITIONS         ####
######################################

#############################
#### COSINE SIMILARITY
#############################

def Cosine(x,y):
   z = 0
   if sum(x) !=0 and sum(y) != 0:
      z = dot(x,y)/(norm(x)*norm(y))
   return z

#############################
#### JOINT PROBE
#############################

def getJointProbeExpectation(defVec,WordSet,MemorySet,Tau):
   S = np.zeros(N_dimension)
   for memory in MemorySet:
      Activation = 1
      for defWord in defVec:
         #print(defWord)
         Similarity = Cosine(WordSet.loc[defWord],memory)**Tau
         if Similarity >0:
            Activation *= Similarity
      if Activation!=1:
         S+=Activation*memory
   return S



#############################
#### EXPECTATION VECTOR
#############################

'''
takes word(string) as input
'''

def getExpectationVector_1(Word,WordSet,MemorySet,Tau):
   S = np.zeros(N_dimension)
   W_Representation = WordSet.loc[Word]
   #W_Permuted = W_Representation[RP[loc]]       #Permuted
   for memory in MemorySet:
      Activation = (Cosine(W_Representation,memory)**Tau)
      if Activation >0:
         S +=Activation*memory
   #print(Activation)
   return S



'''
takes vector representation of words
'''

def getExpectationVector_2(Word_R,MemorySet,Tau):
   S = np.zeros(len(MemorySet[1]))
   W_Representation = Word_R
   #W_Permuted = W_Representation[RP[loc]]       #Permuted
   for memory in MemorySet:
      Similarity = Cosine(W_Representation,memory)
      if Similarity >0:
         S +=(Similarity**Tau)*memory
   return S


#############################
#### COMPREHENSION VECTOR
#############################


'''
retrieved expectations are summed into a single vector.
iteraitvely constructed expectation vector are returned.
To get final comprehension vector, use getComprehensionVector(Set,WordSet,MemorySet,Tau)[-1]
'''

def getComprehensionVector(Sent,WordSet,MemorySet,Tau,RP):
   DynamicProcessRecord = []
   S = np.zeros(len(MemorySet[1]))
   for position in range(len(Sent)):
      Word = Sent[position]
      W_Representation = WordSet.loc[Word]
      Expectation_Word = getExpectationVector(Word,WordSet,MemorySet,Tau,position,RP)
      #PermutedWords = np.array(W_Representation[RPs[position]])
      DynamicProcessRecord.append((" ".join(Sent[:position+1]),S+PermutedWords))
      S += PermutedWords
   return DynamicProcessRecord

