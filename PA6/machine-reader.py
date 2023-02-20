#Alex Bleth Date: 12/08/2021
#
#I tried implementing part of mode 1 however due to time constraints (This was a busy week for me) I didnt complete it fully (so I only have 5 rules), however mode 0 is fully implemented 
#
#This is a machine reading program that specifies a mode 0 (baseline) and a mode 1 (enhanced) and takes in a file formatted from the mc500 dataset 
# and answers each question for each story in the dataset based on the mode it was set to. 
# Mode 1 works off of mode 0 where if there was answers it could not distinguish between 2 or more answers during mode 0 (and it was set to mode 1), then use the rules implemented to find a better fit answer.
#
# an example would be if I ran the command  c:/Users/ablet/Documents/NLP/PA6/machine-reader.py 0  mc500.dev.tsv 
# then this program would run in mode 0, which uses a simple sliding window over the story, and answers the question 
# based on which question+answer pair had the most occurances in the story (so if answer A had 8 occurances, while B, C, and D had less, then A is our best answer)
#to run this, run this file with the command line option of the mode (0 or 1) and the name of the mc500 file.
#The algorith works like this:
#1. open up the file
#2. create a dictionary that uses the story as the key, a list of questions and a list of answers for those questions as the value. This is then done for each story in the list.
#3. for each story do the following:
#4. for each question in the story: 
#5. split the question into a list and prep it for comparison (by removing punctuation, and setting it to lowercase)
#6. for each answer pertaining to the question do the following: (so 3 layers of nested for loops)
#6. prep the answer by tokenizing the words in the answer and making them lowercase
#7. set the window size equal to the length of the question plus the length of the answer
#8. add the two lists of tokens (question and answer) into a 'bag of words' and stem each word for consistency
#9. loop through the story with the window and process the story words (so that they are also lowercase, have no punctuation, and are stemmed)
#   then count how many words in the window shows up in the bag of words. record the highest occurance that this one answer gives
#10. after you have a set of the for answers find the position of the highest occurance and label that as the correct answer (so if the highest occurance is in position 0, then label it A, and so on, where 1 = B, 2 = C, and 3 = D)
#11. if mode 1 is enabled the check the current set of answers and see if it has duplicate highest values (so if answer a and b have a value of 8, then they are duplicates(c and d have less))
#12. if yes then mode 1 will look at the answers and use the rules provided (see after algorithm) to change the answer to the question if necessary
#13. after this it will record the bestAnswer for the question (for both mode 0 and mode 1)
#14 after finishing a set of questions for a story, append a list of each answer for the questions to a final list
#15. write the answers to the questions in the apropriate format

#List of Rules:
# QA1 if the word 'who' is in the question, the answer must contain a word with the tag 'NNP',if it does, then switch to the answer that first has it
# QA2 if the word 'what' is in the question, the answer must contain a word with the tag 'NN',if it does, then switch to the answer that first has it
# QA3 if the word 'where' is in the question, the answer must contain a word with the tag 'NNP' or 'NN',if it does, then switch to the answer that first has it
# QA4 if the word 'why' is in the question, the answer must contain a word with the tag 'VB',if it does, then switch to the answer that first has it
# QA5 if the wordS 'how' and 'many' is in the question, the answer must contain a word with the tag 'CD',if it does, then switch to the answer that first has it
import sys
import re
from nltk import tokenize
from nltk import pos_tag
from nltk.stem import PorterStemmer
from nltk.corpus import stopwords
#initialize the porterstemmer to be able to stem words
ps = PorterStemmer()
#this dictionary holds the story, and its associated questions and answers as key and value pairs
dicOfStories = dict()
#holds the final answers for each question set for each story
listOfFinalAnswers = []

notEndOfFile = True
#gets the list of arguements
args = sys.argv[1:]
#holds the value of the mode(should be 0 or 1)
mode = int(args[0])
#gets the file that is used
fileName = str(args[1])
#is for naming the file that gets written to (so if dev is the dataset, it will be able to write dev.MODE.answers.txt)
header = ""
if "dev" in fileName:
    header = "dev"
elif "test" in fileName:
    header = "test"
#This fuction works by taking the bagOfWords from the question answer pair and counts how many words from the window are in the bagOfWords
#it will then return the total amount it counted
def countOccurances(bag,window):
    count = 0
    
    for word in bag:
        if word in window:
            count = count+1
    return count
