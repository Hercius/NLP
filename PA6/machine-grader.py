#Alex Bleth Date: 12/08/2021
#
#This is a machine reading comprehension grader that grades how well the machine reader program did. 
# It will compare the answers from the machine reader to the appropriate gold standard answer list based on the two files that are inputed as command line arguements.
#Lastly it will output a file with the score, the machine reader answers, the actual answers, and the number of incorrect answers
#An example would be if I had an answer set from the machine reader used mode 0 on the dev dataset, then I would run the grader with the command line arguement:
# machine-grader.py dev.0.answers.txt mc500.dev.ans
#and it would out put a file that gave the appropriate accuracy followed by what was specified above.
#Here is how the algorithm works:
#1. get the command line arguements
#2. check if this is using dev or test and set header to the appropriate value, same for mode
#3. read in the machine reader answer file and store its contents in a list (guessList)
#4. read in the gold standard answer file and store its contents in another list. (answerList)
#5. for each row in the guessList/answerList do the following:
#6. loop through each each answer for an answer set to see if it is right, if it is add it to the list of correct answers, 
# if not then add it to the list of incorrect answers for the set
#7. write to the gradedd file with the following:
# show the accuracy (totalCorrect/totalAmount)
# for each answer set show the answer set for the machine learner, gold standard, and the amount the machine reader got wrong for the question.

import sys
args = sys.argv[1:]
#get machine reader file
ourFile = str(args[0])
# get gold standard file
AnswerFile = str(args[1])
mode = ""
header = ""
#keeps track of the mode for the file write
if "0" in ourFile:
    mode = "0"
elif "1" in ourFile:
    mode = "1"
#keeps track of the header for the file write
if "dev" in ourFile:
    header = "dev"
elif "test" in ourFile:
    header = "test"
#holds the machine reader answer set
guessList = []
#holds the gold standard answer set
answerList = []
#holds the amount of incorrect answers for each answer set
listOfIncorrect = []
#read in the machine reader's anwers file and put it in the guessList
with open(ourFile,"r") as guesses:
    notEndOfFile = True

    while notEndOfFile:
        guess = guesses.readline()
        if guess:
            guess = guess[:len(guess)-1]
            letters = guess.split("\t")
            guessList.append(letters)
        else:
            notEndOfFile = False

#read in the gold standard anwers file and put it in the answerList
with open(AnswerFile,"r") as answers:
    notEndOfFile = True

    while notEndOfFile:
        answer = answers.readline()
        if answer:
            answer = answer[:len(guess)-1]
            letters = answer.split("\t")
            answerList.append(letters)
        else:
            notEndOfFile = False
counter = 0
i = 0
#loop through each answer set in the list (guessList and answerList are parallel so using the length of guessList works fine)
while i < len(guessList):
    incorrectCount = 0
    j = 0
    #loop through each answer in the answer set (for a given question) and see if the machine reader got it correct,
    #if so add it to the correct amount, if no add it to the incorrect counter
    while j < len(guessList[i]):

        if guessList[i][j] == answerList[i][j]:
            counter = counter + 1
        else: 
            #counts number of incorrect for a given answer set
            incorrectCount = incorrectCount + 1
        j = j + 1
    #add the final count of incorrect answers for each answer set
    listOfIncorrect.append(incorrectCount)
    i = i + 1
#preps the top line of the file with the accuracy
topLine = "mode " + mode + " accuracy: " + str(counter/(len(guessList)*4.0)) +"\n"
#write to the graded file
with open(header+"."+mode+".graded.txt", "w") as file:
    file.write(topLine)
    k = 0
    #these 3 loop puts the answers in the correct format of: A A A A | A A A A | 0
    while k < len(guessList):
        line = ""
        m = 0
        while m < len(guessList[k]):
            line = line + str(guessList[k][m]) + "\t"
            m = m + 1
        m = 0
        line = line + "|" + "\t"
        while m < len(answerList[k]):
            line = line + str(answerList[k][m]) + "\t"
            m = m + 1
        line = line + "| " + str(listOfIncorrect[k]) + "\n"
        #write to the graded file
        file.write(line)

        k = k+1