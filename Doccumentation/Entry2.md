For the second day of my work I decided I wanted to develop some usefull tools for me to use in development

Namely I wanted to be able to map query results to defined data objects , often reffered to as Data Transfer Objects or 'Dto'
To do this I first of all decided to create a QueryResult class that I can use to define validation methods for query results such as assetting a query only has one record , or that it can be null

I then started working to define the Mappable base class that all of my Dto's will inherit from and the generic method used to try mapping a QueryResult to a Mappable object , to do this I used pythons classmethod along with the class decorator @dataclasss, this allowed me to pass the class type of subclasses of Mappable to a method defined in the base as Map() , then using reflection I can look at the __dataclass__fields__ dictionary to iterate over the expected fields / types a dto requires, eventually validating them against the qery result column map and then building the dataclass instances from the results.

I hope I explained that well, but if not take a look at Mappable.py and you will see what I mean.

I then wanted to create a developer friendly way to view the results of a mapped query dto, Ideally I would just use an external library to save me time but since it was requested to avoid these if possible I will try to code my own, should be a simple case of printing a table like view of the array of Mappable objects , though to do this I will need to extend the list base type in python to include a .PrintTable() method that is only accessable on a list of Mappable objects.



The Next challenge I decided to take was to define a generic validator for validing dyanmic SQL parameters, I wanted to have at least some prevention of SQL Injection otherwise its just plainly a terrible program.