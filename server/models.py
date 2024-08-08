from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    reset_token = db.Column(db.String, nullable=True)
    token_expiry = db.Column(db.String, nullable=True)
    confirmed = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default= True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', name='fk_user_role'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=True)
    
    saved_properties = db.relationship('SavedProperty', back_populates='user')
    reviews = db.relationship('Review', back_populates='user')
    contact_messages = db.relationship('ContactMessage', back_populates='user')
    role = db.relationship('Role', back_populates='users')
    applications = db.relationship('AgentApplication', back_populates='user')
    profile = db.relationship('Profile', uselist=False, back_populates='user')
    

    def set_password(self, password):
        self.password = generate_password_hash(password)




class AgentApplication(db.Model):
    __tablename__ = 'agent_applications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique = True)
    license_number = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    experience = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    for_sale = db.Column(db.Integer, nullable=False, default=0)
    photo_url = db.Column(db.String, nullable=False)
    sold = db.Column(db.Integer, nullable=False, default=0)
    languages = db.Column(db.String, nullable=False)
    agency_name = db.Column(db.String, nullable=False)
    listed_properties = db.Column(db.Integer, nullable=False, default=0)
    status = db.Column(db.String(20), default='pending', nullable=False)  # 'pending', 'approved', 'rejected'
    
   

    # Relationship to the User model
    user = db.relationship('User', back_populates='applications')

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    
    users = db.relationship('User', back_populates='role')

class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    photo_url = db.Column(db.String, nullable=True)
    bio = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String, nullable=True)
    website = db.Column(db.String, nullable=True)

    user = db.relationship('User', back_populates='profile')
    
class Feature(db.Model):
    __tablename__ = 'features'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    properties = db.relationship('Property', back_populates='feature')

   


class Property(db.Model):
    __tablename__ = 'properties'
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String, nullable=False)
    city = db.Column(db.String, nullable=False)
    square_footage = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    property_type = db.Column(db.String(50), nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    listing_status = db.Column(db.String(20), nullable=False)
    feature_id = db.Column(db.Integer, db.ForeignKey('features.id')) 


    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id', name='fk_property_agent'), nullable=False)

    photos = db.relationship('Photo', back_populates='property')
    agent = db.relationship('Agent', back_populates='properties')
    saved_by = db.relationship('SavedProperty', back_populates='property')
    contact_messages = db.relationship('ContactMessage', back_populates='property')
    reviews = db.relationship('Review', back_populates='property')
    feature = db.relationship('Feature', back_populates='properties')

class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    photo_url = db.Column(db.String, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id', name='fk_photo_property'), nullable=False)
    
    property = db.relationship('Property', back_populates='photos')

class Agent(db.Model):
    __tablename__ = 'agents'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, nullable=False)
    license_number = db.Column(db.String, nullable=False)
    full_name = db.Column(db.String, nullable=False)
    photo_url = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    experience = db.Column(db.String, nullable=False)
    phone_number = db.Column(db.String, nullable=False)
    for_sale = db.Column(db.Integer, nullable=False)
    sold = db.Column(db.Integer, nullable=False)
    languages = db.Column(db.String, nullable=False)
    agency_name = db.Column(db.String, nullable=False)
    listed_properties = db.Column(db.Integer, nullable=False)

    properties = db.relationship('Property', back_populates='agent')
    messages = db.relationship('ContactMessage', back_populates='agent')

class SavedProperty(db.Model):
    __tablename__ = 'saved_properties'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_savedproperty_user'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id', name='fk_savedproperty_property'), nullable=False)

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

    property_id = db.Column(db.Integer, db.ForeignKey('properties.id', name='fk_contactmessage_property'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_contactmessage_user'), nullable=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id', name='fk_contactmessage_agent'), nullable=False)

    property = db.relationship('Property', back_populates='contact_messages')
    user = db.relationship('User', back_populates='contact_messages')
    agent = db.relationship('Agent', back_populates='messages')

class Review(db.Model):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    comment = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    property_id = db.Column(db.Integer, db.ForeignKey('properties.id', name='fk_review_property'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_review_user'), nullable=False)

    property = db.relationship('Property', back_populates='reviews')
    user = db.relationship('User', back_populates='reviews')
