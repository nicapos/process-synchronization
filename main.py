
import process
import sys

def main():
    
    user_input = input()
    if len(user_input.split()) != 6:
        print("Invalid input, must be 6 integers separated by space")
        sys.exit(0)

    process.process_input(user_input)

if __name__ == "__main__":
    main()
