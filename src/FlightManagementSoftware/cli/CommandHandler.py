from abc import ABC, abstractmethod
from dataclasses import dataclass
from FlightManagementSoftware.cli.UserInputHelpers import AbortCommandException

'''
    Abstract base class for our cli command objects , this will allow me to have command specific argument validation
    but the overall process is callable through the base type.
'''
@dataclass
class CommandHandler(ABC):
    # Post init class to run on handlers such that we can just do result = Handler(options)
    # Commands have no real need to return data since I am not integrating this into any other application
    # an api layer would be responsible for determining how to handle any data returned in a Command but that is out of scope for this project
    def __post_init__(self):
        try:
            self.Validate()
            self.Handle()
        except AbortCommandException as e:
            print(f"Command Aborted : {e}")


    @abstractmethod
    def Validate(self):
        raise NotImplementedError()

    @abstractmethod
    def Handle(self):
        raise NotImplementedError()
    

