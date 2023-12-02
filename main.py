# The program accepts three inputs from the user.
# - n - maximum number of concurrent instances
# - t - number of tank players in the queue
# - h - number of healer players in the queue
# - d - number of DPS players in the queue
# - t1 - minimum time before an instance is finished
# - t2 - maximum time before an instance is finished
import process

def run_simulation():
    
    user_input = input()
    if len(user_input.split()) != 6:
        # TODO: Change this if we have to keep asking if input is invalid
        print("Invalid input, must be 6 integers separated by space")
      
    process.process_input(user_input)    
        
if __name__ == "__main__":
    run_simulation()  
