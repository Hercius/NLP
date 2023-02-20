#Alex Bleth Date: 10/20/2021
#This is a sentiment analysis program that takes in snetiment training data 
# and builds the decision list of words that deteminine the sentiment of a review as positive or negative.
#The decision list is determined by the log likelihood of the a word appearing for a given classification.
# an example of this would be the training file classifies a review, and so all words in that review are stored with their classification.
#then it sums each occurance of that word in other reviews. 
# (so like the word brilliant showing up 10 times in positive and 1 time in negative, meaning brilliant would be classified as positive)
#to run this, simply run this file, and you can change the training data if need be by changing the input file on line 28.
#The algorith works like this:
#1. open up the training file
#2. configure each review to change words that are negated with the not handler
#3. create a list that contains all the unigrams and bigrams with their associated rank from the review it came from
#4. create a dictionary with a key value pair of a word and an array of positive and negative counts
#5. create another list that takes the log likelihood of the associated word based on its positive and negative occurances.
#6. sorts the words in order of highest to lowest likelihood to create the decision list
#7. write the decision list to the decision list file
import math
import re
#this class holds each word from a review and its associated rank of that review
class sentimentOfWord:
    def __init__(self,word,rank):
        self.word = word
        self.rank = rank
#this was taken from my PA2 but converted to just give bigrams from a given list of words (in order)
def generateBigrams(words_list, rank):
        ngrams_list = []
 
        for num in range(0, len(words_list)):
            ngram = ' '.join(words_list[num:num + 2])
            ngrams_list.append(sentimentOfWord(ngram,rank))
        return ngrams_list

def main():
    print("Running Alex Bleth's Training program.")
    #this is a cutoff that will get rid of any features that show up less than the cutoff amount
    criticalCutoffmin = 35
    words = []
    notEndOfFile = True
    with open("sentiment-train.txt", "r") as file:
       
        #this grabs each review from the training set, and separates each of its fields into the review class. 
        #This also gives the list of unigrams and bigrams. 
        while notEndOfFile:
            initialReview = file.readline()
            if initialReview:
                text = initialReview.split()
                identity = text[0]
                rank = text[1]
                unigramsList = []
                UnigramReview = initialReview.split()[2:]
                newUnigrams = []
                between = False
                #this loops through the review and adds the not handle to each feature that follows any not words
                for i in UnigramReview:
                    if i == "." or i == "!" or i == "?":
                        between = False
                    if between:
                        i = "not_"+ i
                        
                    if i == "not" or i == "can't" or i == "isn't" or i =="aren't" or i == "won't":
                        between = not between
                    #this is to generate the bigrams
                    newUnigrams.append(i)
                    #this constructs the list of unigrams with its associated rank 
                    unigramsList.append(sentimentOfWord(i,rank))
                
                #generates bigrams
                bigramsList = generateBigrams(newUnigrams, rank)
                #add the unigrams and bigrams to the initial features list
                words.extend(unigramsList)
                words.extend(bigramsList)
                            
            else:
                notEndOfFile = False
        
        sentimentWords = dict()
        #this creates a dictionary with a word keyword and is paired with a list that had the total positive in the first position 
        # and total negative in the second position
        for ngram in words:
                  
            if ngram.word in sentimentWords:
                    
                if ngram.rank == "1":
                    sentimentWords[ngram.word][0] = sentimentWords[ngram.word][0]+1
                elif rank == "0":
                    sentimentWords[ngram.word][1] = sentimentWords[ngram.word][1]+1
                        
            else: 
                if ngram.rank == "1":   
                    sentimentWords[ngram.word] = [1,0]
                elif ngram.rank == "0":
                    sentimentWords[ngram.word] = [0,1]
    #this creates the final sentiment tally for the words, and cuts off unigrams/bigrams that are less than the cutoff, so that one that show up rarely do not sway the decision more than the statistcally sound
    #this also gets rid of the not useful, or to commonly occuring features (like the word the) so that it narrows the decisionlist, and makes it more accurate as a whole.
    finalSentimentWords = dict()  
    for word in sentimentWords:
        if sentimentWords[word][0] + sentimentWords[word][1] > criticalCutoffmin and not re.search(r"\bthe\b",str(word)) and not re.search('[.:,()|*@="]',str(word)) :
            finalSentimentWords[word] = sentimentWords[word]
   #this creates a dictionary with the word, loglikelyhood, and the rank
    wordWithDecisionList = dict()
    for word in finalSentimentWords:
        probabilityOfP = finalSentimentWords[word][0]/(finalSentimentWords[word][0]+finalSentimentWords[word][1]) + .1
        probabilityOfN = finalSentimentWords[word][1]/(finalSentimentWords[word][0]+finalSentimentWords[word][1]) + .1
        if probabilityOfN > probabilityOfP:
            wordWithDecisionList[word] = [round(abs(math.log(probabilityOfP/probabilityOfN,2)),4),0]   
        else:
            wordWithDecisionList[word] = [round(abs(math.log(probabilityOfP/probabilityOfN,2)),4),1]
    #this sorts the decision list dictionary by the highest to the lowest likelyhood
    sortedWordsWithDecision = dict(sorted(wordWithDecisionList.items(), key=lambda item: item[1][0],reverse = True))
    #creates the decisionlist file
    with open("sentiment-decision-list.txt","w") as file:
        for item in sortedWordsWithDecision:
            file.write(item + " " + str(format(sortedWordsWithDecision[item][0],".4f")) + " " + str(sortedWordsWithDecision[item][1])+"\n")
               
main()