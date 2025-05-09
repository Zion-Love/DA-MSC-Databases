
from typing import Any
from dataclasses import fields
from FlightManagementSoftware.Entities.QueryResult import QueryResult

class Mappable:
    def __init__(self):
        raise TypeError("Mappable is not a instantiatable type, it must be inherited")

    @classmethod
    def Map(cls, queryResult : QueryResult) -> list[Any]:

        if not isinstance(queryResult, QueryResult):
            raise Exception(f".Map must be called with a queryResult, instead got : {type(queryResult).__name__}")
      
        dataClassFields = fields(cls)

        # using set manipulation to verify our result contains all of our mapping fields
        # this does assume our query must have all the same fields as our mapping class
        # we COULD only map those we find and dispose of the rest of the data
        # but I think that would be bad practice in terms of development
        # data could get lost and we could needlessly be querying for columns we are not using
        # resulting in silently more expensive queries than neccessary 
        incomingColumnIndexMapping = {description[0] : i for i, description in enumerate(queryResult.cursor.description)}
        incomingColumnNames = set(incomingColumnIndexMapping.keys())
        expectedColumnNames = set([f.name for f in dataClassFields])
        setDifference = incomingColumnNames - expectedColumnNames
        if(len(setDifference) != 0):
           print(queryResult.query)
           raise Exception(f"dataClassFields and QueryResult do not match : \n QUERY : {sorted(list(incomingColumnNames))} \n MAPPING  : {sorted(list(expectedColumnNames))}")
        
        result = []
        if len(queryResult.result) == 0 or queryResult.result == None:
            return None

        for i in range(0,len(queryResult.result)):
            objectInstanceKwargs = dict()
            for dataField in dataClassFields:
                objectInstanceKwargs[dataField.name] = queryResult.result[i][incomingColumnIndexMapping[dataField.name]]
            result.append(cls(**objectInstanceKwargs))
        
        return result
    