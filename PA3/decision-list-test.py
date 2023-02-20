#Alex Bleth Date: 10/20/2021
#This is a decision-list tester that is paired with the decision-list train file. 
# It takes in the decision list made from the file that was made by the decision-list train file and uses the decision list to classify each review in a test file.
# it will then output its classifications with the appropriate review to an answer file.
# an example would be you get a review, and the first word in the decision list is found in the review, the review is classified based on that words classification.
# the algorith works like this:
# 1. take in the decision list, and separate out the parts into their apropriate section (so word, loglikelihood and rank)
# 2. next it opens up the test data and prepares the review to be classified against by adding the not handles to the appropriate words in the review.
# 3. it will then run down the decision list for each review and classify the review based on a word(or bigram) that was found in the review
# 4. it then writes to a file that contains the identifier, and its classification for each review 

import re
#This holds the word, loglikely, and the rank
class sentimentDecision:
    def __init__(self,word,logLikely,rank):
        self.word = word
        self.likely = logLikely
        self.rank = rank
def main():
    decisionList = []
    notEndOfFile = True
    identifierAndReview = []
    classifiedReview = []
    reviewList = []
    newReview = []
    newReviewsList = []
   
    between = False
    count = 0
    #this opens up the decision list and gets its values by spliting them into their apropriate parts
    with open ("sentiment-decision-list.txt","r") as decisionListFile:
        while notEndOfFile:
            decision = decisionListFile.readline()
            if decision:
                wordPosi = re.search("(?=[0-9]\.)", decision).start()
                word = decision[:wordPosi-1]
                log = re.search("[0-9]\.\w+", decision).group(0)
                rank = re.search("[0-9]$",decision).group(0)
                decisionList.append([str(word),log,rank])
            else:
                notEndOfFile = False

    #this opens up the test data and prepares the review to be referenced
    notEndOfFile = True
    
    with open("sentiment-test.txt","r") as test:
        while notEndOfFile: 
            between = False
            testData = test.readline()
            if testData:
                fileName = re.search("^.+.txt",testData).group(0)
                review = re.search("(?<=__\s).*",testData).group(0)
                notHandles = review.split()
               #this preps the test review with the not handlers so that the decision list can classify the review     
                for i in notHandles:
                    if i == "." or i == "!" or i == "?":
                        between = False
                    if between:
                        i = "not_"+ i
                        
                    if i == "not" or i == "can't" or i == "isn't" or i =="aren't" or i == "won't":
                        between = not between
                    newReview.append(i)
                    
                identifierAndReview.append([fileName,' '.join(newReview)])
                newReview = []
            else:
                notEndOfFile = False
    #this loop is where it goes down the decision list for each review and classifies it.
    for review in identifierAndReview:
        count = 0
        givenReview = str(review[1])
    
        while count < len(decisionList):
        
            if re.search("\s"+re.escape(decisionList[count][0])+"\s",givenReview):
                print("classified on: " + re.search("\s"+decisionList[count][0]+"\s",givenReview).group(0) + "\n" + decisionList[count][0])
                break
            count = count + 1
        if count < len(decisionList):
            classifiedReview.append([review[0],decisionList[count][2]])
        else:
            print("could not be classified")
    #this writes the file that holds all of the classified reviews
    with open("sentiment-system-answers.txt","w") as output:
        for review in classifiedReview:
            output.write(review[0] + " " + review[1] + "\n")
    
main()