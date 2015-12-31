__author__ = 'Arian'
from a import CustomThread
import threading
import os
import random


globalVariable = ''
fileName = os.getcwd()+'/commonFile.txt'
mutex = threading.Lock()
fakeNames = ['json','matt','joey','chandler','barney','ted','marshal','mitch','don']

class CustomThreadB(CustomThread):
    global globalVariable
    def run(self):
        print "thread " + self.id + " waiting"
        mutex.acquire()
        print "thread " + self.id + " is in critical section"
        print "doin the thing ...."
        globalVariable = self.id
        commonFile = open(fileName,'a+')
        line = "thread no. " + str(self.id) + " is writing its name: " + self.name +"\n"

        commonFile.write(line)
        commonFile.close()
        print "thread " + self.id + " is finished"
        mutex.release()







if __name__ == "__main__":

    commonFile = open(fileName,'w').close()

    threads = []
    for i in range(random.randint(5,20)):
        temp = CustomThreadB(str(i),fakeNames[random.randint(0,len(fakeNames)-1)],fakeNames[random.randint(0,len(fakeNames)-1)])
        threads.append(temp)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

