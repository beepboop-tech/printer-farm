from queue import Queue
from threading import Thread, Lock, RLock
lock = RLock()
import time

def do_something(n):
    while True:

        with lock:
            print("Worker", n, " sleeping")
        time.sleep(1)
t= Thread(target=do_something, args=('1',))
t1= Thread(target=do_something,args=('2',))
t.start()
t1.start()


while True:
    with lock:
        print("Producer chilling")
    time.sleep(1)
