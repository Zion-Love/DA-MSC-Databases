### Getting started with sqlite3

I wanted to begin first by learning to establish a connection to a sqlite3 database

after doing this I wanted to look at creating a factory for managing database transactions , this would in future allow me to desigg my querying independtantly and rollback entire transaction blocks should a dependant query fail

I have had some experience doing this in the past using python3 and Postgres so I was confident I knew where to start, that being said I dont like pushing raw sql to the db as it is bad practice in general


After setting this up I created a CreateTestData.sql file that I can use to build my intial database state upon launching my applicaiton, for this I included a flag to refresh the database on init_db so i can start from fresh whenever I need to.

In an actuall application I would use a similar method for creating a test database, although depending on code-first vs db-first I would either inflect the db state from remote to build the tables / orm classes from, OR build them from the ORM setup, since we were asked not to use existing ORM like sqlalchemy for our project, i started thinking about creating a very barebones one to make my own life easier , at least a base class for mapping a dataclass to a query result, handling missing columns mapping explicitly etc


Surrounding all of this I also setup up my dbeaver installation to conenct to the local sqlite database , this would allow me to test externally to verify data state without needing to explicitly do it in code and re running the applicaiton, 

I could also then test sql queries directly on the db connection instead of having to pass them through the python api, with the ability to refresh the entire db based on a single file I can confidently play around and break my db setup to my hearts content knowing full well that I can get back to a stable state if need be.