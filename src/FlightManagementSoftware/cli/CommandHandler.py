from abc import ABC, abstractmethod
from dataclasses import dataclass, fields, MISSING

from Exceptions.ValidationException import ValidationException
'''
    Abstract base class for our cli command objects , this will allow me to have command specific argument validation
    but the overall process is callable through the base type.
'''

@dataclass
class CommandHandler(ABC):
    # Post init class to run on handlers such that we can just do result = Handler(options)
    # a lot of commands will not return a specific result and instead just print information to the screen.
    @abstractmethod
    def __post_init__(self):
        self.Validate()
        self.Handle()

    @abstractmethod
    def Validate(self):
        raise NotImplementedError()

    @abstractmethod
    def Handle(self):
        raise NotImplementedError()
    
    '''
        This method will try to convert a kwargs dictionary into an instance of thie CommandHandler

        by also checking the field default declaration to see if that variable is explicitly required
        or if it can be defaulted by the class itself, this handles None cases since dataclasses.MISSING
        is not equavalent to None, so deafulting a value to None is ok and will not throw here.
    '''
    @classmethod
    def FromKwargs(cls, **kwargs):
        
        myFieldsNames = {f.name : f.default  for f in fields(cls)}
        if len(set(myFieldsNames) != len(myFieldsNames)):
            raise ValidationException(f"Duplicate parameters found during Command {cls.__name__} paramater construction : {kwargs}")
        
        missingRequiredFieldsInKwargs : dict = {fieldName : defaultValue for fieldName, defaultValue in myFieldsNames 
                                         if fieldName not in kwargs.keys() 
                                         and defaultValue != MISSING}
        if len(missingRequiredFieldsInKwargs != 0):
            raise ValidationException(f"Missing required fields for Command  : {cls.__name__} missing fields : {missingRequiredFieldsInKwargs.keys()}")

        return cls(**kwargs)
       

