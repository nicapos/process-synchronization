import classes
import threading
import time
from queue import Queue    
import logging
from globals import terminate_simulation

# For logging errors
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Output the current stats of the instances
def display_results(instances):
    global terminate_simulation
    while not terminate_simulation:
        time.sleep(5)

        with classes.Instance.summary_lock:
            print("\nCurrent Status of Instances:")
            for instance in instances:
                if terminate_simulation:
                    break  # Exit the loop if termination flag is set
                if instance.active:
                    print(f"Instance {instance.instance_id}: Active")
                else:
                    print(f"Instance {instance.instance_id}: Empty")

            print("\nSummary of Parties Served:")
            for instance in instances:
                print(f"Instance {instance.instance_id}: {instance.total_parties_served} parties served")

            print("\nTotal Time Served Across All Instances:")
            total = 0
            for instance in instances:
                total += instance.total_time_served
            print(f"{total} seconds")

        
# process the instances
def process_instances(n, t1, t2, tank_queue, healer_queue, dps_queue):
    global terminate_simulation
    # Create lock to synchronize instance process
    status_lock = threading.Lock()
    
    # Create n instances
    instances = [classes.Instance(instance_id=i, t1=t1, t2=t2,
                           tank_queue=tank_queue, healer_queue=healer_queue, dps_queue=dps_queue,
                           status_lock=status_lock) for i in range(n)]

    instance_threads = [threading.Thread(target=instance.start_instance, args=(tank_queue, healer_queue, dps_queue)) for instance in instances]
    update_status_thread = threading.Thread(target=classes.Instance.update_instance_status, args=(instances, status_lock))
    display_results_thread = threading.Thread(target=display_results, args=(instances,))

    for thread in instance_threads:
        thread.start()

    update_status_thread.start()
    display_results_thread.start()

    for thread in instance_threads:
        thread.join()

    update_status_thread.join()
    display_results_thread.join()

    logger.info("Terminating create_instances function.")

# Create characters based on the number of tanks, healers, and dps and put them in separate queues
def create_characters(t,h,d):
    tank_queue = Queue()
    healer_queue = Queue()
    dps_queue = Queue()
    
    if t!=0 or h!=0 or d!=0:
        for i in range(t):
            tank = classes.Character(role=classes.Role.TANK, name=i+1)
            tank_queue.put(tank)
        for j in range(h):
            healer = classes.Character(role=classes.Role.HEALER, name=j+1)
            healer_queue.put(healer)
        for k in range(d):
            dps = classes.Character(role=classes.Role.DPS, name=k+1)
            dps_queue.put(dps)  
    else:
        logger.error("Cannot create a full party. Tank in queue = {t}, Healer in queue = {h}, DPS in queue = {d}")        
    
    return tank_queue, healer_queue, dps_queue  

# Start processing the input
def process_input(user_input):
    global terminate_simulation
    inp_arr = user_input.split()
    
    n = int(inp_arr[0])
    t = int(inp_arr[1])
    h = int(inp_arr[2])
    d = int(inp_arr[3])
    t1 = int(inp_arr[4])
    t2 = int(inp_arr[5])
    
    tq, hq, dq = create_characters(t, h, d)
    
    if not tq.empty() or not hq.empty() or not dq.empty():
        process_instances(n, t1, t2, tq, hq, dq)
        # process_instance_fin(n,t1,t2,tq, hq, dq)
    else:
        logger.error("Process Terminated")
        terminate_simulation = True