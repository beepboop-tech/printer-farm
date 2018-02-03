from orchestrators import Orchestrator
from printers      import Printer
from jobs          import Job
import threading
import time


ps = [Printer('printer_1', '192.168.0.201', 'B5A36115A3DC49148EFC52012E7EBCD9', 'MVB', 'rep', 'PLA', 'r'),
      Printer('printer_2', '192.168.0.202', 'ED7F718BBE11456BA3619A04C66EF74A','MVB', 'rep', 'PLA', 'r')]


# o = Orchestrator(ps)
#
# thread  = threading.Thread(target=o.run)
# thread.start()
#
# j = Job('1', 'r', 'PLA')
# jj = Job('2', 'r', 'PLA')

print(ps[0].simple_status())

# time.sleep(2)
# o.queue.put(j)
# # time.sleep(3)
# o.queue.put(jj)
# # o.queue.put(jj)
# # o.queue.put(jj)
# time.sleep(1)
#
#
# print(o.jobs)
# time.sleep(1)
# o.queue.queue.clear()
