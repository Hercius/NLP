import re
notEndOfFile = True
with open("sentiment-train.txt", "r") as file:
       
        #this grabs each review from the training set, and separates each of its fields into the review class. 
        #This also gives the list of unigrams and bigrams. 
        
            initialReview = file.readline()
            if initialReview:
                text = initialReview.split()
                identity = text[0]
                rank = text[1]
                unigramsList = []
                UnigramReview = initialReview[re.search(".*\.txt\s[0-1]\s",initialReview).end():]
                between = False
                #this loops through the review and adds the not handle to each feature
                indices = [[m.start(0), m.end(0)] for m in re.finditer("(?<=not\s).*?[\.!?]", UnigramReview)]
                startOfWord = True
                startOfWords = []
                for i in indices:

                    count = 0
                    start = i[0]
                    while start < i[1]:
                        if re.match("\w",initialReview[start]) and startOfWord:
                            startOfWord = False
                            startOfWords.append(start)
                        if re.match("\s",initialReview[start]):
                            startOfWord = True
                for j in startOfWords:
                    

                            
                
            print(indices)