from enum import Enum
import threading
import synch

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
                
class InstanceStatus(Enum):
    EMPTY = "empty"
    ACTIVE = "active"

class Instance:
    def __init__(self, instance_id):
        self.id = instance_id
        self.tanks_served = 0
        self.healers_served = 0
        self.dps_served = 0
        self.total_time_served = 0
        self.parties_served = 0
        self.status = InstanceStatus.EMPTY  # Use the InstanceStatus enumeration

class Dungeon:
    def __init__(self, num_instances, tanks, healers, dps, t1, t2):
        self.num_instances = num_instances
        self.tanks = tanks
        self.healers = healers
        self.dps = dps
        self.t1 = t1
        self.t2 = t2
        self.instances = [Instance(i) for i in range(num_instances)]
        self.lfg_monitor = synch.LFG_Monitor()