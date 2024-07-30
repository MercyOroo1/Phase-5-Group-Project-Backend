from flask_sqlalchemy import SQLAlchemy

db=SQLAlchemy()


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    role = db.relationship('Role',backpopulates='role')

    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    agents=db.relationship('Agent', backpopulates='user')
    properties = db.relationship('Property', backref=db.backref('user'))


class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    users = db.relationship('User', back_populates='role')



class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String,nullable=False)
    city = db.Column(db.String, nullable=False)
    squareFootage = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    photos=db.relationship('Photo',backpopulates='property')
    user = db.relationship('User', backref=db.backref('properties'))
    agent = db.relationship('Agent', backref=db.backref('property'))

class Photo(db.Models):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    photo_url = db.Column(db.String, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    property = db.relationship('Property', backref=db.backref('photos'))


class Agent(db.Models):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    license_number = db.Column(db.Integer, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    experience = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    for_sale = db.Column(db.Integer, nullable=False)
    sold=db.Column(db.Integer, nullable=False)
    languages = db.Column(db.String, nullable=False)
    agency_name = db.Column(db.String, nullable=False)
    listed_proprties = db.Column(db.String, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('agents'))
    properties = db.relationship('Property', backref=db.backref('agent'))   





    

   