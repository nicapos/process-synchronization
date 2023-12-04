import threading

class LFG_Monitor:
    def __init__(self):
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)
        self.head = 0
        self.tail = 0

def lock(monitor):
    with monitor.lock:
        thread_idx = monitor.tail
        monitor.tail += 1
        while thread_idx != monitor.head:
            monitor.cond.wait()

def unlock(monitor):
    with monitor.lock:
        monitor.head += 1
        monitor.cond.notify_all()