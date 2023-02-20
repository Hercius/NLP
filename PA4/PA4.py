#Alex Bleth Date: 11/03/2021
#This program is designed to look at a large corpus of words, 
# and determine the similarity of two words based on the co Occurances of words in the corpus by the cosine between their word vectors.
# to run this, simply type in as follows: python PA4 <w> <d> <p> 
# where <w> is the window size looking at co occurances, <d> is the directory of your corpus files, and <p> is the input file containing the word pairs you want to look at.
# an example of this would be if we set it to be a window size of 2, and after it looking through our corpus lets say it was looking at: clinton clinton, 
# since clinton and clinton are the same word, they should have a cosine value of 1, meaning they are the same word. the closer the cosine is to 1, the more similar the words are.
# The algorith is as follows:
# 1. for each file in our directory of the corpus:
# 2. preprocess the given sentence, then pass the window over it
# 3. add the coOccurances from the given window to the coOccurance count matrix
# 4. once all sentences have been passed over by the window, then for each co Occurance calculate its pmi value
# at this point preprocessing is done
# 5. for each pair in our input file, calculate the cosine of the two words and store it in a matrix
# 6. print out the cosine, word1, word2, word1count, word2count, coOccuranceCount, and pmi value sorted by the highest to lowest cosine.
import sys, getopt, os
import re
import math
#Keeps track of the total word count (for debugging purposes)
totalWordCount = 0
#Keeps track of the total Co-Occurances that are put in the matrix
totalOccurances = 0
#This dictionary stores the word as a key value and its number of times it appears
individuaCount = dict()
#This keeps track of each coOccurances and their counts (This is my coOccurance matrix, where the two words are used as a key value pair)
coOccuranceCount = dict()
#Keeps track of all the words that have been used as the word in the CoOccurance (the left side of the matrix)
wordOccurance = dict()
#Keeps track of all the words that have been used as the context word in the CoOccurance (the top side of the matrix)
ContextOccurance = dict()
#This is matrix holds the pmi values for all of the co Occurances in the matrix
pmiMatrix = dict()

#This function processes each sentence it is passed and gets rid of all of the punctuation and converts all the words into lowercase
def processSentence(sentence):
    newSentence = re.sub("[.?!:,_“'”’]",'', sentence)
    return newSentence.lower()

#This function passes a window of size: wSize over a given sentence and gets all of the coOccurances and adding their counts to the matrix, as well as summining the rows and columns.
def processWindow(wSize, sentence):
    #split each sentence into each individual word
    separatedSentence = sentence.split()
    i = 0
#loop through each word in the sentence and add them to the coOccurance matrix
    while i < len(separatedSentence):
        global totalWordCount 
        global totalOccurances
        totalWordCount = totalWordCount + 1
        if separatedSentence[i] in individuaCount:
            individuaCount[separatedSentence[i]] = individuaCount[separatedSentence[i]] + 1
        else:
            individuaCount[separatedSentence[i]] = 1
        
        j = i + 1
        #loops the window to capture all of the co Occurances
        while j < wSize+i:
            if(j < len(separatedSentence)):
                if (separatedSentence[i],separatedSentence[j]) in coOccuranceCount:
                    coOccuranceCount[(separatedSentence[i],separatedSentence[j])] = coOccuranceCount[(separatedSentence[i],separatedSentence[j])] + 1
                    wordOccurance[separatedSentence[i]] = wordOccurance[separatedSentence[i]] + 1
                    ContextOccurance[separatedSentence[j]] = ContextOccurance[separatedSentence[j]] + 1
                    totalOccurances = totalOccurances + 1
                else:
                    coOccuranceCount[(separatedSentence[i],separatedSentence[j])] = 1
                    wordOccurance[separatedSentence[i]] = 1
                    ContextOccurance[separatedSentence[j]] = 1
                    totalOccurances = totalOccurances + 1
            j = j + 1
        i = i + 1
