from tabulate import tabulate
from dataclasses import fields
from FlightManagementSoftware.DataTransferObjects.Mappable import Mappable

'''
    Defining a rudimentary DataFrame type similar to pandas 

    here though it is such I can define only the methods I need

    it would never be aas optimised as Pandas which I believe is written in cython, but since we were asked to avoid
    external libraries where possible I have to implement my own way of viewing data from query results

    should I ever need to though I could write Pivot / ordering / aggregation function logic here to perform on in-memory data

    but for this project I doubt I would need to do that...
'''

class DataFrame:
    # Requires a provided mappable type, though
    def __init__(self, data : list[Mappable], _type : Mappable):

        if(not issubclass(_type, Mappable)):
            raise Exception("A Dataframe can only be constructed using a Mappable subclass")
        
        self.type = _type

        if data == None or len(data) == 0:
            self.data = []
            return
        
        if(not all(type(d) == self.type for d in data)):
            raise Exception(f"Data supplied to DataFrame does not match its assigned type {self.type}")

        self.data = data
        

    def remove(self, index : int):
        self.data.remove(self.data[index])


    def append(self, data):
        if(not issubclass(data, self.type)):
            raise Exception(f"Cannot append object of type : {type(data)} to DataFrame of type : {self.type}")
        self.data.append(data)


    # Operator overloading of default printing logic to call to tabulate and print data as a user readable table
    def __str__(self):
        # firstly convert to single dictionary using dictionary / list comprehension
        # this will result in a dictionary where each column name has a list of all the value from each object instance
        # in the same order as the original data set
        if self.data == []:
            # no data so just print the column headers
            dataDict = {column.name : [] for column in fields(self.type)}    
        else:
            dataDict = {column.name : [item.__getattribute__(column.name) for item in self.data] for column in fields(self.type)}
        tableData = zip(*[value for key ,value in dataDict.items()])
        return tabulate(tableData, headers=dataDict.keys(), floatfmt=".2f",missingval='-')


    # operator overload for calling DataFrame[index] to retrive item from DataFrame.data also works with DataFrame[x:y]
    def __getitem__(self, index):
        if(isinstance(index, slice)):
            return DataFrame(self.data[index.start:index.stop:index.step], self.type)
        
        return self.data[index]
