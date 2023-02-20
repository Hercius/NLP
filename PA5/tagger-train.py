#Alex Bleth Date: 11/18/2021
#This is a Part of Speech Tagger program that takes in a pre-tagged training set 
# and calculates the probability each word has to be associated with a tag with p(tag|word).
#
# an example would be the word 'past', in which it can be used as JJ, NN, IN, or RB. We count up the times it appears, and count each different tag it appears with.
# We then get the probablity for each tag that is asociated to the word and write that to our training file.
#to run this, run this file with the command line option of the training set.
#The algorith works like this:
#1. open up the training file
#2. separate the word from the tag
#3. count each word and each tag associated with that word 
#4. create a dictionary with a key value pair of a word and its tag that keeps track of the number of occurances.
#5. create another dictionary that gets the probablity: p(tag|word) of the tag and word.
#6. sorts the dictionary
#7. write the probabilities with its tag and word associated with it.
import re
import sys
def main():
    #gets the file name
    args = sys.argv[1:]
    trainingFile = args[0]
    #dictionaries for the tagged words, the tags, and the words themselves (counting each occurance)
    taggedWords = dict()
    wordCount = dict()
    tagCount = dict()
    fileNotDone = True
    taggedWordsProb = dict()
    totalWordCount = 0
    #open training set file
    with open(trainingFile,"r") as file:
        #loop through full file
        while fileNotDone:
            currWord = file.readline()
            if currWord:
                #increase total word count
                totalWordCount = totalWordCount +1
                #checks for the words with \/ in it
                if re.search(".*[\\\]/.*/",currWord):
                    #separate the word from the tag
                    word = re.search(".*\\\/.*/", currWord).group()
                    word = word[0:len(word)-1]
                    

                    tag = re.search("\/\w*$", currWord).group(0)[1:]
                    #add the tag and word to each appropriate count
                    if word not in wordCount:
                            wordCount[word] = 1
                    else:
                            wordCount[word] = wordCount[word] + 1
                    if tag not in tagCount:
                            tagCount[tag] = 1
                    else:
                            tagCount[tag] = tagCount[tag] + 1
                    if (word,tag) not in taggedWords:
                                taggedWords[word,tag] = 1
                    else:
                                taggedWords[word,tag] = taggedWords[word,tag] +1
                    
                #words that do not contain a \/ in it
                else:
                    #separate word from tag
                    word = re.search("(.*?)/",currWord).group()
                
                    word = word[0:len(word)-1]
                    
                    
                    tag = re.search("\/.*", currWord).group()[1:]
                   #add tag and word to their appropriate counts
                    if (word,tag) not in taggedWords:
                                taggedWords[word,tag] = 1
                    else:
                                taggedWords[word,tag] = taggedWords[word,tag] +1
                    if word not in wordCount:
                                wordCount[word] = 1
                    else:
                                wordCount[word] = wordCount[word] + 1
                    if tag not in tagCount:
                                tagCount[tag] = 1
                    else:
                                tagCount[tag] = tagCount[tag] + 1

                   
                    
            else:
                fileNotDone = False
            
        #Counting of tags and words is done
        #for each pair that is found in the matrix, calculate the probability of: p(tag|word)
        for word in wordCount:
            for tag in tagCount:
                if (word,tag) in taggedWords:
                    
                    taggedWordsProb[word,tag] = (round(taggedWords[word,tag]/wordCount[word],4))

        #sort by smallest to largest probability       
        sortedTaggedWordsProb = dict(sorted(taggedWordsProb.items(), key=lambda item: item[1]))
        
        #write each probability, tag, and word to the list
        with open("tagger-train-probs.txt","w") as fileP:
                for keyV in sortedTaggedWordsProb:
                    
                    if keyV in sortedTaggedWordsProb:
                        
                        fileP.write(str(sortedTaggedWordsProb[keyV]) + " " + keyV[1] + " " + keyV[0] + "\n")
                
        
    

    
            

main()