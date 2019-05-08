'''
Dominance measure with ITS
'''

#import ITS
#from ITS import *
import ITS_Definitions
from ITS_Definitions import *
import pandas as pd
import numpy as np
import re
import nltk
from nltk.corpus import wordnet as wn
import collections
from collections import Counter

Tau = 3
corpus = open("tasaDocsPara.txt","r").read()
word_count = Counter(re.sub("[^\w]"," ",corpus).split())

#====================================================================


Memory = np.array(pd.read_csv("Memory_storage_tasaPara.csv",header = None))
print("-------------------Memory is imported")

Words = pd.read_csv("Words_tasaPara.csv", header=None)
Words = Words.loc[1:].set_index(0)
Wordset = Words.index
print("-------------------Wordset is imported")


norm = pd.read_table('eDom_norms.txt',sep='\t')
Wordsmyth = open('WordSmyth.csv',errors='ignore').readlines()
Wordsmyth = [i.replace('\n','') for i in Wordsmyth]
Wordsmyth = [i.split(',') for i in Wordsmyth]
WS_dictionary = dict()

i = 1


for WD in Wordsmyth:
   W = WD[0]
   D = WD[1:]
   D = [x for x in D if x!='']
   if W in Wordset:
      WS_dictionary[W]=D
   i+=1
   if i>553:
      break

#============
#  STORAGE CREATION
#============
result = dict()
targetwords = []
def1 =[]
def2 = []
def1_freq = []
def2_freq = []
def1_similarity = []
def2_similarity = []
similarity_btwn_defs = []
norm_dominance= []
ITS_dominance = []
ITS_dominance_2 =[]
word_frequency = []
   
#==============
# Data Creation - Predict dominancy of homonyms using ITS
#     
#
#==============

for t_word in WS_dictionary.keys():
   WRep = getExpectationVector_2(Words.loc[t_word],Memory,Tau)
   defs=WS_dictionary[t_word]

   Similarities_WD = []
   defReps = []

   
   if len(defs)==2 and (norm[norm['word']==t_word]['NumMeanings']==2).bool():
      for num in range(len(defs)):

         #Cleasing definition
         definition = defs[num].lower()
         definition = re.sub("[^\w]"," ",definition).split()
         
         #Exclude words that are not included in Tasa Corpus
         definition = [word for word in definition if word in Wordset and word != t_word]
         
         #Get ExpectationVector from each definition
         definition_expectationVector = getJointProbeExpectation(definition,Words,Memory,Tau)
         #definition_expectationVector = definition_expectationVector/sum(abs(definition_expectationVector))
         defReps.append(definition_expectationVector)
         
         #Get Similarity between the word representation and definition
         Similarities_WD.append(Cosine(WRep,definition_expectationVector))
         
         #Get Similarity between two definitions
      similarity_between_defs = Cosine(defReps[0],defReps[1])


           # Add to result dataset 
      targetwords.append(t_word)
      def1.append(defs[0])
      def2.append(defs[1])
      def1_freq.append(norm[norm['word']==t_word]['p1'].values[0])
      def2_freq.append(norm[norm['word']==t_word]['p2'].values[0])
      def1_similarity.append(round(Similarities_WD[0],4))
      def2_similarity.append(round(Similarities_WD[1],4))
      similarity_btwn_defs.append(round(similarity_between_defs,4))
      norm_dominance.append(norm[norm['word']==t_word]['dominance'].values[0])
      ITS_dominance.append(round((max(Similarities_WD)-min(Similarities_WD)),4))
      ITS_dominance_2.append(round((max(Similarities_WD)-min(Similarities_WD))/max(Similarities_WD),4))
      word_frequency.append(word_count[t_word])




result['targetword']= targetwords
result['def1'] = def1
result['def2'] = def2
result['def1_freq'] = def1_freq
result['def2_freq'] = def2_freq
result['def1_similarity'] = def1_similarity
result['def2_similarity'] = def2_similarity
result['similarity_btwn_defs'] = similarity_btwn_defs
result['norm_dominance'] = norm_dominance
result['ITS_dominance'] = ITS_dominance
result['ITS_dominance_2'] = ITS_dominance_2
result['word_frequency'] = word_frequency 



result = pd.DataFrame(result)
result.to_csv(os.getcwd()+'/result.csv',index=True)

