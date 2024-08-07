#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime
import os


if os.getenv('HBNB_TYPE_STORAGE') == 'db' :
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """A base class for all hbnb models"""
    id = Column(String(60),
                nullable=False,
                primary_key=True)
    created_at = Column(DateTime,
                        nullable=False,
                        default=datetime.now())
    updated_at = Column(DateTime,
                        nullable=False,
                        default=datetime.now())

    def __init__(self, *args, **kwargs):
        """Instatntiates a new model"""
        self.id = str(uuid.uuid4())
        if not kwargs:
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key, value in kwargs.items():
                if key == "created_at" or key == "updated_at":
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != "__class__":
                    setattr(self, key, value)
            if 'created_at' not in kwargs:
                self.created_at = datetime.now()
            if 'updated_at' not in kwargs:
                self.updated_at = datetime.now()

    def __str__(self):
        """Returns a string representation of the instance"""
        cls = (str(type(self)).split('.')[-1]).split('\'')[0]

        filtered_dict = {key: value for key, value in self.__dict__.items() if key not in ['_sa_instance_state', 'cities', '__class__']}   
        return '[{}] ({}) {}'.format(cls, self.id, filtered_dict)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dict format"""
        dictionary = {}
        dictionary.update(self.__dict__)
        dictionary.update({'__class__':
                          (str(type(self)).split('.')[-1]).split('\'')[0]})
        dictionary['created_at'] = self.created_at.isoformat()
        dictionary['updated_at'] = self.updated_at.isoformat()

        if '_sa_instance_state' in dictionary:
            del dictionary['_sa_instance_state']
        # del dictionary['__class__']
        return dictionary

    def delete(self):
        """ delete current instance from storage """
        for key, value in self.__objects.items():
            flag = False
            if value.id == self.id:
                flag = True
                wanted_key = key
                break
        if flag:
            del self.__objects[wanted_key]
            self.save()