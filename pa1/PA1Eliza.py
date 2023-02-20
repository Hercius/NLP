#Written by: Alex Bleth
#Date: 9/22/2021
#This is an Eliza based chatbot that takes the role of a career councilor. 
#It is able to handle user input and generate an appropriate response that would be plausible.
#an example of this would be if I wrote "I am unsure of my major" Then Eliza would ask them about their major.
#The algorith works like this:
#1. it starts off by asking for their name, in which Eliza can recognize their name from different ways of inputing it
#2. Then it asks the user as to how it can help them (From here on the program loops until the user writes exit)
#3. The user will write their response, and it will be immediately scanned to see if it uses negative or positive language.
#4. After this it checks to see if the user mentions their major (as it generally is a common problem)
#5. if yes, then it will record their major.
#6. Otherwise it go through the list of regex's and see if any match, and if they do it will respond with a transformation.
#7. if the language seems uncertain, then it will ask them about it.
#8. Eliza will switch the conversation after the user says something that is either repeated or is not accounted for.
#9. when the conversation is switched it will record the answer to the new question.
# 10. if eliza runs out of questions then it recalls in memory what the user has given as a response to a previous question.
# 11. lastly if all else fails eliza will say it does not understand and get another input from the user. 
import re;
import random;
#This class is used for creating a ranking for the level of emotion a given word has,
# which is why it has two variables, rank and word.
class wordRanked:
     def __init__(self,w,r):
        self.word = w
        self.rank = r
#This class is used to create what are called the forwarding questions.
#These are the questions that are asked when Eliza determines to change to a different topic
class question:
     def __init__(self,q,a):
        self.questionAsked = q
        self.hasBeenAsked = a

#These two lists hold the positive and negative words respectively that eliza will look out for as emotionally charged. 
listOfPositiveWords = [wordRanked('.*[hH]appy.*',1),wordRanked('.*[eE]xcited.*',2),wordRanked('.*[eE]njoy.*',1),wordRanked('.*[pP]assionate.*',3), wordRanked('.*[eE]ncouraged.*',2), wordRanked('.*[sS]mile.*',1),wordRanked('.*[hH]elpful.*',1),wordRanked('.*YES.*',3)]
listOfNegativeWords = [wordRanked('.*[sS]ad.*',-1),wordRanked('.*[uU]pset.*',-1),wordRanked('.*[aA]ngry.*',-2),wordRanked('.*[sS]tupid.*',-3), wordRanked('.*[aA]nnoying.*',-2), wordRanked('.*[mM]ean.*',-1),wordRanked('.*[hH]ate.*',-2),wordRanked('.*[uU]nhappy.*',-2)]
#This function just looks at the phrase and sees if it is overall positively or negatively charged.
#It looks at the phrase and sums up the rankings of any keywords present to determine its emotion level and returns a number.
#If the number is positive, the phrase is positively charged, if it is negative, it is negatively charged, otherwise if it returns 0 it is a neutral phrase.
def calcEmotion(phrase):
    emotionLevel = 0
  
    for sWord in listOfPositiveWords:
        if(re.search(sWord.word,phrase)):
           emotionLevel += sWord.rank
    for sWord in listOfNegativeWords:
        if(re.search(sWord.word,phrase)):
            emotionLevel += sWord.rank
    return emotionLevel

    
