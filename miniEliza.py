import re
def main ():
    prefixQuestion = '< why do you say '
    iPattern = "[iI]+\s\w+\smy\s(\w+\s*\w*)+[.!?]{1}"
    yPattern = "[yY]ou+\s\w+\syour\s(\w+\s*\w*)+[.!?]{1}"
    wPattern = "[wW]e+\s\w+\sour\s(\w+\s*\w*)+[.!?]{1}"
    userInput = ''
    print('< Hello, Please talk to me')
    while(userInput != 'exit'):
        userInput = input()
        print('> '+ userInput)
        if(re.search(iPattern,userInput)):
            reg = re.sub('[.].*', '?', userInput)
            reg = re.sub('^[iI]', 'you', reg)
            reg = re.sub('my', 'your', reg)
            
            print(prefixQuestion + reg)
            
        elif(re.search(yPattern,userInput)):
            reg = re.sub('[.!?].*', '?', userInput)
            reg = re.sub('^[yY]ou', 'I', reg)
            reg = re.sub('your', 'my', reg)
           
            print(prefixQuestion + reg)
            
        elif(re.search(wPattern,userInput)):
            reg = re.sub('[.!?].*', '?', userInput)
            reg = re.sub('^[wW]e', 'you', reg)
            reg = re.sub('our', 'your', reg)
            print(prefixQuestion + reg)
        elif(userInput == 'exit'):
            print('goodbye')
        else:
            print("Tell me more")
    
main()
