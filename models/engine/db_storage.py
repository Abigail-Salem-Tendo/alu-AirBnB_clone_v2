#!/usr/bin/python3
"""This module defines a class to manage db storage for hbnb clone"""
import os
from models.base_model import BaseModel, Base
from sqlalchemy import create_engine

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