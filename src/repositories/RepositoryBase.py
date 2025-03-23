from db.sqlite import dbConnectionInstance
from Entities.QueryResult import QueryResult

'''
    This abstract base class will be used to define our main methods of interacting with specific tables

    One thing that is good about python is we can define an abstract *args param , and then specify a list 
    of accepted args , meaning in a single method signature we can define behaviour for all query filters and 
    conditinally add them as needed, though to validate we will need to be explicit about the accepted args and their types.

    The blessing and curse of a dynamically typed language means I need to add a lod of boilerplate to validate our data integrity
    this is especially important when working with databases since it will try to case to the column type , failing that will 
    cause an error to be thrown.
'''

class RepositoryBase:
    def __init__(self):
        pass
        