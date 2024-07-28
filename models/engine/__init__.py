#!/usr/bin/python3
"""This module instantiates an object of class FileStorage"""
from os import getenv
from models.engine.file_storage import FileStorage
from models.engine.db_storage import DBStorage

# Conditional depending on the value of the env var HBNB_TYPE_STORAGE
env = getenv('HBNB_TYPE_STORAGE')

if env == 'db':
    storage = DBStorage()
    storage.reload()
else:
    storage = FileStorage()
    storage.reload()
