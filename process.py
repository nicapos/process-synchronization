import threading
import time
import random
import classes

def print_instances(dungeon):
    # print remaining tanks
    print("Remaining Tank instances: " + str(dungeon.tanks))
    # print remaining healers
    print("Remaining Healer instances: " + str(dungeon.healers))
    # print remaining dps
    print("Remaining DPS instances: " + str(dungeon.dps))
    print()

    for i in range(0, dungeon.num_instances, 4):
        for j in range(4):
            if i + j < dungeon.num_instances:
                tmp = dungeon.instances[i + j]
                status_str = classes.InstanceStatus.ACTIVE.value if tmp.status == classes.InstanceStatus.ACTIVE else classes.InstanceStatus.EMPTY.value
                print(f"Instance {tmp.id}: {status_str}\t", end="")       
        print()
    print("===================================")    

def update_dungeon(dungeon, i):
    dungeon.tanks -= 1
    i.tanks_served += 1
    
    dungeon.healers -= 1
    i.healers_served += 1
    
    dungeon.dps -= 3
    i.dps_served += 3
    i.status = classes.InstanceStatus.ACTIVE

def dungeon_clear(dungeon):
    return dungeon.t1 + random.randint(0, dungeon.t2 - dungeon.t1 + 1)

def start_instance(args):
    dungeon = args.dungeon
    i = dungeon.instances[args.id]

    while True:
        # Lock dungeon
        classes.lock(dungeon.lfg_monitor)
        # Print current instances
        print_instances(dungeon)
        
        # If not enough members to create a party
        if dungeon.tanks < 1 or dungeon.healers < 1 or dungeon.dps < 3:
            classes.unlock(dungeon.lfg_monitor)
            break
        else:
            update_dungeon(dungeon, i)
            print_instances(dungeon)
            classes.unlock(dungeon.lfg_monitor)

            # Simulate dungeon clear
            clear_time = dungeon_clear(dungeon)
            time.sleep(clear_time)
            
            i.total_time_served += clear_time
            i.parties_served += 1
            i.status = classes.InstanceStatus.EMPTY

def start_process(dungeon):
    random.seed(time.time())
    threads = []

    # Create and start instance threads
    for i in range(dungeon.num_instances):
        args = run_instance_args(dungeon, i)
        thread = threading.Thread(target=start_instance, args=(args,))
        threads.append(thread)
        thread.start()

    # Terminate threads
    for thread in threads:
        thread.join()

def print_summary(dungeon):
    print()
    print("========= S U M M A R Y =========")
    total_served = 0
    for instance in dungeon.instances:
        print(f"Instance {instance.id}:\n"
            f"Parties Served: {instance.parties_served}\n"
            f"Total Time Served: {instance.total_time_served}\n")
        total_served += instance.parties_served

    print(f"\nTotal Parties Served: {total_served}\n\n")
    print("Remaining: ")
    print(f"Tanks: {dungeon.tanks}")
    print(f"Healers: {dungeon.healers}")
    print(f"DPS: {dungeon.dps}")

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
    
    dungeon = classes.Dungeon(n, t, h, d, t1, t2)     
    start_process(dungeon)
    print_summary(dungeon)