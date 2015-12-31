__author__ = 'Arian'
import threading
import sqlite3
import sys
import random
import itertools

mutex = threading.Lock()
fakeNames = ['json','matt','joey','chandler','barney','ted','marshal','mitch','don']
sqliteConnection = sqlite3.connect("test.db",check_same_thread=False)

class CustomThread(threading.Thread):
    global mutex
    global sqliteConnection
    def __init__(self,id,name,text):
        super(CustomThread,self).__init__()
        self.id = id
        self.name = name
        self.text = text
    def say(self,text):
        self.text = text
        print self.text

    def run(self):

        print "thread " + self.id + " waiting"
        mutex.acquire()
        print "thread " + self.id + " is in critical section"
        print "doin the thing ...."
        cursor = sqliteConnection.cursor()
        cursor.execute("INSERT INTO Threads VALUES('Thread ID: {0}','Thread Name: {1}  ','Thread text: {2}')".format(self.id,self.name,self.text))
        print "thread " + self.id + " is finished"
        cursor.close()
        mutex.release()




if __name__ == "__main__":

    cursor = sqliteConnection.cursor()
    cursor.execute("CREATE TABLE if not EXISTS Threads(Id INT, Name TEXT, Text TEXT)")
    cursor.close()

    threads = []
    for i in range(random.randint(5,20)):
        temp = CustomThread(str(i),fakeNames[random.randint(0,len(fakeNames)-1)],fakeNames[random.randint(0,len(fakeNames)-1)])
        threads.append(temp)

    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()

    cursor = sqliteConnection.cursor().execute("Select * from Threads")
    data = cursor.fetchall()
    cursor.close()

    print "data in Data Base:"
    print "#####################################################"
    for datum in data:
        print "# " + str(datum[0])+'\t'+str(datum [1])+'\t'+str(datum[2])

    print "#####################################################"


    print "done ;)"
