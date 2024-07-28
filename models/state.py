#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from os import environ


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship("City", backref='state',
                          cascade="all, delete-orphan")

    if not environ.get('HBNB_TYPE_STORAGE') == "db":
        @property
        def cities(self):
            from models import storage
            cities_list = [city for _, city in storage.all("City").items()
                           if city.state_id == self.id]
            return cities_list
