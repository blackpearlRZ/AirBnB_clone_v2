#!/usr/bin/python3
""" A module that contains the class engine DBStorage """
from os import getenv
from models.city import City
from models.state import State
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.base_model import Base

# Getting the value of the enviromental variables
user = getenv('HBNB_MYSQL_USER')
passwd = getenv('HBNB_MYSQL_PWD')
host = getenv('HBNB_MYSQL_HOST')
db = getenv('HBNB_MYSQL_DB')
hbnb_env = getenv('HBNB_ENV')

# Preparing the engine URL
url = f"mysql+mysqldb://{user}:{passwd}@{host}:3306/{db}"


class DBStorage():
    """ A Database engine class """
    __engine = None
    __session = None

    def __init__(self):
        """ Instantiation of attributes """
        self.__engine = create_engine(url, pool_pre_ping=True)

        # Drop All tables if env_var HBNB_ENV equals "test"
        if hbnb_env == 'test':
            self.__engine.execute("DROP TABLE IF EXISTS {}".format(hbnb_env))

    def all(self, cls=None):
        """ Return the query of all objects """
        objects = {}
        # if cls_name is not given we loop over all classes
        if cls is None:
            classes = [User, State, City, Amenity, Place, Review]
            for cls in classes:
                objs_cls = self.__session.query(cls).all()
                # we loop over the query to get all objs of cls
                for obj in objs_cls:
                    key = obj.__class__.__name__ + "." + str(obj.id)
                    objects[key] = obj
        # if cls_name is not given we just get all objs of the given cls
        else:
            obj_cls = self.__session.query(cls).all()
            for obj in obj_cls:
                key = obj.__class__.__name__ + "." + str(obj.id)
                objects[key] = obj
        return objects

    def new(self, obj):
        """ Adds the object to the current database session """
        self.__session.add(obj)

    def save(self):
        """ Commits all changes of the current database session """
        self.__session.commit()

    def delete(self, obj=None):
        """ Deletes from the current database session obj if not None """
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """ Creates all tables and thecurrent database session """
        from models.state import State
        from models.user import User
        from models.place import Place
        from models.review import Review
        from models.amenity import Amenity
        # Create all tables in the database
        Base.metadata.create_all(self.__engine)
        # Creating the current database session
        self.__session = sessionmaker(bind=self.__engine,
                                      expire_on_commit=False)
        self.__session = scoped_session(self.__session)

    def close(self):
        """ Closes the current session """
        self.__session.remove()
