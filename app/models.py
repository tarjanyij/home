import base64
import os
from datetime import datetime, timedelta
from flask_login import UserMixin
from flask_sqlalchemy import BaseQuery
from sqlalchemy import ForeignKey, Index
from sqlalchemy.orm import relationship
from werkzeug.security import generate_password_hash, check_password_hash
from app import db

class APIMix(object):
    @staticmethod
    def to_collection_dict(query):
        
        data = {
            'items' : [item.to_dict() for item in query]           
        }
        return data

class UserMix(object):
    @staticmethod
    def to_collection_dict(query):
        data = {
            'items' : [item.to_dict() for item in query]
        }
        return data

class User(UserMix, UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True) # primary keys are required by SQLAlchemy
    email = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    name = db.Column(db.String(1000))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    # Relationships
    roles = db.relationship('Role', secondary='user_roles',
                backref=db.backref('users', lazy='dynamic'))


    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now:
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        self.token_expiration = now + timedelta(seconds=3600)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)
        
    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user
    
    def to_dict(self):
        data = {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'name': self.name,
            'rolename' : self.roles[0].rolename,
            'roleid' : self.roles[0].id
        }
        return data

# Define the Role data model
class Role(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    rolename = db.Column(db.String(50), unique=True)

# Define the UserRoles data model
class UserRoles(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.id', ondelete='CASCADE'))
    role_id = db.Column(db.Integer(), db.ForeignKey('role.id', ondelete='CASCADE'))

class SensorConfig(db.Model):
    __tablename__ = "sensor_config"
    id = db.Column(db.Integer, primary_key=True)
    sensorname = db.Column(db.String(50))
    sensorid = db.Column(db.String(50),index=True)
    display_order = db.Column(db.Integer)
    tick = db.Column(db.Integer)
    highervalue = db.Column(db.Integer)

    #Temperature = relationship("Temperature", back_populates="SensorConfig")

class Temperature(APIMix, db.Model):
    __tablename__ = "temperature"
    id = db.Column(db.Integer, primary_key=True)
    thermosensor_id = db.Column(db.String(50), ForeignKey('sensor_config.sensorid'))
    #thermosensor_id = db.Column(db.String(50))
    temperature = db.Column(db.Float)
    date = db.Column(db.DateTime)
    SensorConfig = relationship("SensorConfig", cascade="save-update")
    

    def to_dict(self):
        data = {
            'id': self.id,
            'thermosensor_id': self.thermosensor_id,
            'temperature': self.temperature,
            'date': self.date
        }
        
        return data
    
    
