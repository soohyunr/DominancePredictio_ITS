rm(list=ls())
getwd()
result <- read.csv(file = 'result_new.csv', header = TRUE)
library(ggplot2)

##############
#
#remove words whose prepocessed definitions has length of 0 or 1
#
##############

result<- result[which(result$def1_len!=0),]
result<- result[which(result$def1_len!=1),]

result<- result[which(result$def2_len!=0),]
result<- result[which(result$def2_len!=1),]

frequency <- c()
accuracy <- c()

result1<-result[which(result$word_frequency<300),]
frequency <- append(frequency,0)
accuracy <- append(accuracy,sum(result1$correct)/length(result1$correct))

result2<-result[which(result$word_frequency>=300 & result$word_frequency <600),]
frequency <- append(frequency,300)
accuracy <- append(accuracy,sum(result2$correct)/length(result2$correct))

result3<-result[which(result$word_frequency>=600 & result$word_frequency<900),]
frequency <- append(frequency,600)
accuracy <- append(accuracy,sum(result3$correct)/length(result3$correct))

result4<-result[which(result$word_frequency>=900),]
frequency <- append(frequency,900)
accuracy <- append(accuracy,sum(result4$correct)/length(result4$correct))

data <- data.frame(frequency,accuracy)
ggplot(data = data, aes(x=frequency, y = accuracy)) + geom_smooth()


##############################################################################################
# Correlation Test
# (error = [norm_dominance - ITS_dominance]^2)
##############################################################################################

#Sum of squre error
result$error <- (result$norm_dominance-result$ITS_Dominance)**2

#gives tnedency of negative correlation
cor.test(result$error, result$word_frequency)   

