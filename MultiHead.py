import time
from multiprocessing import Process, Queue

def multiChild(masterQueue, number):
    time.sleep(2)
    masterQueue.put(number)
    return

def multiHead():
    coolQueue = Queue(3)
    child1 = Process(target=multiChild, args=(coolQueue, 2))
    child1.start()
    while (coolQueue.empty()):
        print('Got nothing yet')
    # time.sleep(10)
    print(coolQueue.get())

    return

if __name__ == '__main__':
    multiHead()