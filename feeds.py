import nltk.data
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet as wn
from boilerpipe.extract import Extractor
from nltk.tag import pos_tag
from processor import get_euclidean_dif
from processor import DTWDistance
import db


class AllFeeds:
    feedList = {}


class AllStories:
    storyList = []

    def addToStory(self, item, conn):
        if len(self.storyList) == 0:
            newStory = Story(item, conn)
            self.storyList.append(newStory)
            #print 'empty feedList'
            return newStory
        else:
            bestDif = (1, None)
            for thing in self.storyList:
                dif = get_euclidean_dif(thing.items[0].article.vector, item.article.vector)
                if dif < 0.6:
                    if dif < bestDif[0]:
                        bestDif = (dif, thing)
                        #print dif
                        thing.addArticle(item.article, conn)
                        return bestDif[1]
            #print item
            anewStory = Story(item, conn)
            self.storyList.append(anewStory)
            #print 'no similar stories'
            #print 'story: ' + str(anewStory)
            return anewStory

#takes a url and returns the sentences contained in it


def get_sentences(text):
    sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
    #split article into sentences using tokenizer
    article_sentenses = sent_detector.tokenize(text.strip())
    return article_sentenses


class Story:
    def __init__(self, article, conn):
        #print 'new story' + str(article)
        self.items = []
        self.title = article.title.text
        self.items.append(article)
        self.text = article.article.text
        self.desc = article.desc.text
        self.storyID = db.addStory(self.title, self.text, self.desc, conn)

    def __str__(self):
        return str(self.items[0])

    def addArticle(self, article, conn):
        if len(self.items) == 0:
            self.items.append(article, conn)
            self.text = article.text
        else:
            self.appendArticle(article, conn)
            self.items.append(article)
            #self.appendArticle(article)

    def appendArticle(self, article, conn):
        #Stuff in here which sorts out the sentences
        sentences = get_sentences(article.text)
        existingSentences = get_sentences(self.text)
        for item in sentences:
            maindif = 0
            for existing in existingSentences:
                words1 = get_words(item)
                words2 = get_words(existing)
            #words = get_words(item)
            #vector = create_word_vector(words)
            #dif = get_euclidean_dif(vector, article.vector)
                d = DTWDistance(words1, words2)
                dif = d.start()
                print dif
                if(dif > maindif):
                    maindif = dif
            print("maindif" + str( maindif))
            if(maindif < 20):
                print('Appending!')
                print item
                db.appendStory(self.storyID, item, conn)
                self.text = self.text + item
        self.items.append(article)

        return None


class Feed:
    def __init__(self, feedname):
        self.feedname = feedname
        self.items = {}

    def __unicode__(self):
        string = ''
        for item in self.items:
            string += str(self.items[item].article) + '\n'
        return string

    def __str__(self):
        return unicode(self).encode('utf-8')

    def __getitem__(self, i):
        t = 0
        for item in self.items:
            if t == i:
                return self.items[item]
            else:
                t = t + 1
                return None

    def add_feed_item(self, item):
        samePost = None
        isNew = False
        if len(self.items) == 0:
            isNew = True
        for key in self.items:
            if item.equalTo(self.items[key]):
                samePost = self.items[key]
                if item.isNew(self.items[key]):
                    #print 'is equal and new'
                    isNew = True
                break

        if samePost is not None:
            # 'is equal'
            if isNew:
                # 'is new'
                self.items[samePost.link] = item
                return True
        else:
            # 'is just new'
            self.items[item.link] = item
            return True
        return False


class ProcessingItem:
    text = None
    words = None
    tags = None
    vector = None

    def __init__(self, text):
        self.text = text
        self.words = get_words(text)
        self.tags = pos_tag(self.words)
        self.vector = create_word_vector(self.words)

    def __unicode__(self):
        return self.text

    def __str__(self):
        return str(self).encode('utf-8')


def getArticleProcItem(link):
    #request the url
    extractor = Extractor(extractor='ArticleExtractor', url=link)
    text = extractor.getText()
    return ProcessingItem(text)


class Item:
    def __init__(self, url, title, desc):
        self.link = url
        self.title = ProcessingItem(title)
        self.desc = ProcessingItem(desc)
        self.article = getArticleProcItem(url)

    def __str__(self):
        return str(self.title)

    def getLink(self):
        return self.link

    def equalTo(self, newItem):
        if self.link == newItem.link:
            # print 'link same'
            return True
        if self.title == newItem.title:
            # print 'title same'
            return True
        if self.desc == newItem.desc:
            #  print 'desc same'
            return True
        return False

    def isNew(self, newItem):
        if self.link != newItem.link:
            #  print 'link different'
            return True
        if self.title != newItem.title:
            #   print 'title different'
            return True
        if self.desc != newItem.desc:
            #  print 'desc different'
            return True
        return False


def get_words(text):
    text = text.lower()
    words = word_tokenize(text)
    taggedWords = nltk.pos_tag(words)

    #j=0;
    word_list = []
    #stemming
    for index, item in enumerate(taggedWords):
        if 'VB' in item[1]:
            pos = wn.ADV
            #print item[1]+'vb'
        elif 'AJ' in item[1]:
            #print item[1]+'aj'
            pos = wn.ADJ
        else:
            #print item[1]+'noun'
            pos = wn.NOUN
        #morphy needs to take the pos... Fix this!
        test = wn.morphy(item[0], pos)
        #word_list[j]=wn.morphy(w)
        if(test is None):
            word_list.append(item[0])
        else:
            word_list.append(test)
        #j=j+1
    return word_list


def create_word_vector(words):
    word_vector = {}
    for word in words:
        if(word in word_vector):
            word_vector[word] = word_vector[word] + 1
        else:
            word_vector[word] = 1
    return word_vector
