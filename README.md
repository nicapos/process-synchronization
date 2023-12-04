# Process Synchronization

A programming exercise to simulate process synchronization.

## Specifications

Consider the following synchronization problem:

Suppose you are tasked to create a solution that will manage the LFG (Looking for Group) dungeon queuing of an MMORPG.

- There are only n instances that can be concurrently active. Thus, there can only be a maximum n number of parties that are currently in a dungeon.
- A standard party of 5 is 1 tank, 1 healer, 3 DPS.
- The solution should not result in a deadlock.
- The solution should not result in starvation.
- It is assumed that the input values arrived at the same time.
- A time value (in seconds) t is randomly selected between $\text{t1}$ and $\text{t2}$. Where $\text{t1}$ represents the fastest clear time of a dungeon instance and $\text{t2}$ is the slowest clear time of a dungeon instance. For ease of testing $\text{t2} \leq 15$.

### Input

The program accepts three inputs from the user.

- n - maximum number of concurrent instances
- t - number of tank players in the queue
- h - number of healer players in the queue
- d - number of DPS players in the queue
- t1 - minimum time before an instance is finished
- t2 - maximum time before an instance is finished

### Output

The output of the program should show the following:

  - Current status of all available instances
  - If there is a party in the instance, the status should say "active"
  - If the instance is empty, the status should say "empty"

At the end of the execution there should be a summary of how many parties an instance have served and total time served.

## Simulation

The **synchronization technique** used in the program is the monitor pattern. The specific implementation details can be found in the [`classes.py`](./classes.py) file, specifically in lines 4 to 21.

```python
class LFG_Monitor:
    def __init__(self):
        self.lock = threading.Lock()
        self.cond = threading.Condition(self.lock)
        self.head = 0
        self.tail = 0
```

```python
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
```

## Usage
To start the simulation program, run:
```bash
python main.py
```