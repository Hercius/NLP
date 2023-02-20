#Alex Bleth October 7, 2021
#This program will take in n (the ngram amount, so 2 would be a bigram for instance), 
# m, the number of sentences to be printed out
#and any amount of books as arguments to create randomly generated sentences from the books pulled.
# 
# for example, If I use n = 3, m = 10 and Dracula.txt and Gatsby.txt 
# (I have more, but for the example these is what I will use), this program will generate 10 sentences, 
# with using trigrams that are found from the books uses.

import random
import sys, getopt
import re
def main():
    #This is a helper function that can generate random ngrams 
    #(I just use this for my trigram, it gives me a starting bigram to work off of)
    def generateNgrams(words_list, n):
        ngrams_list = []
 
        for num in range(0, len(words_list)):
            ngram = ' '.join(words_list[num:num + n])
            ngrams_list.append(ngram)
        return ngrams_list
 
    #This section removes the first arguement (the python file), and gets n and m from the arguements
    args = sys.argv[1:]
    n = int(args[0])
    args = args[1:]
    m = int(args[0])
    args = args[1:]
    #This boolean will flip to false when a .?! is used at the end of a sentence
    sentenceIsNotOver = True
    #sentence that will be generated
    ngram = ""
    #this boolean is to check if it is the first time through the creating sentence loop
    #this allows the program to set up the sentence for the appropriate ngram
    isFirstTime = True
    #if the first time through has a .?! in the first or second word, 
    # it is generally not a good sentence, so it just ignores it.
    doPrint = True
    #counts the number of sentences
    count = 0
    #this will store my corpus from the books that I pulled from
    words = []
    #This the first word that is generated (and then cycled from the third to the second to the first regarding trigrams and bigrams)
    firstWord = ""
    #intial string of all the books added together
    book = ""
    
    #this will open each book, append the contents to the corpus, then put each word in its own indice in an list
    for i in args: 
        with open(i,"r") as file:
            book = book + " " + file.read()

    words = list(map(str, book.split()))
    print(words)

    print("This program generates " + str(m) + " random sentences based on a " + str(n) + "-gram model. CS 5242 by Alex Bleth\n")
    #this loop keeps track of sentence generation
    while count < m:
        #resets my boolean variables
        sentenceIsNotOver = True
        isFirstTime = True
        doPrint = True
        #increment the count
        count = count + 1    
        #this will randomly generate the first word, used for bigram and monogram model
        firstWord = random.choice(words)
       #this will generate my sentence 
        while sentenceIsNotOver:
        #If the ngram model is 1, then it will print the monogram model
            if n == 1:
                if isFirstTime:
                
                    ngram = firstWord
                    isFirstTime = False
                elif firstWord == "." or firstWord == "?" or firstWord == "!":    
                    ngram = ngram + firstWord
                    sentenceIsNotOver = False
                elif firstWord == ",":
                    ngram = ngram + firstWord
                elif len(firstWord) == 1 and not firstWord == 'i' and not firstWord == "a":
                    ngram = ngram + random.choice(words)
                else:
                    ngram = ngram + " " + firstWord
                firstWord = random.choice(words)
        #If the ngram model is 2, then it will print the bigram model    
            if n == 2:
                #This iterates through my corpus to find all of the positions of the first word
                indices = [i for i, x in enumerate(words) if x == firstWord]
                #since I have all the postions of the first word, I can just grab the position of the word from a random spot in my corpus
                rIndex = random.choice(indices)
                #Adding one to the position just moves the index to match with the second word 
                # (essentially given the position of the first word, the second word is the word in following position)
                rIndex = rIndex + 1
                secondWord = words[rIndex]
                #checks if this sentence is a false start (like a sentence starting with .!?)
        
                if isFirstTime and (firstWord == "." or firstWord == "!" or firstWord == "?" or firstWord == ","): 
                    ngram = ngram + secondWord
                    firstWord = secondWord
                    sentenceIsNotOver = False
                    isFirstTime = False
                    doPrint = False
                    count = count - 1
                elif isFirstTime:
                
                    isFirstTime = False
                #These elif's either end the sentence, or attach the words appropriately to the model.
                elif firstWord == "." or firstWord == "!" or firstWord == "?":
                    sentenceIsNotOver = False

                
                elif secondWord == "." or secondWord == "!" or firstWord == "?":
                    ngram = ngram + secondWord
                    sentenceIsNotOver = False
                  
                elif firstWord == ",":
                    ngram = ngram  + " " + secondWord
                
                elif secondWord == ",":
                    ngram = ngram +  secondWord
                
                else:
                    ngram = ngram + " " + secondWord
                
                #This moves the second word into the first word to set up the next bigram
                firstWord = secondWord
            #if n is 3, then it will print trigrams
            if n == 3:
                #This will a grab a random bigram to start off with if it is the first time
                if isFirstTime:
                    grabbed = generateNgrams(words,2)
                    bigram = random.choice(grabbed)
                
                    individualWords = bigram.split()
                    #sets the first and second word from the bigram
                    firstWord = individualWords[0]
                    secondWord = individualWords[1]
                    #this checks for a "false start" again, so if it starts with a punctuation, just get rid of it.
                    if firstWord == ',' or firstWord == '.' or firstWord == '?' or firstWord == '!' or secondWord == ',' or secondWord == '.' or secondWord == '?' or secondWord == '!':
                        sentenceIsNotOver = False
                        count = count - 1
                        doPrint = False

                    ngram = ngram + firstWord + " " + secondWord          
                    isFirstTime = False
                #This with get all of the locations of the first word and second word, and store those locations in two separate arrays
                indices = [i for i, x in enumerate(words) if x == firstWord]
                indices2 = [i for i, x in enumerate(words) if x == secondWord]
                indices3 = []
                #This will then cross reference the locations of the first word and the second word. 
                # so if the second word location is following the first words location, add the location of the secondword location plus one
                #This essentially creates a list of all the locations of the words that follow the given 2 words
                for i in indices2:
                    try:
                        if indices.index(i - 1) >= 0:
                            indices3.append(i + 1)
                    except:
                        continue
                #this will then grab the third word of the trigram based off the given two first words.
                thirdWord = words[random.choice(indices3)]
                #checks to see if the sentence is over
                if firstWord == "." or firstWord == "!" or firstWord == "?" or secondWord == "." or secondWord == "!" or secondWord == "?":
                    sentenceIsNotOver = False
                    ngram = ngram + firstWord
                elif secondWord == "." or secondWord == "!" or secondWord == "?":
                    sentenceIsNotOver = False
                    ngram = ngram + secondWord
                elif thirdWord == "." or thirdWord == "!" or thirdWord == "?":
                    sentenceIsNotOver = False
                    ngram = ngram +  thirdWord
           
                elif not firstWord == ',' and not secondWord == ',' and thirdWord == ',':
                    ngram = ngram + thirdWord

                #if the sentence is continueing, set the first word to the second, and the third to the second.
                #This allows the trigram model to continue
                else:
                    ngram = ngram +  " " + thirdWord
                firstWord = secondWord
                secondWord = thirdWord
        #these just check for comma spaces, it just ensures the comma is in the right place.
        ngram = re.sub(" , ", ", ", ngram)    
        ngram = re.sub(",,", ",", ngram)
        #If a valid sentence (no false start), print the sentence.
        if doPrint:
            print(str(count) + ": " + ngram)
            print("\n")
        ngram = ""
        

main()