 #!/usr/bin/python
import sys
import re
import string
import urllib2
import datetime
import time
import random
import os

# # # # # ARGS TAKEN # # # # # 
# Arg 1: Starting url for search
# Arg 2: Depth of Search
#Create our word key dictionary

# # # # # ARG Error Exceptions # # # # #
if (len(sys.argv) < 3):
    print "\n\nERROR: 2 arguments are required:\nThe starting http:// site,"
    print "and an integer defining search depth (For testing, choose a low number <=2)\n\n"
    sys.exit()

if "http" not in sys.argv[1]:
    print "\n\nERROR: It's required that your starting site begins with either"
    print "http:// or https://"
    print "That's just how the web parser syntax works\n\n"
    sys.exit()


# # # # Flag Arguments # # # #

# # # # Creating my Archives # # # # #
ParaDict = { "dummyPhrase" : "dummyHead" }
WebList = list()


#Get my prime Url flag
prime = sys.argv[1]
if "www." not in prime:
    div = prime.replace('//',' ').replace('.',' ').split()
    prime = div[1]
else:
    div = prime.replace('//',' ').replace('.',' ').split()
    prime = div[2]

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
                       print newUrl
                       WebList.append(newUrl)
                       Spider(prime, newUrl, iterations+1, searchScope)
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

# <title> Analysis
        elif statement.startswith('title>'):
            statement = statement[6:]
            statement = statement.lower()
            Header = statement



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


#End Time
end = datetime.datetime.now()

#StopWatch
print "\nWebsites visited: " + str(len(WebList))
print WebList
print (end - start)
