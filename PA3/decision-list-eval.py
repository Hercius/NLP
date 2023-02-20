#Alex Bleth Date: 10/20/2021
#This program is associated with the training and tester programs to 
# evalute how well the decision list did at classifying the reviews by comparing it to the gold standard.
# to run this simply run the file, and you can change the systems classified file and gold standard file if you want to evaluate other data.
# an example of this running would be is that it takes the classified data and compares it to the actual classification of the data and evalutes its accuracy, precision, and recall.
# The algorithm works like this:
# 1. open up the system answers classification and store them.
# 2. open up the correct answers and store them.
# 3. for each review check to see if it was a correct classification, if yes add to the total correctly classified for its given class.
# 4. if it is not correctly classified, then add to the total of incorrect classifications for its given class.
# 5. compute the accuracy, precision, and recall of the overall program.
# 6. store the results in a results file
def main():
    classifiedRanks = []
    actualRanks = []
    idList = []
    truePositives = 0
    trueNegatives = 0
    falsePositives = 0
    falseNegatives = 0
    notEndOfFile = True
    #this opens up the classified file
    with open("sentiment-system-answers.txt","r") as classified:
        while notEndOfFile:
            classification = classified.readline()
            if classification:
                rank = classification.split()[1]
                classifiedRanks.append(rank)
            else:
                notEndOfFile = False
    notEndOfFile = True
    #this opens up the gold standard file
    with open("sentiment-gold.txt","r") as classified:
        while notEndOfFile:
            classification = classified.readline()
            if classification:
                rank = classification.split()[1]
                id = classification.split()[0]
                actualRanks.append(rank)
                idList.append(id)
            else:
                notEndOfFile = False
    #this writes the final results file, by checking the classified rank to the actual rank and tallying the correct and incorrect responses
    correctCount = 0
    counter = 0
    with open("sentiment-system-answers-scored.txt","w") as score:
        while counter < len(classifiedRanks):
            score.write(idList[counter] + " " + actualRanks[counter] + " " + classifiedRanks[counter] + "\n")  
            if classifiedRanks[counter] == actualRanks[counter]:
                correctCount = correctCount + 1
                if actualRanks[counter] == "1":
                    truePositives = truePositives + 1
                if actualRanks[counter] == "0":
                    trueNegatives = trueNegatives + 1

            else:
                if actualRanks[counter] == "1":
                    falseNegatives = falseNegatives + 1
                elif actualRanks[counter] == "0":
                    falsePositives = falsePositives + 1
                  
            counter = counter + 1
        #this calculates the accuracy, precision, and recall and then adds it to the bottom of the score file
        accuracy = "accuracy: " + str(correctCount/counter) + "\n"
        precision = "precision: " + str(truePositives/(truePositives+falsePositives)) + "\n"
        recall = "recall: " + str(truePositives/(truePositives+falseNegatives)) 
        score.write(accuracy + precision + recall)
    
main()