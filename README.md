# DominancePrediction_ITS
Project to predict dominancy of meanings inherent homonyms using Instance-based Distributional Semantic Model (The Instance Theory of Semantics (ITS) Jamieson, Avery, Johns, & Jones, 2018) 

## TasaSentDocs.txt
[Thomas K Landauer and Susan T Dumais. 1997. A solution to plato’s problem: The latent semantic analysis theory of acquisition, induction, and representation of knowledge. Psychological review, 104(2):211.]

This corpus used to construct memory on the basis of sentences

## tasadocspara.txt
[Thomas K Landauer and Susan T Dumais. 1997. A solution to plato’s problem: The latent semantic analysis theory of acquisition, induction, and representation of knowledge. Psychological review, 104(2):211.]

This corpus used to construct memory on the basis of paragraphs

## eDom_norms.txt
[Blair C Armstrong, Natasha Tokowicz, and David C Plaut. 2012. edom: Norming software and relative meaning frequencies for 544 english homonyms. Behavior research methods, 44(4):1015–1027.]

This is used as target value for testing ITS's performance in determining dominancy


## Encodinng_TASASent.py

This is the process of constructing memory with tasaSentDocs.txt corpus

## Encoding_TASAPara.py

This is the process of constructing memory with tasadocspara.txt corpus

## ITS_Definitions.py

This includes functions that ITS model needs especially to retrieve semantic meanings
from words or sets of words

## DominanceMeasurement.py

This is to implement ITS in predicting dominancies of homonyms

## Analysis.R

This is for statistical analyses of the performance of ITS model
