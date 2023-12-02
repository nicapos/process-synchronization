# The program accepts three inputs from the user.
# - n - maximum number of concurrent instances (parties)
# - t - number of tank players in the queue
# - h - number of healer players in the queue
# - d - number of DPS players in the queue
# - t1 - minimum time before an instance is finished
# - t2 - maximum time before an instance is finished
import classes

def create_party(tank, healer, dps):
    party = classes.Party()
    party.add_member(tank)
    party.add_member(healer)
    for dps_member in dps:
        party.add_member(dps_member)
    return party

def start_queue():
    pass
def process_input(user_input):
    inp_arr = user_input.split()
    
    n = int(inp_arr[0])
    t = int(inp_arr[1])
    h = int(inp_arr[2])
    d = int(inp_arr[3])
    t1 = int(inp_arr[4])
    t2 = int(inp_arr[5])
    
    start_queue()
    