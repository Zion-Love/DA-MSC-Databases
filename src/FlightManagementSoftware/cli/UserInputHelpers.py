
'''
    A reusable helper function for commands that have confirmation steps
'''

class AbortCommandException(Exception):
    def __init__(self, *args):
        super().__init__(*args)

# Simple function to request confirmation and cancel should it not be recieved
def ContinueYN(warningMessage : str = "WARNING: Execution paused Continue ? (y/n)"):
    print(warningMessage)
    userInput = input()
    if userInput.lower() in ['y', 'yes']:
        pass
    elif userInput.lower() in ['n', 'no']:
        raise AbortCommandException("Operation aborted by user input")
    else:
        raise AbortCommandException(f"Un-recognized input expected 'y' or 'n' instead got '{userInput}', Operation cancelled.")