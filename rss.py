from feeds import AllFeeds, Feed, Item, AllStories
import processor
import db

from Queue import Queue
from threading import Thread
from time import sleep

stories = AllStories()



class Worker(Thread):
    #Thread executing tasks from a given tasks queue
    def __init__(self, tasks):
        Thread.__init__(self)
        self.tasks = tasks
        self.daemon = True
        self.start()

    def run(self):
        while True:
            print ('processing task')
            func, args, kargs = self.tasks.get()
            try:
                func(*args, **kargs)
            except Exception as e:
                print (e)
            finally:
                self.tasks.task_done()


class ThreadPool:
    #Pool of threads consuming tasks from a queue
    def __init__(self, num_threads):
        self.tasks = Queue()
        for _ in range(num_threads):
            Worker(self.tasks)

    def add_task(self, func, *args, **kargs):
        #Add a task to the queue
        print ('\n\rAdding task')
        self.tasks.put((func, args, kargs))

    def wait_completion(self):
        #Wait for completion of all the tasks in the queue
        self.tasks.join()


#testing function - removes the threads, only runs one feed
def test():
    getFeed('Guardian')


#start the processing
def getFeed(feedname):
    global processPool

    print(('getting ' + feedname))
    item_node = processor.getXMLItems(feedname)

    #save the title and link of each
    print(feedname)
    if feedname in AllFeeds.feedList:
        print('not new feeds')
    else:
        AllFeeds.feedList[feedname] = Feed(feedname)

    for item in item_node:
        print('add processing task')
        processPool.add_task(processFeed, item, feedname)


def processFeed(item, feedname):

    print(('processing ' + feedname))
    global stories
    #run through each item in the feeds

    conn = db.getConnection()

    title = item.getElementsByTagName("title")
    link = item.getElementsByTagName("link")
    desc = item.getElementsByTagName("description")

    if title:
        ftitle = processor.getText(title[0].childNodes)
    if link:
        flink = processor.getText(link[0].childNodes)
    if desc:
        fdesc = processor.getText(desc[0].childNodes)

    newItem = Item(flink, ftitle, fdesc)
    AllFeeds.feedList[feedname].add_feed_item(newItem)

    stories.addToStory(newItem, conn)

    return AllFeeds.feedList[feedname]


def poll():
    sleep(3000)
    for feedname in processor.feedList.getFeedNames():
        try:
            getPool.add_task(getFeed, feedname)
            print(('add get task' + feedname))
        except:
            print(("There is an error with the " + feedname + " feeds."))
    poll()

getPool = ThreadPool(10)
processPool = ThreadPool(4)


def main():
    conn = db.getConnection()
    db.cleardb(conn)
    global getPool
    print('start main')
    for feedname in processor.feedList.getFeedNames():
        try:
            getPool.add_task(getFeed, feedname)
            print(('add get task' + feedname))
        except:
            print(("There is an error with the " + feedname + " feeds."))
    poll()

if __name__ == "__main__":
    main()
