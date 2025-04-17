import sqlite3
from sqlite3 import Connection, Cursor
from contextlib import contextmanager
import os
import pkg_resources
from typing import Generator


'''
    The following class SqliteDbConnection is used to:
      - Abstract build-up / tear-down of our database
      - wrap database transaction blocks

    This allows me to write querys that are dependant on one another whilst providing a session safe way to rollback should
    dependant queries fail.

    Every query should likely exist within a transaction block , this would mean I am handling exceptions consistently throughout my program
    and I should not need to explicitly flush / commit to the database outside of this class

    using the contextlib class to negate the need to define __enter__ and __exit__ methods for my context factory   

    I would like to setup a CreateFromEntityMap function in here of which would reflect all classes inheriting from EntityBase in my codebase
    and create the tables dynamically from that , this would however mean pretty much creating my owm ORM of sorts, likely outside the scope of this project.
'''

CREATE_TABLE_RESOUCE = 'sql/CreateTables.sql'
TEST_DATA_RESOURCE =  'sql/CreateTestData.sql'


class SqliteDbConnection:
    def __init__(self):
        self.relative_path : str = os.path.dirname(__file__)
        self.conn : Connection = None
        self.Init_db(refresh=False)

    def Is_Online(self) -> bool:
        try:
            if(self.conn == None):
                self.Init_db(False)
            qry = self.conn.execute("SELECT 1;").fetchone()
            return qry != None and qry[0] == 1
        except Exception as e:
            print("Database connection not online")
            return False
    

    # used with using(db.Get_transaction() as transaction)
    # to create db sesssions for multiple statement execution and allowing
    # us to provide rollback operations to an entire transaction on failure
    # will protect against dependant operations failing
    @contextmanager
    def Get_Transaction(self) -> Generator[Cursor, None, None]:
        if(self.conn == None):
            self.Init_db(False)
        cursor = self.conn.cursor()
        # Creates an auto rollback on exception transaction block 
        try:
            cursor.execute("BEGIN TRANSACTION")
            yield cursor
            self.conn.commit()
        except Exception as e:
            self.conn.rollback()
            print(f"Exception {e} occured in transaction block, rolling back...")
            raise e
        finally:
            cursor.close()


    def Init_db(self, refresh : bool = True):
        # using relative path to keep database contained in same directory as project
        db_file = self.relative_path + '/database.sqlite3'
        print("Initisalising db")
        if(not os.path.isfile(db_file)):
            print("Could not find existing database file , creating new one...")
            refresh = True
        self.conn = sqlite3.connect(db_file)

        # Without proper ORM reflection here we dont neccessarily know if our db matches the expected tables in our application
        # Honestly I would never do this with raw sql , even using a db first setup I would want to run a test reflecting the db 
        # to ensure our code tables etc match that of our db
        if(refresh == False): 
            print("db initialized")
            return
        
        print("Rebuilding : tearing down db...")

        # Query to see if database contains any data currently
        query : str = "SELECT COUNT(*) from sqlite_master WHERE type='table';"
        query_result = self.conn.execute(query).fetchone()
        table_count = query_result[0] if query_result else 0

        if(table_count > 0 and refresh == False):
            raise Exception("Existing data found in database , please either provide refresh=True or manually review the database data")

        # clear existing data from database before populating with hard coded test data
        # easiest way of doing this with inmemory local db, is just to delete the file and recreate it
        # I had issues with this because I was using WSL2 and creating the file within a windows mnted drive location
        # To remedy it i had to give permission to WSL 2 to that specific directory
        if(table_count > 0 and refresh == True):
            os.chmod(db_file, 0o777)
            os.remove(db_file)
            self.conn = sqlite3.connect(db_file)

        # Refference to a hardcoded sql file containing all the setup requirements for the database
        # things like tble definitions and test data used by the application
        testDataFile : str = pkg_resources.resource_filename('FlightManagementSoftware', TEST_DATA_RESOURCE)
        createTableFile : str = pkg_resources.resource_filename('FlightManagementSoftware', CREATE_TABLE_RESOUCE)

        if(not os.path.isfile(testDataFile)):
            raise Exception("Cannot find ../sql/CreateTestData.sql db initialization aborted")
        
        if(not os.path.isfile(createTableFile)):
            raise Exception("Cannot find ../sql/CreateTables.sql db initialization aborted")
        
        print("building up database...")
        
        with(self.Get_Transaction() as transaction):
                try:
                    # Run CreateTables.sql first 
                    with(open(createTableFile, 'r') as createTableFile):
                        createTableSql = createTableFile.read()
                        transaction.executescript(createTableSql)

                    # Run CreateTestData.sql second to populate our tables with test data
                    with(open(testDataFile, 'r') as testDataFile):
                        testDataSql = testDataFile.read()
                        transaction.executescript(testDataSql)
                except Exception as e:
                            raise Exception(f"Unexpected Exception executing db command : \n {e}")
                
        print("db initialized")


dbConnectionInstance = SqliteDbConnection()
