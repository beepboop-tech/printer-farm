from orchestrators import Orchestrator
from printers      import Printer
from jobs          import Job
import threading
import time


ps = [Printer('printer_1', '192.168.0.201', 'B5A36115A3DC49148EFC52012E7EBCD9', 'MVB', 'rep', 'PLA', 'r'),
      Printer('printer_2', '192.168.0.202', 'ED7F718BBE11456BA3619A04C66EF74A','MVB', 'rep', 'PLA', 'r')]


o = Orchestrator(ps)

threads = []
thread  = threading.Thread(target=o.run)
threads.append(thread)
thread.start()

j = Job('1', 'r', 'PLA')
jj = Job('2', 'r', 'PLA')


time.sleep(2)
o.queue.put(j)
time.sleep(3)
o.queue.put(jj)
