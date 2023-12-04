import threading
import time
import random
import synch

EMPTY = 0
ACTIVE = 1

class Instance:
    def __init__(self, id):
        self.id = id
        self.tanks_served = 0
        self.healers_served = 0
        self.dps_served = 0
        self.total_time_served = 0
        self.parties_served = 0
        self.status = EMPTY

class Dungeon:
    def __init__(self, n, t, h, d, t1, t2):
        self.n_instances = n
        self.tanks = t
        self.healers = h
        self.dps = d
        self.t1 = t1
        self.t2 = t2
        self.instances = [Instance(i) for i in range(n)]
        self.lfg_monitor = synch.LFG_Monitor()

def print_instances(dungeon):
    # print remaining tanks
    print("Remaining Tank instances: " + str(dungeon.tanks))
    # print remaining healers
    print("Remaining Healer instances: " + str(dungeon.healers))
    # print remaining dps
    print("Remaining DPS instances: " + str(dungeon.dps))
    print()

    for i in range(0, dungeon.n_instances, 4):
        for j in range(4):
            if i + j < dungeon.n_instances:
                tmp = dungeon.instances[i + j]
                print(f"Instance {tmp.id}: { 'ACTIVE' if tmp.status else 'EMPTY' }\t")
        print()

def update_dungeon(dungeon, i):
    dungeon.tanks -= 1
    i.tanks_served += 1
    
    dungeon.healers -= 1
    i.healers_served += 1
    
    dungeon.dps -= 3
    i.dps_served += 3
    i.status = ACTIVE

def run_instance(args):
    dungeon = args.dungeon
    i = dungeon.instances[args.id]

    while True:
        # Lock dungeon
        synch.lock(dungeon.lfg_monitor)
        # Print current instances
        print_instances(dungeon)
        # If not enough members to create a party
        if dungeon.tanks < 1 or dungeon.healers < 1 or dungeon.dps < 3:
            synch.unlock(dungeon.lfg_monitor)
            break

        update_dungeon(dungeon, i)
        print_instances(dungeon)
        synch.unlock(dungeon.lfg_monitor)

        duration = dungeon.t1 + random.randint(0, dungeon.t2 - dungeon.t1 + 1)
        time.sleep(duration)
        i.total_time_served += duration
        i.parties_served += 1
        i.status = EMPTY

    return

def start_process(dungeon):
    random.seed(time.time())
    threads = []

    # Create and start instance threads
    for i in range(dungeon.n_instances):
        args = run_instance_args(dungeon, i)
        thread = threading.Thread(target=run_instance, args=(args,))
        threads.append(thread)
        thread.start()

    # Terminate threads
    for thread in threads:
        thread.join()

def print_summary(dungeon):
    print("S U M M A R Y")
    total_served = 0
    for i in range(dungeon.n_instances):
        instance = dungeon.instances[i]
        print(f"Instance {instance.id}:\n"
              f"Parties Served: {instance.parties_served}\n"
              f"Total Time Served: {instance.total_time_served}\n")
        total_served += instance.parties_served

    print(f"\nTotal Parties Served: {total_served}\n")
    print(f"\Remaining:\n\tTanks: {dungeon.tanks}\n\tHealers: {dungeon.healers}\n\tDPS: {dungeon.dps}\n")

def run_instance_args(dungeon, instance_id):
    return RunInstanceArgs(dungeon, instance_id)

class RunInstanceArgs:
    def __init__(self, dungeon, instance_id):
        self.dungeon = dungeon
        self.id = instance_id
        
def process_input(user_input):
    global terminate_simulation
    inp_arr = user_input.split()
    
    n = int(inp_arr[0])
    t = int(inp_arr[1])
    h = int(inp_arr[2])
    d = int(inp_arr[3])
    t1 = int(inp_arr[4])
    t2 = int(inp_arr[5])
    
    dungeon = Dungeon(n, t, h, d, t1, t2)     
    start_process(dungeon)
    print_summary(dungeon)