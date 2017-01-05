import sys
import re
import string
import HTMLParser
import urllib2
import datetime
import time
import random
import os
import collections

#Create our word key dictionary

ParaDict = { "dummyPhrase" : "dummyHead" }
SentenceDict = dict()
PhraseDict = dict()
KeyDict = dict()


# # # RECURSIVE SEARCH # # #

def Spider(url, iterations, searchScope):
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
                print newUrl
                Spider(newUrl, iterations+1, searchScope)
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
            #Sentences = re.split('. |! |?  ', statement)
            Sentences = statement.split(".|!|?")
            #Sentences = statement.replace(',',' ').replace('.',' ').replace('?',' ').split()
            for sentence in Sentences:
                SentenceDict[sentence] = SentenceDict.get(sentence,0) + 1
                Phrases = sentence.split(";|:")
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
Spider("https://github.com/AlexMapley/Bartimeaus/blob/master/LanguageCollector.py", 0, 3)



# # # # Inneficient & Incomplete Dictionary Sorting # # # #
    #Should be sending out raw data for later Sorting
#Do this sorting in an R environment??
#from collections import OrderedDict
#SentenceDict = OrderedDict(sorted(SentenceDict.items(),
#                                  key=lambda kv: kv[1]['K'], reverse=True))
#PhraseDict = OrderedDict(sorted(PhraseDict.items(),
#                                  key=lambda kv: kv[1]['K'], reverse=True))
#KeyDict = OrderedDict(sorted(KeyDict.items(),
#                                  key=lambda kv: kv[1]['K'], reverse=True))

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
print (end - start)
