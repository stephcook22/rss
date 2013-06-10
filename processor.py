import string
import operator
import math
import urllib2
from nltk.corpus import wordnet as wn
from xml.dom import minidom

#Only specific tags are used in some functions, this function deals with that
def getPosfromTag(taggedWord):
    if 'VB' in taggedWord[1]:
            return wn.ADV
            #print item[1]+'vb'
    elif 'AJ' in taggedWord[1]:
            #print item[1]+'aj'
            return wn.ADJ
    else:
            #print item[1]+'noun'
            return wn.NOUN

#Get the similarity of the words from wordnet
#Takes a tuple of words
def wordnetSimilarity(words):
    wnword={}
    for item in words:
        a = wn.synsets(item)
        b = 0
        if len(a) is 0:
            return 0.5
        else:
            for posWord in a:
                word = [lemma.name for lemma in posWord.lemmas]
                #print word
                if(word[0] == item):
                    a = posWord
                    b = 1
                    break
            if (b == 0):
                a = a[0]
                #print a
        wnword[item]=a

    if(wnword[words[0]].path_similarity(wnword[words[1]]) is None):
        if(wnword[words[1]].path_similarity(wnword[words[0]]) is None):
            return 0.5
        else:
            return wnword[words[1]].path_similarity(wnword[words[0]])
    return wnword[words[0]].path_similarity(wnword[words[1]])

#get the url for the feed (using feedlist)
#return the items of the rss feed 
def getXMLItems(feedname):
    address = feedList.getFeedURL(feedname)
    file_request = urllib2.Request(address)
    file_opener = urllib2.build_opener()
    file_object = file_opener.open(file_request)
    file_feed = file_object.read()
    file_xml = minidom.parseString(file_feed)
    #Get the 'items' from the dom
    item_node = file_xml.getElementsByTagName("item")
    return item_node


#get the text from an xml node
def getText(nodelist):
    rc = []
    for node in nodelist:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)

#calculate the euclidean distance from 2 vectors including word weighting and length normalisation
def get_euclidean_dif(vector1, vector2):
    vector1 = list(vector1.items())

    #test data
    #vector1 = [('cricket',1),('is',1),('a',1),('game',1), ('played',1),('by',1),('fools',1),('watched',1),('others',1)]

    vector1.sort()
    vector2 = list(vector2.items())

    #test data same article, doubled length to test normalisation
    #vector2 = [('cricket',2),('is',2),('a',2),('game',2), ('played',2),('by',2),('fools',2),('watched',2),('others',2)]

    #test data, completely different document.
    #vector2 = [('bing',1),('bong',1),('boop',1),('billa',1), ('zac',1),('time',1),('test',1),('shane',1),('red',1)]

    vector2.sort()
    total = 0
    sub1 = 0
    for index, item in enumerate(vector1):
        vector1[index] = (item[0], item[1] * get_word_weight(item))
    for index, item in enumerate(vector2):
        vector2[index] = (item[0], item[1] * get_word_weight(item))

    for item in vector1:
        sub1 = sub1 + (item[1] * item[1])
        #sub1 = sub1 +item[1]
    sub1 = 2 * (sub1)
    sub1 = math.sqrt(sub1)
    for index, item in enumerate(vector1):
        vector1[index] = (item[0], item[1] / sub1)

    sub2 = 0
    for item in vector2:
        sub2 = sub2 + (item[1] * item[1])
        #sub2 = sub2+item[1]
    sub2 = 2 * (sub2)
    sub2 = math.sqrt(sub2)
    for index, item in enumerate(vector2):
        vector2[index] = (item[0], item[1] / sub2)
    #print vector1
    #print vector2
    while vector1 != [] or vector2 != []:
        if vector1 == []:
            total = total + (((vector2[0][1] * vector2[0][1])))
            vector2 = vector2[1:]
        elif vector2 == []:
            total = total + (((vector1[0][1] * vector1[0][1])))
            vector1 = vector1[1:]
        else:
            a = vector1[0]
            #print vector2
            b = vector2[0]
            #print '1: '
            #print a
            #print '2: '
            #print b
            if a[0] == b[0]:
                #print str(a[1]) + ' - ' + str(b[1])
                #print '+ '+str((a[1]-b[1])*(a[1]-b[1]))
                total = total + ((a[1] - b[1]) * (a[1] - b[1]))
                vector1 = vector1[1:]
                vector2 = vector2[1:]
                #print a[0] + ' = '+ b[0]

            elif a[0] < b[0]:
                #print '+ '+str((a[1]*a[1]))
                total = total + (a[1] * a[1])
                vector1 = vector1[1:]
                #print a[0] + ' < '+ b[0]
            else:
                #print '+ '+  str(((b[1])*(b[1])))
                total = total + ((b[1]) * (b[1]))
                vector2 = vector2[1:]
                #print a[0] + ' > '+ b[0]
    #print total
    total = math.sqrt(total)
    #print total
    return total


def get_word_weight(word_tup):
    if word_tup[0] in freqs:
        weight = word_tup[1] / freqs[word_tup[0]]
    else:
        weight = word_tup[1]
        #print float(word_tup[1])
        #print averageDoc
        #weight = float(word_tup[1])/averageDoc
    #print word_tup[0]
    #print weight
    return weight


class FeedList:
    record = {}

    def __init__(self):
        filename = "feedlist.dat"
        #Open the file
        datafile = open(filename, "r")
        #read the first line of the file
        line = datafile.readline()
        #for each line
        while line:
            #split on ;
            data = string.split(line, ';')
            feedname = data[0]
            address = data[1]
            #record the feedname and its address
            self.record[feedname] = address
            line = datafile.readline()

    def getFeedNames(self):
        return list(self.record.keys())

    def getFeedURL(self, name):
        if name in self.record:
            return self.record[name]
        else:
            return None

