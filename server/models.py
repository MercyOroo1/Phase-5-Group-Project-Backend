from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    role_id = db.Column(db.Integer, db.ForeignKey('roles.id'))
    role = db.relationship('Role', back_populates='users')
    
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    agents = db.relationship('Agent', back_populates='user')
    properties = db.relationship('Property', back_populates='user')
    saved_properties = db.relationship('SavedProperty', back_populates='user')
    reviews = db.relationship('Review', back_populates='user')
    contact_messages = db.relationship('ContactMessage', back_populates='user')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    users = db.relationship('User', back_populates='role')

class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    square_footage = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    property_type = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=True)
    
    photos = db.relationship('Photo', back_populates='property')
    agent = db.relationship('Agent', back_populates='properties')
    saved_by = db.relationship('SavedProperty', back_populates='property')
    contact_messages = db.relationship('ContactMessage', back_populates='property')
    reviews = db.relationship('Review', back_populates='property')

class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    photo_url = db.Column(db.String, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    property = db.relationship('Property', back_populates='photos')

class Agent(db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    license_number = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    experience = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    for_sale = db.Column(db.Integer, nullable=False)
    sold = db.Column(db.Integer, nullable=False)
    languages = db.Column(db.String, nullable=False)
    agency_name = db.Column(db.String, nullable=False)
    listed_properties = db.Column(db.Integer, nullable=False) 
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    
    user = db.relationship('User', back_populates='agents')
    properties = db.relationship('Property', back_populates='agent')

class SavedProperty(db.Model):
    __tablename__ = 'saved_properties'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    
    user = db.relationship('User', back_populates='saved_properties')
    property = db.relationship('Property', back_populates='saved_by')

class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False)
    subject = db.Column(db.String, nullable=False)
    message = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    property = db.relationship('Property', back_populates='contact_messages')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='contact_messages')

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    property = db.relationship('Property', back_populates='reviews')
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    user = db.relationship('User', back_populates='reviews')
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=True)
    agent = db.relationship('Agent', back_populates='reviews')
