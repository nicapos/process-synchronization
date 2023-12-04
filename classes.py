import time
import random
import threading
from enum import Enum
from globals import terminate_simulation

class Role(Enum):
    TANK = "tank"
    HEALER = "healer"
    DPS = "dps"

class Character:
    def __init__(self, role, name) -> None:
        self.__role = role
        self.__name = name

    @property
    def role(self) -> Role:
        return self.__role
    
    @property
    def name(self) -> str:
        return f"tank {self.__name}"
    
class Party:
    party_counter = 0

    def __init__(self) -> None:
        self.__party_id = Party.party_counter
        Party.party_counter += 1
        self.tank = None
        self.healer = None
        self.dps = []
        self.__start_time = time.time()

    @property
    def party_id(self) -> int:
        return self.__party_id

    def add_member(self, character: Character) -> None:
        if character.role == Role.TANK:
            self.tank = character
        elif character.role == Role.HEALER:
            self.healer = character
        elif character.role == Role.DPS:
            self.dps.append(character)

    def remove_member(self, role: Role) -> None:
        if role == Role.TANK:
            self.tank = None
        elif role == Role.HEALER:
            self.healer = None
        elif role == Role.DPS:
            if self.dps:
                self.dps.pop(0)

    def get_party_size(self) -> int:
        return len(self.dps) + (1 if self.tank else 0) + (1 if self.healer else 0)

    def get_average_wait_time(self) -> float:
        return time.time() - self.__start_time
                
class InstanceStatus(Enum):
    EMPTY = "empty"
    ACTIVE = "active"                
    
class Instance:
    total_parties_served = 0
    summary_lock = threading.Lock()

    def __init__(self, instance_id, t1, t2, tank_queue, healer_queue, dps_queue, status_lock):
        self.instance_id = instance_id
        self.t1 = t1
        self.t2 = t2

        self.tank_queue = tank_queue
        self.healer_queue = healer_queue
        self.dps_queue = dps_queue

        self.status_lock = status_lock
        self.party = None
        self.active = False
        self.total_time_served = 0

    def update_summary_statistics(self, clear_time):
        with self.summary_lock:
            self.total_parties_served += 1
            self.total_time_served += clear_time

    @classmethod
    def update_instance_status(cls, instances, status_lock):
        global terminate_simulation
        while not terminate_simulation:
            time.sleep(5)

            with status_lock:
                # Check if all instances are inactive
                all_instances_inactive = all(not instance.active for instance in instances)

                if terminate_simulation or all_instances_inactive:
                    terminate_simulation = True  # Set the termination flag
                    break  # Exit the loop if termination flag is set or all instances are inactive

                for instance in instances:
                    if instance.active:
                        print(f"Instance {instance.instance_id}: Active")
                    else:
                        print(f"Instance {instance.instance_id}: Empty")


    def dungeon_clearing(self):
        clear_time = random.uniform(self.t1, self.t2)
        time.sleep(clear_time)

        with self.status_lock:
            self.active = False
            completed_party = self.party
            self.party = None
            print(f"Instance {self.instance_id}: Party completed - {completed_party}")

            self.total_parties_served += 1
            self.total_time_served += clear_time
            print(self.total_time_served)

    def start_instance(self, tank_queue, healer_queue, dps_queue):
        while not self.active:
            tank = self.tank_queue.get()
            healer = self.healer_queue.get()

            if tank and healer:
                dps = [self.dps_queue.get() for _ in range(3)]

                # Party Creation
                party = Party()
                party.add_member(tank)
                party.add_member(healer)
                for d in dps:
                    party.add_member(d)

                with self.status_lock:
                    self.active = True
                    self.party = party
                    print(f"Instance {self.instance_id}: Party started - {self.party}")

                self.dungeon_clearing()