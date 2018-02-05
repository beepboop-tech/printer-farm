import time
from random import randint

class Orchestrator():

    def __init__(self, printers):
        self.printers = printers         # TODO: This is not thread safe. Use a queue or a deque

    def run(self, waiting_q, print_q):
        while (True):

            job = waiting_q.get()
            made = False
            for printer in self.printers:
                if printer.can_make(job):
                    job.location = printer.location
                    job.printing_on = printer
                    job.time_remaining = str(randint(47, 59)) + " mins"
                    printer.make(job)
                    print_q.put(job)
                    waiting_q.task_done()
                    made = True
                    break
            if (not made):
                waiting_q.put(job)
                waiting_q.task_done()
            time.sleep(2)