#This function calculates the cosine between the two words
def calcCosine(word1,word2):
    sum = 0
    word1Square = 0
    word2Square = 0
    #This loops through each word in the columns
    for Occurance in ContextOccurance:
        #This checks to see if the words are in the coOccurance matrix, and if so then add them to the calculations
        if (word1, Occurance) in coOccuranceCount:
            word1Square = word1Square + math.pow(pmiMatrix[(word1, Occurance)],2)
            if (word2,Occurance) in coOccuranceCount:
                sum = sum + pmiMatrix[(word1, Occurance)]* pmiMatrix[(word2,Occurance)]
                word2Square = word2Square + math.pow(pmiMatrix[(word2,Occurance)],2)
            
            
        elif (word2,Occurance) in coOccuranceCount:
             word2Square = word2Square + math.pow(pmiMatrix[(word2,Occurance)],2)

    #Does the final calculations to determine the cosine
    word1Square = math.pow(word1Square,.5)
    word2Square = math.pow(word2Square,.5)
    return sum/(word1Square*word2Square)

def main():
    print("PA 4 computing similarity from a word by word PMI co-occurrence matrix, programmed by Alex Bleth.")
    print("\npreprocessing now")
    args = sys.argv[1:]
    #This retrieves the window size from the command line
    win = int(args[0])
    args = args[1:]
    #This retrieves the directory in which it scans the files
    directory = str(args[0])
    args = args[1:]
    #This takes in the key value pairs that you are looking at
    pairs = str(args[0])
    #This begins reading each file and processing each sentence in the file.
    for filename in os.listdir(directory):
        #checks to see if the file is over or not
        notEndOfFile = True
        with open(directory+"/"+filename,"r", encoding="utf8") as currFile:
            while notEndOfFile:
                #get the sentence
                temp = currFile.readline()
                if temp:
                    #pre-process the sentence
                    sentence = processSentence(temp)
                    #pass the window over the sentence
                    processWindow(win,sentence)
                    
                else:
                    notEndOfFile = False
                    
    
  


    #This will calculate the pmi values and put them into a new matrix that corresponds to the co-Occurance matrix     
    for co in coOccuranceCount:
        #probality of the summed occurances that the word is apart of divided by the total number of occurances
        prob1 = wordOccurance[co[0]]/totalOccurances
        #probablity of the second word in the context (so column) divided by the total number of occurances
        prob2  = ContextOccurance[co[1]]/totalOccurances
        #total number in co-Occurance divided by the total occurances
        prob12 = coOccuranceCount[co]/totalOccurances

        finalProb = prob12/(prob1*prob2)
        #calculates the pmi value
        pmiMatrix[co] = round(math.log(finalProb,2),5)

    print("preprocessing is done")
    print("total tokens: " + str(totalWordCount) + "  total types: " + str(len(coOccuranceCount)) + " window size: " + str(win))
    #All preprocessing is done
    #now it moves onto looking at the input of the pairs    
    wordPairs = dict()
    notEndOfFile = True
    #read open from the pairs file
    with open(pairs,"r") as inputFile:
        while notEndOfFile:
            pairing = inputFile.readline()
            if pairing:
                
                words = pairing.split()
                #if the words are in the corpus, then calculate the cosine
                if words[0] in individuaCount and words[1] in individuaCount:
                    wordPairs[(words[0],words[1])] = calcCosine(words[0],words[1])
                else:
                    wordPairs[(words[0],words[1])] = -9999
                if (words[0],words[1]) not in coOccuranceCount:
                    coOccuranceCount[(words[0],words[1])] = 0
                    pmiMatrix[(words[0],words[1])] = 0
            else:
                notEndOfFile = False
    #sorts the list by the cosine value from highest to lowest
    sortedWordPairs = dict(sorted(wordPairs.items(), key=lambda item: item[1],reverse = True))
    #print results
    print("cosine\tword1\tword2 \tword1Count\tword2Count\tcoOccuranceCount\tpmi")
    for pair in sortedWordPairs:
        print(str(sortedWordPairs[pair]) + "\t" + pair[0] + "\t" + pair[1] + "\t" +str(individuaCount[pair[0]]) + "\t" + str(individuaCount[pair[1]]) + "\t" + str(coOccuranceCount[pair]) + "\t" + str(pmiMatrix[pair]) + "\n")

    
main()