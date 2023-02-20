#Alex Bleth Date: 11/18/2021
#This is a Part of Speech Tagger tester program that takes in a the probabilites generated from our test set with their appropriate words and tags
# and assigns the appropriate tag to each word based on what mode it is in.
# Mode 0 is a generic frequency tagger, that assigns the highest probability to the word based off the probability training set.
# Additionally if it does not know what the word is, it marks it as a Noun (NN)
# 
# Mode 1 is and enhanced frequency tagger that does the same thing as Mode 0 but with rules.
# rules for known words and correcting errors (E):
# E-1. if the word before the currrent word is tagged as RB, VBD, or VB, and the current word is tagged as VBD, 
# and the following word is tagged as CC or IN, Mark the current word as VBN
# 
# E-2. if the previous word is tagged as ',' or CD, and the current word is tagged as IN, Mark the word as RB
#
# E-3 if the following word is tagged as RB and the current word is tagged as NN, mark the current word as a VB
#
# E-4 if the following word is tagged as NN,NNP,or NNS, and the current word is tagged as NNP, mark the current as JJ
#
# E-5 if the previous word is tagged as DT and the current word is tagged as VB, mark the current word as NN
#
# Rules for correcting unknown words (U):
#
# U-1 if the current word has the following pattern : (one or more number) followed by a . or , followed by (one or more number) mark it as CD
#
# U-2 if the current word has the following pattern: (one or more word characters) followed by a '-' followed by (one or more word characters)
# and the previous word was tagged with DT, IN, VBD, or CC, tag the current word with JJ
#
# U-3 if the whole word is uppercase or the first letter is uppercase, mark is as NNP
# 
# U-4 if the word ends in an s, mark it as NNS
#
# U-5 if the following word is tagged by NN,NNS,NNP, mark the current word as JJ 
#
# an example would be the word 'Countered', in which it is unknown, if set to mode 0, it would be marked as NN, 
# otherwise if set to mode 1 it is marked based off the rules given above
#to run this, run this file with the command line option of the mode, the training probabilities, and the test file.
#The algorith works like this:
#1. open up the training file
#2. put each tuple (the probability, tag, and word) into the dictionary (that acts as a matrix)
#3. open up the test file and run mode 0 on the test file and store it in a tagged dictionary
# (with the exception that rather than marking each unknown word as NN, it temporarily marks it as NotDefined, so that Mode 0 or 1 can be used on those words)
#4. do a second pass over the now tagged testfile and do the following:
#5. if mode 0, set all tags that were original put as NotDefined to NN, and then write the results to the file
#6. if mode 1, then for each pair (word, tag) use the set of rules for E and U were E are the rules that change words that are know but in correct,
#and U are the rules for words that are unknown.
#7. still for mode 1: if rules do not change the word at all, use the mode 0 outcome (so if unknown and rules didnt affect it, mark it as a NN), write the results to the file.

