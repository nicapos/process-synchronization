from enum import Enum
import threading

# DESCRIPTION: This class represents a monitor (synchronization mechanism) for managing access to shared resources 
# in a First In, First Out (FIFO) manner.

# Attributes:
# lock: A threading lock for mutual exclusion.
# cond: A threading condition variable associated with the lock.
# head: Represents the head of the FIFO queue.
# tail: Represents the tail of the FIFO queue.

# Methods:
# lock(monitor): Acquires the lock and adds the current thread index to the FIFO queue. It then waits until the current thread becomes the head of the queue before proceeding.
# release(monitor): Releases the lock, increments the head of the queue, and notifies all waiting threads.

class LFG_Monitor:
    def __init__(self):
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)
        self.head = 0
        self.tail = 0

# Acquire lock
def lock(monitor):
    with monitor.lock:
        thread_idx = monitor.tail
        monitor.tail += 1
        while thread_idx != monitor.head:
            monitor.cond.wait()

# Release lock
def release(monitor):
    with monitor.lock:
        monitor.head += 1
        monitor.cond.notify_all()
       
# DESCRIPTION: This is an enumeration representing possible states of an instance, 
# either "empty" or "active."                
class InstanceStatus(Enum):
    EMPTY = "empty"
    ACTIVE = "active"

# DESCRIPTION: This class represents an instance within the dungeon.

# Attributes:
# id: The unique identifier for the instance.
# tanks_served, healers_served, dps_served: Counters for the number of tanks, healers, and DPS served by this instance.
# total_time_served: Total time spent serving parties.
# parties_served: Number of parties served.
# status: The current status of the instance, using the InstanceStatus enumeration.
class Instance:
    def __init__(self, instance_id):
        self.id = instance_id
        self.tanks_served = 0
        self.healers_served = 0
        self.dps_served = 0
        
        self.total_time_served = 0
        self.parties_served = 0
        self.status = InstanceStatus.EMPTY  # Use the InstanceStatus enumeration

# DESCRIPTION: This class represents the overall dungeon.

# Attributes:
# num_instances: Number of instances in the dungeon.
# tanks, healers, dps: Counts of available tanks, healers, and DPS in the dungeon.
# t1, t2: Time range for simulating dungeon clearing.
# instances: A list of Instance objects representing the instances in the dungeon.
# lfg_monitor: An instance of the LFG_Monitor class for managing synchronization.
class Dungeon:
    def __init__(self, num_instances, tanks, healers, dps, t1, t2):
        self.num_instances = num_instances
        self.tanks = tanks
        self.healers = healers
        self.dps = dps
        self.t1 = t1
        self.t2 = t2
        self.instances = [Instance(i) for i in range(num_instances)]
        self.lfg_monitor = LFG_Monitor()