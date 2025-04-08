class MissingColumnException(Exception):
    def __init__(self, entityName : str,columnName : str):
        print(f"Column : {columnName} does not exist for Entity : {entityName}")

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

    # TODO : Convert column object to executable query statement
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

    def ValidateColumnConstraints(self, constraints : list[ColumnConstraint]):
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

