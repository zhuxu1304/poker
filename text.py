import multiprocessing
import time

q = multiprocessing.Queue()

def wr(q):
    for i in range(100):
        print('put',i)
        q.put(i)
        time.sleep(0.5)

def rd(q):
    while True:
        while not q.empty():
            last = q.get()
            print('got',last)
        print('last',last)
        time.sleep(1)

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=wr,args=(q,))
    p2 = multiprocessing.Process(target=rd,args=(q,))
    p1.start()
    p2.start()