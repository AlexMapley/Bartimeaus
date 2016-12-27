import sys
import re
import string
import HTMLParser
import urllib2
import datetime
import time
import random
import os

#Create our word key dictionary
keyDict = dict()
PhraseDict = { "dummyPhrase" : "dummyHead" }


# # # RECURSIVE SEARCH # # #

def recSpider(url, iterations, searchScope):
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
                recSpider(newUrl, iterations+1, searchScope)
            else:
                pass

        #Statement Learning
        elif statement.startswith('p>'):
            statement = statement[2:]
            statement = statement.lower()
            PhraseDict.update({statement : Header})
            fragments = statement.split()
            for word in fragments:
                if re.match('^[\w-]+$', word):
                    keyDict[word] = keyDict.get(word,0) + 1

        #Title Association
        elif statement.startswith('title>'):
            statement = statement[6:]
            statement = statement.lower()
            Header = statement
            fragments = statement.split()
            for word in fragments:
                if re.match('^[\w-]+$', word):
                    keyDict[word] = keyDict.get(word,0) + 1





# # # Main / Time Trials # # #

#Start Time
start = datetime.datetime.now()

#Origin Point, github repository
recSpider("https://github.com/AlexMapley/Bartimeaus/blob/master/Language.py", 0, 2)
print PhraseDict
print keyDict

#End Time
end = datetime.datetime.now()

#StopWatch
print (end - start)







# # # Speech Interaction # # #
while 1:
    raw_input('[User]: ')
    response = random.choice(PhraseDict.keys())
    #cmd = "say '" + response + "'"
    print response
    #os.system(cmd)