import re
import sys
def main():
    #get the mode, trainingFile, and test file from the command line parameters
    args = sys.argv[1:]
    mode = int(args[0])
    trainingFile = args[1]
    testFile = args[2]
    #create dictionaries which houses the training data, and the later tagged test words
    taggedWordsProb = dict()
    taggedWord = dict()
    #list of all tags
    tagsList = []
    #list of all words
    wordsList = []
    notEndOfFile = True
    taggedWordsList = []
    #open training file, and put the appropriate info into the taggedWordsProb dictionary with key (word,tag): probability
    with open(trainingFile, "r") as train:
        while notEndOfFile:
            currLine = train.readline()
            if currLine:
                line = currLine.split(" ")
                taggedWordsProb[re.sub("\n","",line[2]),line[1]] = line[0]
                if line[1] not in tagsList:
                    tagsList.append(line[1])
                if re.sub("\n","",line[2]) not in wordsList:
                    wordsList.append(re.sub("\n","",line[2]))
                    
            else:
                notEndOfFile = False
    #open up the test file, and run the initial mode 0 on the test file
    with open(testFile,"r") as test:
            notEndOfFile = True
            while notEndOfFile:
                testWord = test.readline()
                
                if testWord:
                    testWord = re.sub("\n","",testWord)
                    #for each tag, see if the pair is in the taggedWordsProb, if it is, and not in the taggedWord Dict, add it.
                    for tag in tagsList:
                        if (testWord,tag) in taggedWordsProb:
                            if testWord not in taggedWord:
                               
                                if testWord in wordsList:
                                    taggedWord[testWord] = tag     
                            #if not, check to see if the current tag word pair is greater than the previous, if so, then change the tag to the newer one
                            else:
                                   if taggedWordsProb[testWord,tag] > taggedWordsProb[testWord,taggedWord[testWord]]:
                                        taggedWord[testWord] = tag
                        #if word not known by training set, temporarily label it as NotDefined
                        elif testWord not in wordsList:
                                taggedWord[testWord] = "NotDefined"
                              
                    
                    #add the final pairs to the taggedWordsList
                    taggedWordsList.append([testWord,taggedWord[testWord]])
                        
                else:
                    notEndOfFile = False
    
    #previous pair in the list (so the previous word in the sentence/list of words)
    previousPair = ""
    firstTime = True
    
    for pair in taggedWordsList:
        #runs mode 0
        if mode == 0:
            if pair[1] == "NotDefined":
                taggedWordsList[taggedWordsList.index(pair)][1] = "NN"
        #runs mode 1
        elif mode == 1:
            #this is just for the first word, as there is no previous pair, if the first word is unknown, label it as NN as a precaution.
            if firstTime:
                if pair[1] == "NotDefined":
                    taggedWordsList[taggedWordsList.index(pair)][1] = "NN"
                firstTime = False
            #rest of mode 1
            else:
                #if the word is unknown
                if pair[1] == "NotDefined":
                    #U- 1, refer to up top for what it does
                    if re.match("[0-9]+\.[0-9]+",pair[0]) or re.match("[0-9]+\,[0-9]+",pair[0]):
                        taggedWordsList[taggedWordsList.index(pair)][1] = "CD"
                    #U- 2, refer to up top for what it does
                    elif re.match("\w+[\-]\w+",pair[0]) and (previousPair[1] == "DT" or previousPair[1] == "IN" or previousPair[1] == "VBD" or previousPair[1] == "CC"):
                            taggedWordsList[taggedWordsList.index(pair)][1] = "JJ"
                    #U- 3, refer to up top for what it does
                    elif str.isupper(pair[0]) or str(pair[0])[0].isupper():
                        taggedWordsList[taggedWordsList.index(pair)][1] = "NNP"
                    #U- 4, refer to up top for what it does
                    elif re.match("\w*s",pair[0]):
                        taggedWordsList[taggedWordsList.index(pair)][1] = "NNS"
                    #U- 5, refer to up top for what it does
                    elif taggedWordsList[taggedWordsList.index(pair)+1][1] == "NN" or taggedWordsList[taggedWordsList.index(pair)+1][1] == "NNS" or taggedWordsList[taggedWordsList.index(pair)+1][1] == "NNP":
                        taggedWordsList[taggedWordsList.index(pair)][1] = "JJ"
                    #defaults to mode 0 output if it cannot use any of the rules above
                    else:    
                        taggedWordsList[taggedWordsList.index(pair)][1] = "NN"
                #if word is known
                else:
                    #E- 1, refer to up top for what it does
                    if (previousPair[1] == "RB" or previousPair[1] == "VBD" or previousPair[1] == "VB") and pair[1] == "VBD" and  (taggedWordsList[taggedWordsList.index(pair)+1][1] == "CC" or taggedWordsList[taggedWordsList.index(pair)+1][1] == "IN"):
                        taggedWordsList[taggedWordsList.index(pair)][1] = "VBN"
                    #E- 2, refer to up top for what it does
                    elif (previousPair[1] == "," or  taggedWordsList[taggedWordsList.index(pair)+1][1] == "CD") and pair[1] == "IN":
                        taggedWordsList[taggedWordsList.index(pair)][1] == "RB"
                    #E- 3, refer to up top for what it does
                    elif taggedWordsList[taggedWordsList.index(pair)+1][1] == "RB" and pair[0] == "NN":
                        taggedWordsList[taggedWordsList.index(pair)][1] == "VB"
                    #E- 4, refer to up top for what it does
                    elif  (taggedWordsList[taggedWordsList.index(pair)+1][1] == "NN" or taggedWordsList[taggedWordsList.index(pair)+1][1] == "NNP" or taggedWordsList[taggedWordsList.index(pair)+1][1] == "NNS") and pair[0] == "NNP":
                        taggedWordsList[taggedWordsList.index(pair)][1] == "JJ"
                    #E- 5, refer to up top for what it does
                    elif previousPair[0] == "DT" and pair[0] == "VB":
                        taggedWordsList[taggedWordsList.index(pair)][1] == "NN"
            #set the previous pair to the current pair for the next pair in the list
            previousPair = taggedWordsList[taggedWordsList.index(pair)]
                


    #write the final tagged words to the pos-test-key[01] depending on what mode it is
    with open("pos-test-key"+str(mode)+".txt", "w") as testW:
        for wordPair in taggedWordsList:
            testW.write(wordPair[0]+"/"+wordPair[1]+"\n")


main()