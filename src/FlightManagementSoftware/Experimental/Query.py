from Entities.EntityBase import (
    EntityBase, 
    Column, 
    MissingColumnException, 
    ForeignKeyConstraint, 
    PrimaryKeyConstraint
)
from typing import List, enum, Any
import inspect
import re

class QueryBasic:
    # this was a bit tricky to get generically working , I wanted to create a method to validate querys and their parameters
    # but I wanted this to be dynamic and not accepting kwargs as with kwargs I would need explcititly define key , values , types
    # but using args means I require individual parameter parsing rather than generic dictionary, this means I can validate that the query
    # and all variables denoted using a variabeName = ?
    def __init__(self, query : str , * args):
        methodSignature = inspect.signature(self.__init__)
        parameters = list(methodSignature.parameters.values())
        self.parameters = []

        # verify the count of ? to parameters matches
        numberOfParamsInQuery = len(re.findall('?', query))
        if(len(args) != numberOfParamsInQuery):
            raise Exception("Number of parameters in query does not match number supplied")

        # used to track where in the query we are finding this parameter name, for this to work we need to make sure
        # our parameters are supplied in the same order from left to right as our query has defined them, this is because
        # using the sqlite escape formatting we need to supple our query with param = ? where the ? will be replaced by properly escaped
        # parameters supplied as *args to the .execute function
        # I could try to convert the ordering here to be more lenient to development , but I think verbosely 
        # excepting will give more insight and provide me with a more consistently right query in the end
        # regex was built and tested using https://regex101.com/ 
        paramIndex = 0

        # validate we dont have any sameNamed parameters
        paramSet = set([param.name for param in parameters])

        if(len(paramSet) != len(parameters)):
            raise Exception("Duplicate parameter names supplied to query")

        for i , value in enumerate(args):
            paramName = parameters[2 + i].name

            # ensure our param name is in the query , parameters COULD be either surrounded by ' ' OR the left hand side could be a .
            # in the case of multiple tables with alias sharing column names
            # the following regex pattern should detect this.
            regexPattern = r'(?<=[\s\.])' +  {paramName} + r'(?=\s)'
            strMatch = re.search(regexPattern,query)
            patternMatchIndex = strMatch.start()

            # always ensure the next iteration is looking ahead of the previously matched index
            if(patternMatchIndex < paramIndex):
                raise Exception(f"Query Parameter ordering does not match : {query} \n : {args}")
            paramIndex = patternMatchIndex

            # for param matching lists, to avoid having to do (?,?,?) and supplying each as a param1_1= param1_2 = ...
            # I am using string aggregation here to combine each into a tuple like ('value1', 'value2')
            if(issubclass(value, list) or isinstance(value, list)):
                parameterString = str.join(', ', value)
                continue


      
# likely only need these join types to translate
class EJoinType(enum):
    Left = "LEFT JOIN"
    Right = "RIGHT JOIN"


class JoinCondition:
    def __init__(self, sourceEntity : EntityBase, 
                 targetEntity : EntityBase, 
                 sourceColumn : Column, 
                 targetColumn : Column, 
                 JoinType : EJoinType):
        self.JoinType =  JoinType
        self.sourceEntity = sourceEntity
        self.sourceColumn = sourceColumn
        self.targetEntity = targetEntity
        self.targetColumn = targetColumn
 
    # alias table as table name to avoid conflicting column names making query fail...
    def Translate(self):
        return f'''
            {self.JoinType} {self.targetEntity.Name} {self.targetEntity.Name}
                ON {self.targetEntity.Name}.{self.sourceColumn} = {self.targetColumn} \n
        '''


# Designed like an ORM , this helps to reduce the need to supply raw sql commands to the database
# with proper value validation it should prevent SQL injection as well as provide a developer friendly way
# of constructing querys against our code based mapping
'''
    Joins , orders , selects all of the functions here represent basic query syntax operationsas such will be applied to the 
    query itself and not operate on in-memory data 
    (though since using sqlite3 locally its technically all in-memory just not in RAM, but lets not argue semantics ey)

    also it would be a real pain to implement all potential aggregate functions / conditions within this class

    so I probably wont do that :)
'''
class Query:
    # our base entity is the table that is ALWAYS selected from 
    def __init__(self, sourceEntity : EntityBase):
        self.BaseEntity : EntityBase
        self.selectedEntites = {self.BaseEntity : []}
        self.JoinConditions : List[JoinCondition] = []
        self.Parameters = {}


    def Select(self, columnNames : str): 
        raise NotImplementedError()       
    

    def Join(self, 
             joinType : EJoinType,
             targetEntity : EntityBase, 
             targetColumnName : Column, 
             sourceEntity : EntityBase = None, 
             sourceColumn : Column = None):
        # TODO validate join conditions, entity exists with target column , column is a foreign key to one of our selected entites
        targetColumn = targetEntity.GetColumn(targetColumnName)

        if(sourceEntity != None or sourceColumn != None):
            if(sourceEntity == None or sourceColumn == None):
                raise Exception("To join using a source entity / column you must supply info for both")

        # Validate we have that relationship
        for constraint in targetColumn.constraints:
            if type(constraint) == ForeignKeyConstraint:
                break
        
        joinValid = False
        for entity in self.selectedEntites:
            if entity == targetEntity:
                continue
            try:
                column = entity.
            except MissingColumnException as e:
                continue
        joinCondition = JoinCondition(JoinType=joinType)
    
        pass
    
    def Where(self , targetColumn : str, targetValue : Any):
        column = None
        for entity in self.selectedEntites:
            try:
                column = entity.GetColumn(targetColumn)
                break
            except MissingColumnException as e:
                continue

        if column == None:
            raise Exception(f"Query contains no entities with column : {targetColumn} , Selected entities : {self.selectedEntites}")
        
        # get our column type...

    def OrderBy(self, targetColumn : str, ascendingOrDescending : str = 'ascending'):
        if(ascendingOrDescending.lower() != 'ascending' or ascendingOrDescending.lower() != 'descending'):
            raise Exception(f"expected ascending or descending , instead got {ascendingOrDescending}")
        
        raise NotImplementedError()
        

    # translate our mapped query object into an executable sql query
    def Translate(self) :
        return f'''
            SELECT * FROM {self.BaseEntity.Name}
            {str.join([join.Translate() for join in self.JoinConditions])}
        '''