from queue import Queue
import time
from jobs import Job

def do_stuff(q):
    while not q.empty():
        job = q.get()
        if (job.colour == True):
            print("Done task" , job.filename)
            q.task_done()
        else:
            job.colour = True
            q.put(job)
            q.task_done()

q = Queue(maxsize=0)

for x, b in zip(['1','2','3','4'], [True, False, True, True]):
  q.put(Job(x, b, 'b'))

do_stuff(q)
