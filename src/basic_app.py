from orchestrators import Orchestrator
from printers      import Printer
from jobs          import Job
import threading
import time



class TestUser():
    def __init__(self):
        self.username = 'tom'

p = Printer('Duplicator i3', '192.168.0.201', 'B5A36115A3DC49148EFC52012E7EBCD9',
        'Hackspace', 'duplicator', 'PLA', 'black')


# o = Orchestrator(ps)
#
# thread  = threading.Thread(target=o.run)
# thread.start()
#
# j = Job('1', 'r', 'PLA')
job = Job('stepperspacer.gcode', 'black', 'PLA', user=TestUser())

print(p.cancel())
# printer = ps[0]

# print(printer.cancel())
# if(printer.can_make(jj)):
#     printer.make(jj)
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
