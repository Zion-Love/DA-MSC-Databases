from abc import ABC, abstractmethod
from dataclasses import dataclass

'''
    Abstract base class for our cli command objects , this will allow me to have command specific argument validation
    but the overall process is callable through the base type.
'''
@dataclass
class CommandHandler(ABC):
    # Post init class to run on handlers such that we can just do result = Handler(options)
    # a lot of commands will not return a specific result and instead just print information to the screen.
    def __post_init__(self):
        self.Validate()
        self.Handle()

    @abstractmethod
    def Validate(self):
        raise NotImplementedError()

    @abstractmethod
    def Handle(self):
        raise NotImplementedError()
    

