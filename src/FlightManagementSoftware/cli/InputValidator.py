from datetime import datetime
import re
from typing import Any

'''
    In an actual production I would use something like pydantic to validate models as they are bound 
'''

def AssertIsPositiveInteger(val: Any) -> int:
    if(val == None or val < 0):
        raise Exception(f"Expected a positive integer , instead got : {val}")
    return val



def AssertStringIsOneOf(val: Any, validStrings: list[str]) -> str:
    if not val in validStrings:
        raise Exception(f"Expected string to be one of {validStrings} instead got {val}")
    return val


# for the sake of this applications consistency I will be expecting all datetimes to be in one of two formats
def AssertDateTimeString(val: Any) -> datetime:
    expectedDateTimeFormat = r'%Y-%m-%d %H:%M:%S'
    alternativeDateTimeFormat = r'%Y-%m-%d'
    try:
        dt = datetime.strptime(val, expectedDateTimeFormat)
    except Exception as e:
        dt = datetime.strptime(val, alternativeDateTimeFormat)
    return dt


def AssertStringIsBoolean(val : Any) -> bool:
    if(isinstance(val, str)):
        lowercaseVal = val.lower()

        if lowercaseVal in ['true','yes']:
            return True
    
        if lowercaseVal in ['false', 'no']:
            return False


def AssertStringNotEmpty(val : Any) -> str:
    assert isinstance(val,str), f"Expected string instead got : {type(val)}"
    # using regex to strip all whitespace...
    assert len(re.sub('^(\s+)', '', val)) > 0
    return val


def AssertDateAIsBeforeDateB(dateA : datetime, dateB :datetime):
    assert dateA < dateB