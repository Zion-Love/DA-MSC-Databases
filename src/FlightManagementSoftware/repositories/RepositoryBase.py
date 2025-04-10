from FlightManagementSoftware.db.sqlite import dbConnectionInstance
from FlightManagementSoftware.Entities.QueryResult import QueryResult

'''
    This class doesnt do much other than mark our repositories

    If given time this would be used in the Initialization step to create
    Dependancy injection instances
'''
class RepositoryBase:
    def __init__(self):
        pass
