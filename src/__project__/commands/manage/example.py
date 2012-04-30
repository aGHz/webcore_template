from datetime import datetime
import os
from psutil import Process


def perform_example(example_option=False, examples=None):
    """Perform some example task"""

    proc = Process(os.getpid())
    memory = proc.get_memory_info()[0]
    timer_then = datetime.now()

    # ...

    memory = proc.get_memory_info()[0] if proc.get_memory_info()[0] > memory else memory

    timer_now = datetime.now()
    print "Performed examples in %s seconds using %dMB memory" % ((timer_now - timer_then).total_seconds(), int(memory/1000000))

