from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = 'sqlite:///./todos.db'
# saying that the database will be in this directory of todo app

"""
now we need to create an engine; a database engine is what we use to be able to
open up a connection and be able to use our database.
connect arguments are the arguments that we can pass to the create engine to allow us to
be able to define some kind of connection to a database.
by default SQLite will allow only one thread to communicate with it. Assuming that each thread
will handle an independent request. This is to prevent any kind of accident sharing of the same 
connection for different kind of requests. but in fastapi it's very normal to have more than one
thread that could interact with the database at the same time. and we set it to false to say we 
don't want to be checking the same thread all the time because it could be multiple threads happening
to the SQLite database.
"""
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={'check_same_thread': False})


"""
Now we need to create a session local and each instance of the session local will have a database session.
The class itself is not a database session yet, we'll add that later. for now we just need to be able to 
create an instance of the session local that will be able to become an actual database in the future.
so we say: we want the session local, which we'll use in out application. when we use session local, we want
to bind to the engine that we created, and autocommits and autoflushes are set to false, or the database transactions
are going to try to do something automatically. and we want to be fully control of everything out database will do in the future.
"""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


"""
Last thing we need to do is make sure that we can create a database object that we can then interact with later on.
So we want to be able to call our database.py file, be able to create a base which is an object of the database, which
is going to be able to then control our database.
what it means is that we're going to be creating database tables and then here in the database.py we're going to be able
to create an object of our database which will then be able to interact with the tables that we create in the future.
"""
Base = declarative_base()