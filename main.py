import process

def run_simulation():
    user_input = input()
    if len(user_input.split()) != 6:
        # TODO: Change this if we have to keep asking if input is invalid
        print("Invalid input, must be 6 integers separated by space")
      
    process.process_input(user_input)    
        
if __name__ == "__main__":
    run_simulation()  
