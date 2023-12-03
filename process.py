import classes
import threading
from queue import Queue    

def instance_worker(instance, tank_queue, healer_queue, dps_queue):
    instance.start_instance()

# TODO: Fix this to include synchronization techniques
def create_instances(n, max_party_size, t1, t2, tank_queue, healer_queue, dps_queue):
    instances = [classes.Instance(instance_id=i, max_party_size=max_party_size, t1=t1, t2=t2,
                                tank_queue=tank_queue, healer_queue=healer_queue, dps_queue=dps_queue) for i in range(n)]
    threads = []

    for instance in instances:
        thread = threading.Thread(target=instance_worker, args=(instance,))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

def start_queue(n, t1, t2, tank_queue, healer_queue, dps_queue):
    create_instances(n, 5, t1, t2, tank_queue, healer_queue, dps_queue)

def create_characters(t,h,d):
    tank_queue = Queue()
    healer_queue = Queue()
    dps_queue = Queue()
    
    if t!=0 or h!=0 or d!=0:
        for i in range(t):
            tank = classes.Character(role=classes.Role.TANK)
            tank_queue.put(tank)
        for i in range(h):
            healer = classes.Character(role=classes.Role.HEALER)
            healer_queue.put(healer)
        for i in range(d):
            dps = classes.Character(role=classes.Role.DPS)
            dps_queue.put(dps)  
    else:
        print("Cannot create a full party. Tank in queue = {t}, Healer in queue = {h}, DPS in queue = {d}")        
    
    return tank_queue, healer_queue, dps_queue  

def process_input(user_input):
    inp_arr = user_input.split()
    
    n = int(inp_arr[0])
    t = int(inp_arr[1])
    h = int(inp_arr[2])
    d = int(inp_arr[3])
    t1 = int(inp_arr[4])
    t2 = int(inp_arr[5])
    
    tq, hq, dq = create_characters(t,h,d)
    if len(tq) != 0 or len(hq) != 0 or len(dq) != 0:
        start_queue(n, t1, t2, tq, hq, dq)
    else:    
        print("Process Terminated")