def main():
    #This is called when eliza either doesn't have a response to what is said, or in case of repetition. 
    # This will pull from the list of forwarding questions, and if all forwarding questions have been asked, then it will recall their responses
    # to previous questions and ask them about their responses. 
    def forwardConvo():
        i = 0
        while(i < len(forwardingQuestions) and forwardingQuestions[i].hasBeenAsked == True):
            i += 1

        if(i == len(forwardingQuestions)):
            return ('earlier you brought up '+ random.choice(responsesToFQuestions)+ ' Can tell me what impact this has on your career?')
        else:
            forwardingQuestions[i].hasBeenAsked = True
            return forwardingQuestions[i].questionAsked
    #This function is called when a forwarding question has just been asked. 
    # It will take the user's response in as well as the current question.
    #it will also save their responses in a way that primes them for when they are recalled.
    #After saving their answers it will ask the question associated with how they answered.

    def recordAnswer(userInput,currentElizaAnswer):
                i = 0
                while(i < len(forwardingQuestions) and not currentElizaAnswer == forwardingQuestions[i].questionAsked):
                    i += 1
                       
                if(re.search(n2,userInput)):
                    responsesToFQuestions[i] = re.findall(n2,userInput)[0]
                    if(forwardingQuestions[0].questionAsked == currentElizaAnswer):
                        responsesToFQuestions[i] = 'your major is ' + responsesToFQuestions[i]
                    elif(forwardingQuestions[1].questionAsked == currentElizaAnswer):
                        responsesToFQuestions[i] = 'you were from ' + responsesToFQuestions[i]
                    elif(forwardingQuestions[2].questionAsked == currentElizaAnswer):
                        responsesToFQuestions[i] = 'you like ' + responsesToFQuestions[i]
                    
                elif(re.search(n3,userInput)):
                    responsesToFQuestions[i] = re.findall(n3,userInput)[0]
                    if(forwardingQuestions[0].questionAsked == currentElizaAnswer):
                        responsesToFQuestions[i] = 'your major is ' + responsesToFQuestions[i]
                    elif(forwardingQuestions[1].questionAsked == currentElizaAnswer):
                        responsesToFQuestions[i] = 'you were from ' + responsesToFQuestions[i]
                    elif(forwardingQuestions[2].questionAsked == currentElizaAnswer):
                        responsesToFQuestions[i] = 'you like ' + responsesToFQuestions[i]
                if(re.search(n2,userInput)):
                    reg = re.sub('[.!?].*', '?', userInput)
                    reg = re.sub('[mM]y','your', reg)
                    reg = re.sub('is\s','',reg)
                    previousElizaAnswer = currentElizaAnswer
                    currentElizaAnswer = strBuilder + 'Why is ' + reg
                    print(currentElizaAnswer)
                    wasForwarding = False
                elif(re.search(n3,userInput)):
                    reg = re.sub('[.!?].*', '?', userInput)
                    previousElizaAnswer = currentElizaAnswer
                    currentElizaAnswer = strBuilder +'What can you tell me about ' + reg
                    print(currentElizaAnswer)
                    wasForwarding = False
    
    #Eliza question bank. This is a mix of prefixes of eliza questions, as well as fully fleshed out questions.
    #aditionally it has the language reminder, which will append the persons name to the beginning of the sentence.
    prefixQuestion = 'Why do you say '
    languageReminder = ', try not to be negative, can you rephrase your sentence in a nicer tone?'
    happyResponse = 'I am glad that you seem positve! '
    forwardingQuestions = [question('What is your major?',False),question('Where are you from?',False), question('what class do you like the most?', False)]
    likeQuestion = 'why do '
    #regex section
    #These are my regex's that look for the patterns specifically for the words that are said before the word pattern.
    #Example: IMyPattern will look for phrases that have sentences that use I and my in them.
    #This also contains the regex for words/phrases of uncertainty, meaning that if one of them is inputed, 
    # Eliza will recognize they are uncertain.
    IMyPattern = "[iI]\s(\w+\s*\w*)+\smy\s(\w+\s*\w*)+[.!?]{1}"
    youYourPattern = "[yY]ou+\s\w+\syour\s(\w+\s*\w*)+[.!?]{1}"
    canYouPattern = '(\w*\s)*can\syou\s.+[.!?]{1}'
    ILikePattern = '[iI]\s(\w+\s*\w*\s*)*like\s(\w+\s*\w*)+[.!?]{1}'
    itmePattern = '[iI]t\s(\w+\s*\w*)*\s*me\s(\w+\s*\w*)+[.!?]{1}'
    uncertaintyPattern = "([uU]nsure | [dD]o not know | [cC]an't think of | [nN]ot sure | don't know)+"
    fromPattern = 'I\s\w+am\sfrom\w+[.!?]{1}'
    IAmPattern = 'I\s(\w+\s*\w*)*am\s*[.!?]{1}'
    arePattern = '\w*\sare\s\w+[.!?]{1}'
    IPattern = 'I\s(\w+\s*\w*)+[.!?]{1}'
    itisPattern = '[iI]t\sis\s(\w+\s*\w*)+[.!?]{1}'
    #regex's for user's name/my is questions
    n1 = "[Mm]y\s\w+\sis\s\w+.*me\s(\w+\s*\w*)[.!?]{1}"
    n2 = "[Mm]y\s\w+\sis\s(\w+\s*\w*)[.!?]{1}"
    n3 = "^(\w+\s*\w*[.?!])$"
    #after first answer, this is where user input will be stored
    userInput = ''
    #this is where it stores last input, this allows eliza to check for repetition of Eliza.
    previousElizaAnswer = ''
    currentElizaAnswer = '1'
    #This list holds the users responses to forwarding questions.
    responsesToFQuestions = ['','','','']
    #this check is to see if the previous question was answered, another way to avoid Eliza from not responding with anything.
    wasAnswered = False
    #this check is for Eliza to know if the question it just asked was a forwarding question,
    #and if it is, to record their response.
    wasForwarding = False
    #start of program
    print(" Hi, I'm Eliza the Career Counselor. I'm a chatbot written by Alex Bleth.")
    print("Let's get started, what is your name?")
    name = input()
    #captures username
    if(re.match(n1,name)):
        
        name = re.findall(n1,name)[0]
        re.sub('[!.]','', name)
    elif(re.match(n2,name)):
        
        name = re.findall(n2,name)[0]
        re.sub('[!.]','', name)
    elif(re.match(n3,name)):
        
        name = re.findall(n3,name)[0]
        re.sub('[!.]','', name)
    print('Hello ' + name + " what brings you in today?")
    #This is the main portion of Eliza. it will run till the user says exit.
    while(userInput != 'exit'):
        strBuilder = ''
        #This is the emotion level variable, it is reset after each new input.
        lvl = 0
        userInput = input()
        previousInput = userInput
        #gets the users emotional level in the sentence.
        lvl = calcEmotion(userInput)
        print('> '+ userInput)

        if(lvl > 0):
            strBuilder = happyResponse
        #This is the only forwarding question that has its own check.
        #this is do to the fact that the user might bring up their major right away, so Eliza will ask them what it is for later use.
        if(re.search('major',userInput) and forwardingQuestions[0].hasBeenAsked == False):
            forwardingQuestions[0].hasBeenAsked = True
            print(forwardingQuestions[0].questionAsked)
            wasForwarding = True
            previousElizaAnswer = currentElizaAnswer
            currentElizaAnswer = forwardingQuestions[0].questionAsked
        #prints out language reminder if sentence is overall negative
        elif(lvl < 0):
            print(name + languageReminder)
        #This will answer any my ... is responses, and any one word responses. 
        #This will also print out the gibberish detection if it wasn't a real sentence.
        elif(re.search(n2, userInput) or re.search(n3,userInput)):
            wasAnswered = True
            
            if(wasForwarding):
                recordAnswer(userInput,currentElizaAnswer)
                   
            elif(re.search(n2, userInput)):
                reg = re.sub('[.!?].*', '?', userInput)
                reg = re.sub('[mM]y','your', reg)
                reg = re.sub('is\s','',reg)
                previousElizaAnswer = currentElizaAnswer
                currentElizaAnswer = strBuilder + 'Why is ' + reg
                print(currentElizaAnswer)
                wasForwarding = False
            elif(re.search(n3,userInput)):
                reg = re.sub('[.!?].*', '?', userInput)
                previousElizaAnswer = currentElizaAnswer
                currentElizaAnswer = 'What can you tell me about ' + reg
                print(currentElizaAnswer)
                wasForwarding = False
        #Answers any it .. is sentences
        elif(re.search(itisPattern,userInput)):
            wasAnswered = True
            reg = re.sub('[.!?].*', '?', userInput)
            reg = re.sub('my','your', reg)
            previousElizaAnswer = currentElizaAnswer
            currentElizaAnswer = strBuilder + 'why do you say ' + reg
            print(currentElizaAnswer)
            wasForwarding = False 
           #This is the case for when the user sounds uncertain

        elif(re.search(uncertaintyPattern,userInput)):
            wasAnswered = True
            previousElizaAnswer = currentElizaAnswer
            currentElizaAnswer = name + ', you sound uncertain, why is that?'
            print(currentElizaAnswer)
            wasForwarding = False         
        #this will answer any sentences that use are, but no other keywords.
        elif(re.search(arePattern,userInput)):
            wasAnswered = True
            reg = re.sub('[.!?].*', '?', userInput)
            reg = re.sub('are\s', '', reg)            
            previousElizaAnswer = currentElizaAnswer
            currentElizaAnswer = strBuilder + 'why are ' + reg
            print(currentElizaAnswer)
            wasForwarding = False 
        #This is for when the user says it and me in the sentence
        elif(re.search(itmePattern,userInput)):
            wasAnswered = True
            reg = re.sub('[.!?].*', '?', userInput)
            reg = re.sub('me', 'you', reg)            
            previousElizaAnswer = currentElizaAnswer
            currentElizaAnswer = strBuilder + 'why does ' + reg
            print(currentElizaAnswer) 
            wasForwarding = False
        
         #This is for when the user says I and am in the sentence
        elif(re.search(IAmPattern,userInput)):
            wasAnswered = True
            reg = re.sub('[!.?].*', '?', userInput)
            reg = re.sub('^I', 'you ', reg)  
            reg = re.sub('\sam\s','', reg)
            reg = re.sub('\smy\s','your',reg)
            previousElizaAnswer = currentElizaAnswer
            currentElizaAnswer = strBuilder + 'why does ' + reg
            print(currentElizaAnswer)
            wasForwarding = False

         #This is for when the user says I and like in the sentence
        elif(re.search(ILikePattern,userInput)):
            wasAnswered = True
            reg = re.sub('[!.?].*', '?', userInput)
            reg = re.sub('(\w*\s*)*I\s', 'you ', reg)

            previousElizaAnswer = currentElizaAnswer
            currentElizaAnswer = strBuilder + likeQuestion + reg
            print(currentElizaAnswer)
            wasForwarding = False
        #This is for when the user says I and My
        elif(re.search(IMyPattern,userInput)):
            wasAnswered = True
            reg = re.sub('[!.?].*', '?', userInput)
            reg = re.sub('^[iI]', 'you', reg)
            reg = re.sub('my', 'your', reg)
            reg = re.sub('am', 'are', reg)
            previousElizaAnswer = currentElizaAnswer
            currentElizaAnswer = strBuilder + prefixQuestion + reg
            print(currentElizaAnswer)
            wasForwarding = False
        #This is for when the user says you and your
        elif(re.search(youYourPattern,userInput)):
            wasAnswered = True
            reg = re.sub('[.!?].*', '?', userInput)
            reg = re.sub('^[yY]ou', 'I', reg)
            reg = re.sub('your', 'my', reg)
            previousElizaAnswer = currentElizaAnswer
            currentElizaAnswer = strBuilder + prefixQuestion + reg
            print(currentElizaAnswer)
            wasForwarding = False
        #This is for when the user says can and you   
        elif(re.search(canYouPattern,userInput)):
            wasAnswered = True
            reg = re.sub('[.!?].*', '?', userInput)
            reg = re.sub('^[yY]ou', 'I', reg)
            previousElizaAnswer = currentElizaAnswer
            currentElizaAnswer = strBuilder + prefixQuestion + reg
            print(currentElizaAnswer)
            wasForwarding = False
        #This is a catch all I regex, in case they say something that has I, but no other keywords captured above
        elif(re.search(IPattern,userInput)):
            wasAnswered = True
            reg = re.sub('[.!?].*', '?', userInput)
            reg = re.sub('I', 'you', reg)
            previousElizaAnswer = currentElizaAnswer
            currentElizaAnswer = strBuilder + 'why do ' + reg
            print(currentElizaAnswer)            
            wasForwarding = False
       
                    
        
        #Exit Eliza Check
        elif(userInput == 'exit'):
            print('goodbye')
        #check to see if the question was answered, and no meaningful input was entered 
        elif(wasAnswered == True and not re.match('^\w+$', userInput)):
            wasAnswered = False
            wasForwarding = True
            currentElizaAnswer = forwardConvo()
            print(currentElizaAnswer)
        #if all else fails eliza with say she does not understand the person and ask them to rephrase.
        else:
            previousElizaAnswer = currentElizaAnswer
            currentElizaAnswer = "Sorry I cannot understand you, can you rephrase what you said?"
            print(currentElizaAnswer)
            wasForwarding = False
        #lastly this checks for repetion of eliza, so if she does repeat herself, she changes topics
        if(currentElizaAnswer == previousElizaAnswer):
            wasForwarding = True
            currentElizaAnswer = forwardConvo()
            print(currentElizaAnswer)
            
main()