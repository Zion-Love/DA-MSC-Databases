from typing import List, Any
from datetime import datetime
import enum

class EJoinType(enum):
    Left = 1  # Keep all records from left hand table
    Right = 2 # Keep all records from right hand table
    Cross = 3 # keep only intersecting records

class EColumnConstraintType(enum):
    PrimaryKey = 1
    ForeignKey = 2
    MaxLength = 3
    MinLength = 4
    Nullable = 5
    Unique = 6
    Default = 7

class ColumnConstraint:
    def __init__(self, Name  : str, Type : EColumnConstraintType , value : Any):
        self.Name = Name
        self.Type = Type
        self.value = value

class PrimaryKeyConstraint(ColumnConstraint):
    def __init__(self, sourceClass : type, sourceColumn : str):
        self.sourceClass = sourceClass
        name = f"PK_{sourceClass.__name__}_{sourceColumn}"
        super().__init__(name, EColumnConstraintType.PrimaryKey)


class ForeignKeyConstraint(ColumnConstraint):
    def __init__(self, sourceClass : type, sourceColumn : str, targetClass : type, targetColumn : str):
        # Some basic reflection to ensure our table has a desired FK column
        if(not hasattr(sourceClass, sourceColumn)):
            raise Exception(f"{sourceClass} does not contain an attribute for {sourceColumn}")
        if(not hasattr(targetClass, targetColumn)):
            raise Exception(f"{targetClass} does not contain an attribute for {targetColumn}")
        
        self.sourceClass = sourceClass.__name__
        self.sourceColumn = sourceColumn
        self.targetClass = targetClass.__name__
        self.targetColumn = targetColumn
        self.Name = f"FK_{self.sourceClass.upper()}{self.sourceColumn}_{self.sourceColumn.upper()}{self.targetColumn}"
        super().__init__(self.Name, EColumnConstraintType.ForeignKey)


class Column:
    def __init__(self, Name : str, Type : type, constraints : List[ColumnConstraint] = None):
        self.Name = Name
        self.Type = Type
        if constraints != None : self.ValidateColumnConstraints(constraints)
        else : self.constraints = None

    def __str__(self):
        typeConversionString = ""
        match(self.Type):
            case type(int):
                typeConversionString = "int"
            case type(float):
                typeConversionString = "NUMERIC"
            case type(str):
                typeConversionString = "NVARCHAR"
            case type(datetime):
                typeConversionString = "DATETIME2"
        typeLengthConstraint = ""
        return f"{self.Name} {typeConversionString}"

    def ValidateColumnConstraints(self, constraints : List[ColumnConstraint]):
            hasPrimaryKey , hasForeignKey = False
            for constraint in constraints:
                if((hasPrimaryKey or hasForeignKey) and 
                   (constraint.Type == EColumnConstraintType.ForeignKey or constraint.Type == EColumnConstraintType.PrimaryKey)):
                    raise Exception("Column cannot contain more than one of either PrimaryKey or ForeignKeyConstraints")
                if(hasPrimaryKey and constraint.Type == EColumnConstraintType.Nullable):
                    raise Exception("Column cannot contain a Nullable constraint as well as a PrimaryKey constraint")
            # if(self.Type == type(float)):
            #     # for float types we require a max and min length constraint to define the column Numeric(min,max)
            self.constraints = constraints


# TODO : used for joining entitys together in querying 
# Ideally I can use a table refference and then join to any related table through a 
# .Join function
class ForeignTable:

    # on instantiation get the db defined constraints and verify that a fk exists...
    def __init__(self, sourceEntity : type, foreignEntity : type, column : str):
        if(not issubclass(sourceEntity, EntityBase) or not issubclass(foreignEntity, EntityBase)):
            raise Exception(f"Both sourceEntity : ({sourceEntity.__name__}) and foreignEntity: ({foreignEntity.__name__}) must be objects inheriting from EntityBase")
        pass


class EntityBase:
    
    def __init__(self, baseType : type):
        self.Name = baseType.__name__
        self.Columns : List[Column] = List()    

    # Find a column either by name and/or constraint type
    def GetColumn(self, name : str = None, type : EColumnConstraintType = None):
        for column in self.Columns:
            if(type == EColumnConstraintType.PrimaryKey and column.type == EColumnConstraintType.PrimaryKey):
                return column
            if(type == EColumnConstraintType.ForeignKey and column.type == EColumnConstraintType.ForeignKey):
                return column
            if(name == column.Name and (type == None or column.Type == type)):
                return column
        raise Exception(f"Could not find column with name / type : {name} / {type} in Entity : {type(self).__name__}")
    


    def Join(self, foreignTable : str):
        pass
            
    # this is a slightly presumptous method since it will be generating our create table methods
    # doing it like this is a sort of psuedo code first database setup
    # meaning if all goes well I wont have to manually match the definitions between db and codebase
    def GenerateCreateTableStatement(self, drop_existing : bool = True):
        statement : str = ''
        if(drop_existing):
            statement += f'DROP TABLE IF EXISTS {self};'



        return f''' CREATE TABLE {type(self).__name__} ()'''
    
    def CreateTable(self):
        raise NotImplementedError()
