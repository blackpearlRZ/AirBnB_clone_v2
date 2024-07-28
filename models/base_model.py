#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from os import environ

Base = declarative_base()


class BaseModel:
    """A base class for all hbnb models"""
    __abstract__ = True
    id = Column(String(60), unique=True, nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.now(), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(), nullable=False)

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
        else:
            for k, v in kwargs.items():
                if k != "__class__":
                    setattr(self, k, v)
            self.id = kwargs.get("id", str(uuid.uuid4()))
            self.created_at = kwargs.get("created_at", datetime.now())
            self.updated_at = kwargs.get("updated_at", datetime.now())

    def __repr__(self):
        """Returns a string representation of the instance"""
        str_rep = self.__dict__
        try:
            del(str_rep["_sa_instance_state"])
        except KeyError:
            pass
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]
        return '[{}] ({}) {}'.format(cls, self.id, str_rep)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.__dict__["updated_at"] = datetime.now()
        storage.new(self)
        storage.save()

    def delete(self):
        from models import storage
        storage.delete(self)

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        try:
            dictionary['created_at'] = self.created_at.isoformat()
            dictionary['updated_at'] = self.updated_at.isoformat()
        except Exception:
            pass
        try:
            del(dictionary["_sa_instance_state"])
        except Exception:
            pass
        return dictionary
