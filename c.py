__author__ = 'Arian'
import threading
import time
import logging
import random

logging.basicConfig(level=logging.DEBUG)
#ussing  logging so that prints won't concat
class Resource:
    def __init__(self,id,numberOfResources):
        self.id = id
        self.count = numberOfResources
    def acuire(self):
        self.count -= 1
    def release(self):
        self.count += 1
    def availableResources(self):
        return str(self.count)
class Pool:
    def __init__(self,resource):
        self.activeThreads = []
        self.mutex = threading.Lock()
        self.resource = resource
    def getResource(self,id):
        #print "thread " + id + " waiting..."
        logging.debug("thread " + id + " waiting...")
        self.mutex.acquire()
        #print "thread " + id + " is in critical section"
        logging.debug("thread " + id + " is in critical section")
        self.activeThreads.append(id)
        #print "got one || active threads: ", self.activeThreads
        logging.debug("got one || active threads: "+ str(self.activeThreads))
        self.resource.acuire()
        #print "thread " +id + " got a resource, resources available: " + self.resource.availableResources()
        logging.debug("thread " +id + " got a resource, resources available: " + self.resource.availableResources())
        self.mutex.release()

    def releaseResource(self,id):
        #print "thread " + id + " waiting..."
        logging.debug("thread " + id + " waiting...")
        self.mutex.acquire()
        #print "thread " + id + " is in critical section"
        logging.debug("thread " + id + " is in critical section")
        self.activeThreads.remove(id)
        #print "released one || active threads: ", self.activeThreads
        logging.debug("released one || active threads: "+str(self.activeThreads))
        self.resource.release()
        logging.debug("thread " +id + " released a resource, resources available: " + self.resource.availableResources())
        #print "thread " +id + " released a resource, resources available: " + self.resource.availableResources()
        self.mutex.release()

def target(semaphore,pool):
    threadId = threading.currentThread().getName()
    #print "thread " + threadId + " waiting for semaphore to join the pool"
    with semaphore:
        pool.getResource(threadId)
        time.sleep(random.randint(1,3))
        pool.releaseResource(threadId)


if __name__ == "__main__":
    numOfResources = random.randint(4,8)
    logging.debug("total resources: "+str(numOfResources))
    resource = Resource("primaryResource",numOfResources)
    semaphore = threading.Semaphore(numOfResources)
    threadPool = Pool(resource)
    threads = []
    for i in range(random.randint(7,20)):
        temp = threading.Thread(target=target,name=str(i),args=(semaphore,threadPool))
        threads.append(temp)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    print "done ;)"