feedList = FeedList()

averageDoc = None


#Something wrong here..
def getTermFreqs(filename):
    datafile = open(filename, 'r')
    line = datafile.readline()
    record = {}
    #for each line
    while line:
        #split on ;
        data = string.split(line, ' ')
        freq = int(data[1])
        word = data[2]
        #record the feedname and its address
        record[word] = freq
        line = datafile.readline()
    maxim = max(iter(list(record.items())), key=operator.itemgetter(1))[1]
    print(maxim)
    print((maxim / 2))
    global averageDoc
    print(averageDoc)
    averageDoc = maxim / 2
    print(averageDoc)
    for key in record:
        record[key] = float(record[key]) / maxim
    #print record
    return record

freqs = getTermFreqs('lemma.al')


def getAverageDoc():
    global averageDoc
    return averageDoc


class DTWDistance:

    insertScore = 1
    deleteScore = 1
    exchangeScore = 3

    def __init__(self, s, t):

        self.s = s
        self.t = t
        self.i = -1
        self.j = 0
        self.notFinished = True


    def start(self):
        result = [[-1 for x in range(len(self.t))] for x in range(len(self.s))]
        #self.pointer = [[-1 for x in range(len(s) + 1)] for x in range(len(t) + 1)]
        result = self.insert(self.i+1, self.j, result)
        result = self.match(self.i+1, self.j, result)
        result = self.exchange(self.i+1, self.j, result)
        while(self.notFinished):
            address = self.nextItem((self.i,self.j))
            self.i = address[0]
            self.j = address[1]
            #print(('i ' + str(self.i) + self.s[self.i]))
            #print(('j ' + str(self.j) + self.t[self.j]))
            #print((str(result[self.i][self.j])))

            if(self.i is not len(self.s)-1):
                result = self.insert(self.i + 1, self.j, result)
            #print "t len "+ str(len(self.t)-2)
            if(self.j is not len(self.t)-1):
                result = self.delete(self.i, self.j + 1, result)
            if(self.i is not len(self.s)-1 and self.j is not len(self.t)-1):
                result = self.match(self.i + 1, self.j + 1, result)
                result = self.exchange(self.i + 1, self.j + 1, result)

            if((self.j is len(self.t) - 1) and (self.i is len(self.s) - 1)):
                self.notFinished = False

        #print(result)
        return result[self.i][self.j]

    def nextItem(self, address):
        i = address[0]
        j = address[1]
        if(i < (len(self.s) - 1)):
            i = i + 1
            #print('inc i' + str(i))
        else:
            i = 0
            j = j + 1
            #print('inc j' + str(j))
        return (i,j)

    def previousItem(self, address):
        i = address[0]
        j = address[1]
        if(i is 0):
            i = len(self.s) -1
            j = j - 1
        else:
            i = i -1
        return (i, j)

    def insert(self, i, j, result):
        self.insertScore = wordnetSimilarity((self.t[j],self.s[i]))
        #print self.t[j] +self.s[i] + str(self.insertScore)
        #print self.insertScore
        if(result[i-1][j] is -1):
            if(result[i][j] is -1):
                result[i][j] = self.insertScore
            elif(result[i][j]>self.insertScore):
                result[i][j] = self.insertScore
        elif(result[i][j] is -1 or result[i][j] > result[i-1][j] + self.insertScore):
            result[i][j] = result[i-1][j] + self.insertScore

        #print(('insert set' + self.s[i] + self.t[j] + str(result[i][j])))
        return result

    def match(self, i, j, result):
        #print '0'
        if(self.s[i] is self.t[j]):
            if(result[i-1][j-1] is -1):
                if(result[i][j] is -1):
                    result[i][j] = 0
                if( result[i][j]>0):
                    result[i][j] = 0
            elif(result[i][j] is -1 or result[i][j] > result[i - 1][j - 1]):
                result[i][j] = result[i - 1][j - 1]

            #print(('equal set ' + self.s[i] + self.t[j] + str(result[i][j])))
        return result

    def exchange(self, i, j, result):
        self.exchangeScore = wordnetSimilarity((self.t[j],self.s[i]))
        #print self.s[i] + str(self.exchangeScore)
        if(result[i -1][j - 1] is -1 ):
            if(result[i][j] is -1):
                result[i][j] = self.exchangeScore
            if(result[i][j]>self.exchangeScore):
                result[i][j] = self.exchangeScore
        elif(result[i][j] is -1 or result[i][j] > result[i - 1][j - 1] + self.exchangeScore):
            result[i][j] = result[i - 1][j - 1] + self.exchangeScore
        #print(('exchange set ' + self.s[i] + self.t[j] + str(result[i][j])))
        return result

    def delete(self, i, j, result):
        #print len(result)
        #print len(result[i])
        #print i
        #print j
        #print result[i][j]
        self.deleteScore = wordnetSimilarity((self.t[j],self.s[i]))
        #print self.s[i] + str(self.deleteScore)
        if(result[i][j - 1] is -1):
            if(result[i][j] is -1):
                result[i][j] = self.deleteScore
            if ( result[i][j]>self.deleteScore):
                result[i][j] = self.deleteScore
        elif(result[i][j] is -1 or result[i][j] > result[i][j - 1] + self.deleteScore):
            result[i][j] = result[i][j - 1] + self.deleteScore
        #print('delete set' + self.s[i] + self.t[j] + str(result[i][j]))
        return result