#This function looks to see what answers for a question have the highest value, 
#if there are any duplicate answers then return the indexs of those answers
def returnUndecidedAnswers(occurance):
    max_value = max(occurance)

    indices = [index for index, value in enumerate(occurance) if value == max_value]
    return indices
        

#Read from the file and add the story, its questions, and asnwers to the dicOfStories dictionary    
with open(fileName, "r") as file:
    while notEndOfFile:
        currLine = file.readline()
        if currLine:
            #cuts unneccesary data
            currdex = currLine.index(";")
            cutLine = currLine[currdex+1:]
            cutLine = cutLine[cutLine.index(";")+1:]
            #splits the line into each tabulated part
            sectionedParts = cutLine.split("\t")
            #removes the creativity words
            sectionedParts = sectionedParts[1:]
            #holds the story
            story = sectionedParts[0]
            sectionedParts = sectionedParts[1:]
            #this creates the list of questions that are associated with the story
            listOfQuestions = [sectionedParts[0],sectionedParts[5],sectionedParts[10],sectionedParts[15]]
            #This array holds all of the answers for each associated question
            listOfanwsers = [[sectionedParts[1],sectionedParts[2],sectionedParts[3],sectionedParts[4]],[sectionedParts[6],sectionedParts[7],sectionedParts[8],sectionedParts[9]]]
            listOfanwsers.append([sectionedParts[11],sectionedParts[12],sectionedParts[13],sectionedParts[14]])
            listOfanwsers.append([sectionedParts[16],sectionedParts[17],sectionedParts[18],sectionedParts[19]])
            #puts the entry of the story, questions, and answers into the dictionary
            dicOfStories[story] = [listOfQuestions,listOfanwsers]
            

        else:
            notEndOfFile = False



   #This is the start of mode 0
   # this will loop through each story 
    for story in dicOfStories:
        #this list and interger will keep track of the answers for a question
        tempAnswers = []    
        k = 0
        #this will loop through each question for each story
        for question in dicOfStories[story][0]:
            #preps the question by getting rid of punctuation, making it lowecase, and spliting it into a list 
            questionWords = re.sub("[!?.,;:]","",question).lower().split(" ")
        
            #this holds the best occurance from the sliding window for each question
            bestOccurance = []
            #loop through each answer for each question associated with the given story
            for answer in dicOfStories[story][1][k]:
                #makes the answer all lowercase
                splitAnswer = answer.lower()
                #tokenizes the answer
                tokenized = tokenize.word_tokenize(splitAnswer)
                #gets the window size (which is the size of the question and answer combined)
                windowSize = len(questionWords) + len(tokenized)
                #combines the question and answer
                pair = questionWords + tokenized
                bagOfWords = []
                #stems all of the words in the bag
                for word in pair:
                        bagOfWords.append(ps.stem(word))
                #holds the highest count
                answerCount = 0
                i = 0
                #loops through the story with the sliding window
                while i < len(story.split(" "))- windowSize+1:
                    temp = []
                    #preps the part of the story that the sliding window is currently over
                    for j in range(0,windowSize):
                        storyWord = story.split(" ")[i+j].lower()
                        
                        storyWord = re.sub(r"\\newline","",storyWord)
                        storyWord = re.sub("[.,!?;:]","",storyWord)
                        temp.append(storyWord)
                    wind = []
                    #stems the words currently in the window
                    for word in temp:
                            wind.append(ps.stem(word))
                    #get the number of occurances of words in the bag appearing in the window
                    tempCount = countOccurances(bagOfWords, wind)
                    #if the temp count is higher than the current highest, then replace it with the tempCount
                    if tempCount > answerCount:
                        answerCount = tempCount
                    i = i + 1
                
                #add the best occurance (highest number of words in the bag at one time) for the answer
                bestOccurance.append(answerCount)
              
            #get the index of the highest value
            max_value = max(bestOccurance)
            max_index = bestOccurance.index(max_value)
            #sets the best answer based on what index had the highest value (each index refers to an answer, so index 0 is for A)
            if max_index == 0:
                BestAnswer = "A"
            elif max_index == 1:
                BestAnswer = "B"
            elif max_index == 2:
                BestAnswer = "C"
            elif max_index == 3:
                BestAnswer = "D"
            #This is the start of mode 1, which continues from mode 0
            if mode == 1:
                #get rid of stop words in the question
                stop_words = set(stopwords.words('english'))
                #tokenize the question
                qTokenized = tokenize.word_tokenize(question)
                #get rid of all of the stop words
                filteredQTok = [w for w in qTokenized if not w.lower() in stop_words]
                
                fQTok = []
                #stem the rest of the words
                for word in filteredQTok:
                    fQTok.append(ps.stem(word))
                #add parts of speech to the question
                qTagged = pos_tag(fQTok)
                #if there are any duplicates then mode 1 will run
                if len(returnUndecidedAnswers(bestOccurance)) > 0:
                    #gets all of the indexs from the bestOccurance where there was a duplicate answer (in terms of the best occurance)
                    dupIndex = returnUndecidedAnswers(bestOccurance)
                    #refer to rule QA1
                    if "who" in qTokenized:
                        for index in dupIndex:
                            
                            tokAnswer = tokenize.word_tokenize(dicOfStories[story][1][k][index])
                            tagAnswer = pos_tag(tokAnswer)
                            p = 0
                            while p < len(tagAnswer):
                                if tagAnswer[p][1] == "NNP":
                                    if index == 0:
                                        BestAnswer = "A"
                                    elif index == 1:
                                        BestAnswer = "B"
                                    elif index == 2:
                                        BestAnswer = "C"
                                    elif index == 3:
                                        BestAnswer = "D"
                                    break
                                p = p + 1

                    #refer to rule QA2       
                    elif "what" in qTokenized:
                        for index in dupIndex:
                            tokAnswer = tokenize.word_tokenize(dicOfStories[story][1][k][index])
                            tagAnswer = pos_tag(tokAnswer)
                            p = 0
                            while p < len(tagAnswer):
                                if tagAnswer[p][1] == "NN":
                                    if index == 0:
                                        BestAnswer = "A"
                                    elif index == 1:
                                        BestAnswer = "B"
                                    elif index == 2:
                                        BestAnswer = "C"
                                    elif index == 3:
                                        BestAnswer = "D"
                                    break
                                p = p + 1
                    #refer to rule QA3
                    elif "where" in qTokenized:
                        for index in dupIndex:
                            tokAnswer = tokenize.word_tokenize(dicOfStories[story][1][k][index])
                            tagAnswer = pos_tag(tokAnswer)
                            p = 0
                            while p < len(tagAnswer):
                                if tagAnswer[p][1] == "NNP" or tagAnswer[p][1] == "NN":
                                    if index == 0:
                                        BestAnswer = "A"
                                    elif index == 1:
                                        BestAnswer = "B"
                                    elif index == 2:
                                        BestAnswer = "C"
                                    elif index == 3:
                                        BestAnswer = "D"
                                    break
                                p = p + 1
                    #refer to rule QA4
                    elif "why" in qTokenized:
                        for index in dupIndex:
                            tokAnswer = tokenize.word_tokenize(dicOfStories[story][1][k][index])
                            tagAnswer = pos_tag(tokAnswer)
                            p = 0
                            while p < len(tagAnswer):
                                if tagAnswer[p][1] == "VB":
                                    if index == 0:
                                        BestAnswer = "A"
                                    elif index == 1:
                                        BestAnswer = "B"
                                    elif index == 2:
                                        BestAnswer = "C"
                                    elif index == 3:
                                        BestAnswer = "D"
                                    break
                                p = p + 1
                    #refer to rule QA5
                    elif "how" in qTokenized and "many" in qTokenized:
                        for index in dupIndex:
                            tokAnswer = tokenize.word_tokenize(dicOfStories[story][1][k][index])
                            tagAnswer = pos_tag(tokAnswer)
                            p = 0
                            while p < len(tagAnswer):
                                if tagAnswer[p][1] == "CD":
                                    if index == 0:
                                        BestAnswer = "A"
                                    elif index == 1:
                                        BestAnswer = "B"
                                    elif index == 2:
                                        BestAnswer = "C"
                                    elif index == 3:
                                        BestAnswer = "D"
                                    break
                                p = p + 1
            k = k + 1
            #adds the best answer to list for the question set that is currently being looked at
            tempAnswers.append(BestAnswer)
   
        #adds the set of ansers to the final list
        listOfFinalAnswers.append(tempAnswers)
        
    
#write the answers to the answers file, and name it according to what mode and dataset is being used
with open(header+"."+str(mode)+".answers.txt","w") as file:
    for answer in listOfFinalAnswers:
        line = ""
        for letter in answer:
           line = line + letter + "\t"
        line = line[:len(line)-1]
        line = line + "\n"
        file.write(line)

             
