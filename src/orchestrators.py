from queue    import Queue
from printers import Printer
from jobs     import Job


class Orchestrator():

    def __init__(self, printers):
        self.queue = Queue(maxsize=0)
        self.printers = printers         # TODO: This is not thread safe. Use a queue or a deque
        self.jobs = []

    def run(self):
        while (True):
            self.jobs = list(self.queue.queue)
            job = self.queue.get()
            made = False
            for printer in self.printers:
                if printer.can_make(job):
                    printer.make(job)
                    self.queue.task_done()
                    made = True
                    break
            if (not made):
                self.queue.put(job)
                self.queue.task_done()
