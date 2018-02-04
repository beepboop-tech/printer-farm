from queue    import Queue
from printers import Printer
from jobs     import Job
from mutexes  import q_lock


class Orchestrator():

    def __init__(self, printers):
        self.queue = Queue(maxsize=0)
        self.printing_queue = Queue(maxsize=0)
        self.printers = printers         # TODO: This is not thread safe. Use a queue or a deque
        # self.jobs = []

    def run(self):
        # global q_lock

        while (True):
            # q_lock.acquire()
            # try:
            #     job = self.queue.get()
            #     made = False
            #     for printer in self.printers:
            #         if printer.can_make(job):
            #             job.location = printer.location
            #             printer.make(job)
            #             self.printing_queue.put(job)
            #             self.queue.task_done()
            #             made = True
            #             break
            #     if (not made):
            #         self.queue.put(job)
            #         self.queue.task_done()
            # finally:
            #     q_lock.release()
            job = self.queue.get()
            made = False
            for printer in self.printers:
                if printer.can_make(job):
                    job.location = printer.location
                    printer.make(job)
                    self.printing_queue.put(job)
                    self.queue.task_done()
                    made = True
                    break
            if (not made):
                self.queue.put(job)
                self.queue.task_done()
