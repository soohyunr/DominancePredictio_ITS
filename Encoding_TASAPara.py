'''
This file initiate vectors for words and constuct Memory with TASAPara corpus
The Word vectors is stored in "Words_tasaPara.csv"
The Memory matrix is stored in "Memory_storage_tasaPara.csv)"
'''

#### Set parameters
N_dimension = 2000


corpus = open("tasaDocsPara.txt","r").read()
corpus = re.sub("[^\w]null[^\w]"," ",corpus)
corpus = re.sub("[^\w]nan[^\w]"," ",corpus)

#############################
#### Construct the environmental word vectors from a Gaussian
#### with mean = 0 and sd = 1/sqrt(n)
#############################


unique_words = list(set(re.sub("[^\w]"," ",corpus).split()))
matrix=np.random.normal(loc = 0, scale = 1/math.sqrt(N_dimension),
                           size = (len(unique_words),N_dimension))
Words = pd.DataFrame(matrix, index = unique_words)
Words.to_csv(os.getcwd()+'/Words_tasaPara.csv',index=True)

print("Words Vectors are Created")

#############################
#### Construct Memory 
#### based on Words Vectors
#############################


Paras = corpus.split("\n")
Memory = np.zeros((len(Paras), N_dimension))
for i in range(len(Paras)):
   Tmp = Paras[i].split(" ")
   if len(Tmp) > 0:
      for j in range(len(Tmp)):
         W_Representation = Words.loc[Tmp[j]]
         Memory[i] = Memory[i]+W_Representation
         
np.savetxt('Memory_storage_tasaPara.csv', Memory, delimiter = ',')
print("Memory matrix is Created")

