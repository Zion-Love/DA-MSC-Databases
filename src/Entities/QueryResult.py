from db.sqlite import dbConnectionInstance

class QueryResult:

    def __init__(self, query : str):
        # store query next to result for debugging
        self.query = query

        # perform query agaisnt db
        with(dbConnectionInstance.Get_Transaction() as transaction):
            self.cursor = transaction.execute(query)
            self.result = self.cursor.fetchall()


    def AssertSingleOrNull(self):
        if(not len(self.result) <= 1):
            raise Exception(f"Query : {self.query} Expected 1 or no results, instead got : {len(self.result)} \n {self.result}")
        return self


    def AssertSingle(self):
        if(not len(self.result) == 1):
            raise Exception(f"Query : {self.query} Expected exactly 1 result, instead got : {len(self.result)} \n {self.result}")
        return self
            
        
