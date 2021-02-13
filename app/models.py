from datetime import datetime
from flask_login import UserMixin
from flask_sqlalchemy import BaseQuery
from app import db

class APIMix(object):
    @staticmethod
    def to_collection_dict(query):
        
        data = {
            'items' : [item.to_dict() for item in query]
           
        }
        return data

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))

class Temperature(APIMix, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    thermosensor_id = db.Column(db.String(50))
    temperature = db.Column(db.Float)
    date = db.Column(db.DateTime)

    def to_dict(self, include_email=False):
        data = {
            'id': self.id,
            'thermosensor_id': self.thermosensor_id,
            'temperature': self.temperature,
            'date': self.date
        }
        
        return data

