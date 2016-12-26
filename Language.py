import sys
import re
import string
import HTMLParser
import urllib2
import datetime
import time

#Create our word key dictionary
keyDict = dict()
PhraseDict = dict()


# # # RECURSIVE SEARCH # # #

def recSpider(url, iterations, searchScope):
    if (iterations >= searchScope):
        return
    #Opens our url target, and copies contents
    try:
        response = urllib2.urlopen(url)
        page_source = response.read()
        #Splits page source by html closing tags
        list = page_source.split('<')
    except:
        return


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

        elif statement.startswith('p>'):
            statement = statement[2:]
            statement = statement.lower()
            PhraseDict[statement] = PhraseDict.get(statement,0) + 1
        elif statement.startswith('title>'):
            statement = statement[6:]
            statement = statement.lower()
            PhraseDict[statement] = PhraseDict.get(statement,0) + 1





# # # Main / Time Trials # # #

#Start Time
start = datetime.datetime.now()

#Origin Point, http://null-byte.wonderhowto.com/
recSpider("https://www.tutorialspoint.com/python/python_functions.htm", 0, 2)
print PhraseDict

#End Time
end = datetime.datetime.now()

#StopWatch
print (end - start)
