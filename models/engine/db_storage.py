#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from models.user import User
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review


class DbStorage:
    """This class manages db storage for hbnb clone"""
    __engine = None
    __session = None
    def __init__(self):
        user = os.getenv("HBNB_MYSQL_USER")
        pwd = os.getenv("HBNB_MYSQL_PWD")
        host = os.getenv("HBNB_MYSQL_HOST")
        db = os.getenv("HBNB_MYSQL_DB")
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(user, pwd, host, db), pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        new_dict = {}
        if cls is None:
            #Loop through all the classes and query each class
            classes = [User, State, City, Amenity, Place, Review]
            for c in classes:
                results = self.__session.query(c).all()
                for obj in results:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        else:
            #Query one clss
            results = self.__session.query(cls).all()
            for obj in results:
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
        return new_dict
    
    def new(self, obj):
        """Adds a new object to the database"""
        self.__session.add(obj)

    def save(self):
        """Saves the new object to the database by commiting changes"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes an object from the database"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """Creates a session  for creation of the tables"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        self.__session = scoped_session(session_factory)