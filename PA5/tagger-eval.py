#Alex Bleth Date: 11/18/2021
#This is a Part of Speech Tagger program that evaluates how well my test program did by comparing it to a gold standard answer set 
# and outputs a confusion matrix for the correctly and incorrectly tagged words and gives the overall accuracy.
#
# an example would be if I read in my test file for mode 0 and compared it to the gold standard for the same set. it would print the tags in alphabetical order,
# and would show the correct and incorrect tags (so DT DT is correct, and DT VB is incorrect) and then prints the accuracy.
#to run this, run this file with the command line options of the correct answer key and the test file that was made from the test program.
#The algorith works like this:
#1. open up the test file
#2. get each line and put it into a list
#3. open up the answer key
#4. get each line and put it into a separate list
#5. for each word tag pair, check to see if it is correct, if so add it to the correct counter
#6. put the word tag pair into the confusion matrix if it is not in there, else add it to the current matrix position (so adding up that particular occurance)
#6. sort the confusion matrix alphabetically
#7. print the confusion matrix
#8. calculate and print the accuracy
import re
import sys
def main():
    # get the files that are being compared
    args = sys.argv[1:]
    keyFile = args[0]
    testFile = args[1]
    #total word count
    wordCount =0
    #correctly tagged word count
    correctCount = 0
    #list holding test results
    testList = []
    #list holding the key results
    keyList = []
    #list holding the tags
    tagList = []
    #confusion matrix
    confusionMatrix = dict()
    #read in the test results
    with open(testFile,"r") as test:
        
            word = test.read()
            
            testList = word.split("\n")
            
           
    
    #read in the key file
    notEndOfFile = True
    with open(keyFile,"r") as key:
       
        word = key.read()
        keyList = word.split("\n")
            
    #for each pair in test list (its parallel to the key list)
    i = 0
    while i < len(testList)-1:
        # get the appropriate word and tag if the word has \/ in it
        if re.search(".*[\\\]/.*/",testList[i]):
            #test tag
            tag1 = re.search("\/\w*$", testList[i]).group(0)[1:]
            tag2 = re.search("\/\w*$", keyList[i]).group(0)[1:]
            if tag1 not in tagList:
                tagList.append(tag1)
            if tag2 not in tagList:
                tagList.append(tag2)
            #if matching, it tagged it correctly and adds it to the count
            if tag1 == tag2:
                correctCount = correctCount + 1
            
            wordCount = wordCount + 1
            #add to the confusion matrix
            if (tag1,tag2) in confusionMatrix:
                confusionMatrix[tag1,tag2] = confusionMatrix[tag1,tag2] + 1
            else:
                confusionMatrix[tag1,tag2] = 1
        #for the rest of words not holding \/ in it
        else:
            
            tag1 = re.search("/.*$", testList[i]).group()[1:]
            tag2 = re.search("/.*$", keyList[i]).group()[1:]
            if tag1 not in tagList:
                tagList.append(tag1)
            if tag2 not in tagList:
                tagList.append(tag2)
            #if matching, it tagged it correctly and adds it to the count
            if tag1 == tag2:
                correctCount = correctCount + 1
            
            wordCount = wordCount + 1
            #add to the confusion matrix
            if (tag1,tag2) in confusionMatrix:
                confusionMatrix[tag1,tag2] = confusionMatrix[tag1,tag2] + 1
            else:
                confusionMatrix[tag1,tag2] = 1
    
        i= i + 1
    #sort the list alphabetically
    tagList.sort()
    #for each tag pair in the confusion matrix, print its count
    for tag3 in tagList:
        for tag4 in tagList:
            if (tag3,tag4) in confusionMatrix:
                print(tag3 + " " + tag4 + " " + str(confusionMatrix[tag3,tag4]))
                
        
      

    #print the total accuracy        
    print("Accuracy: " + str(correctCount/wordCount))


main()