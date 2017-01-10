 #!/usr/bin/python
import sys
import re
import string
import HTMLParser
import urllib2
import datetime
import time
import random
import os

# # # # # ARGS TAKEN # # # # # 
# Arg 1: Starting url for search
# Arg 2: Depth of Search
#Create our word key dictionary

ParaDict = { "dummyPhrase" : "dummyHead" }
SentenceDict = dict()
PhraseDict = dict()
KeyDict = dict()
WebList = list()

#Get my prime Url flag
prime = sys.argv[1]
if "www." not in prime:
    div = prime.split('.')
    prime = div[0]
else:
    div = prime.split('.')
    prime = div[1]

# # # RECURSIVE SEARCH # # #

def Spider(prime, url, iterations, searchScope):
    if (iterations >= searchScope):
        return url
    #Opens our url target, and copies contents
    try:
        response = urllib2.urlopen(url)
        page_source = response.read()
        #Splits page source by html closing tags
        list = page_source.split('<')
    except:
        return

    Header = ''
    for statement in list:
        if statement.startswith('a href'):
            #Find a new url target
            newUrl= statement[7:]
            if newUrl.startswith('"http'):
                cutoff = '">'
                newUrl = newUrl.split(cutoff, 1)[0]
                cutoff = '" '
                newUrl = newUrl.split(cutoff, 1)[0]
                newUrl = newUrl[1:]
                if prime in newUrl:
                    if newUrl not in WebList:
                       WebList.append(newUrl)
                       print newUrl
                       Spider(primeUrl, newUrl, iterations+1, searchScope)
                    else:
                        pass
            else:
                pass

# <p> Analysis:
    # 4 Levels of data fragmenting/filtering
    #Level 1: Paragraph Interanlization     : Learning critical thinking and thought organization
    #Level 2: Sentence Internalization     : Learning to construct dialogue
    #Level 3: Phrase Internalization      : Learning basic speech
    #Level 4: Word Internalization       : Learning words
        elif statement.startswith('p>'):
            statement = statement[2:]
            statement = statement.lower()
            ParaDict.update({statement : Header})
            Sentences = statement.split(".|!|?")
            for sentence in Sentences:
                SentenceDict[sentence] = SentenceDict.get(sentence,0) + 1
                Phrases = sentence.split(";|,|:")
                for phrase in Phrases:
                    PhraseDict[phrase] = PhraseDict.get(phrase,0) + 1
                    Keys = phrase.split()
                    for word in Keys:
                        if re.match('^[\w-]+$', word):
                            KeyDict[word] = KeyDict.get(word,0) + 1

# <title> Analysis
        elif statement.startswith('title>'):
            statement = statement[6:]
            statement = statement.lower()
            Header = statement
            fragments = statement.split()
            for word in fragments:
                if re.match('^[\w-]+$', word):
                    KeyDict[word] = KeyDict.get(word,0) + 1



# # # Main / Time Trials # # #

#Start Time
start = datetime.datetime.now()

#Origin Point, github repository
Spider(prime, sys.argv[1], 0, sys.argv[2])


#Write Values to files
def store_results(results, filename):
    with open(filename, "w") as input_file:
        for k, v in results.items():
            line = '{} : {}'.format(k, v) + '\n'
            input_file.write(line)
store_results(ParaDict, "Paradict.txt")
store_results(SentenceDict, "SentenceDict.txt")
store_results(PhraseDict, "PhraseDict.txt")
store_results(KeyDict, "KeyDict.txt")


#End Time
end = datetime.datetime.now()

#StopWatch
print "\nWebsites visited: " + str(len(WebList))
print WebList
print (end - start)
