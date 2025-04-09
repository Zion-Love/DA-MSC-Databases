from argparse import ArgumentParser
from abc import ABC, abstractmethod
from dataclasses import fields
from FlightManagementSoftware.cli.CommandHandler import CommandHandler


'''
    This base class is used to template our cli -> command execution

    I built things like this such that in a real world application, instead of CLI I could easily create other object to interact with
    my exposed commands , an api could work in a simlar way and not need much bespoke implementation to execute the same commands against my data
    this abstracts the FE (in this case CLI) from the implementation of the Command business logic

    In theory I could run both cli as defined here and an api to execute the same commands, a use case could be 
    a secure console on the machine the database is stored could require the cli implementation without all the remote connectivity considerations
    but someone working from a remote location would need to interact through an API with proper access controlled authentication processess
    these are two completely seperate concerns but the underlying logic they need to execute is shared.
'''
class CommandParser(ABC):
    def __init__(self, handler : CommandHandler):
        if(not issubclass(handler,CommandHandler)):
            raise Exception(f"CommandParser requires a CommandHandler to initialize")
        self.handler = handler
        

    def run(self, **kwargs):
        handlerFields = [f.name for f in fields(self.handler)]
        filteredKwargs = {k : v for k,v in kwargs.items() if k in handlerFields and v != None}
        print(f"Calling command : {self.handler.__name__} with args : {filteredKwargs}")
        self.handler(**filteredKwargs)


    @abstractmethod
    def BuildCommandArgs(self, parser : ArgumentParser) -> ArgumentParser:
        raise NotImplementedError()
