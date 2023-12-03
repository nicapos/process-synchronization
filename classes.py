import time
import random
from enum import Enum

class Role(Enum):
    TANK = "tank"
    HEALER = "healer"
    DPS = "dps"

class Character:
    def __init__(self, role) -> None:
        self.__role = role

    @property
    def role(self) -> Role:
        return self.__role

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
                
class Instance:
    def __init__(self, instance_id, max_party_size, t1, t2, tank_queue, healer_queue, dps_queue):
        self.instance_id = instance_id
        self.max_party_size = max_party_size
        
        self.t1 = t1
        self.t2 = t2
        self.tank_queue = tank_queue
        self.healer_queue = healer_queue
        self.dps_queue = dps_queue
        
        self.party = None
        self.active = False

    def dungeon_clearing(self):
        clear_time = random.uniform(self.t1, self.t2)
        time.sleep(clear_time)

        self.active = False
        print(f"Instance {self.instance_id}: Party completed - {self.party}")

    def start_instance(self):
        while not self.active:
            tank = self.tank_queue.get()
            healer = self.healer_queue.get()

            if tank and healer:
                dps = [self.dps_queue.get() for _ in range(3)]

                # Create Party
                party = Party()
                party.add_member(tank)
                party.add_member(healer)
                for d in dps:
                    party.add_member(d)

                # Activate Instance
                self.active = True
                self.party = party

                print(f"Instance {self.instance_id}: Party started - {self.party}")
                
                # Dungeon Clearing Simulation
                self.dungeon_clearing()
              
