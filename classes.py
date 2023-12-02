    # Create a data structure to represent a party, which includes a tank, a healer, and three DPS.
    # The party should have a unique ID, and a list of players.
    # The party should have a method to add a player to the party.
    # The party should have a method to remove a player from the party.
    # The party should have a method to return the party's ID.
    # The party should have a method to return the party's size.
    # The party should have a method to return the party's average wait time.

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
    def __init__(self) -> None:
        self.tank = None
        self.healer = None
        self.dps = []

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