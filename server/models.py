from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime


db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String, nullable=False)
    email = db.Column(db.String, nullable=False, unique=True)
    password = db.Column(db.String, nullable=False)
    reset_token = db.Column(db.String, nullable=True)
    token_expiry = db.Column(db.DateTime, nullable=True)
    confirmed = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    role_id = db.Column(db.Integer, db.ForeignKey('roles.id', name='fk_user_role'))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)
    updated_at = db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp(), nullable=True)

    saved_properties = db.relationship('SavedProperty', back_populates='user', cascade='all, delete-orphan')
    reviews = db.relationship('Review', back_populates='user', cascade='all, delete-orphan')
    contact_messages = db.relationship('ContactMessage', back_populates='user', cascade='all, delete-orphan')
    role = db.relationship('Role', back_populates='users')
    applications = db.relationship('AgentApplication', back_populates='user', cascade='all, delete-orphan')
    profile = db.relationship('Profile', uselist=False, back_populates='user', cascade='all, delete-orphan')
    # payments = db.relationship('Payment', back_populates='user', cascade='all, delete-orphan')
    purchase_requests = db.relationship('PurchaseRequest', back_populates='user', cascade='all, delete-orphan')
    userpayments = db.relationship('UserPayment', back_populates = 'users', cascade = 'all, delete-orphan')
    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

# class Features(db.Model):
#     __tablename__ = 'features'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#     description = db.Column(db.String, nullable=False)

#     property = db.relationship('Property', back_populates='features')
#     property_id = db.Column(db.Integer, db.ForeignKey('properties.id'))

class Role(db.Model):
    __tablename__ = 'roles'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False, unique=True)
    
    users = db.relationship('User', back_populates='role')


class ListingFee(db.Model):
    __tablename__ = 'listing_fees'
    
    id = db.Column(db.Integer, primary_key=True)
    fee_amount = db.Column(db.Float, nullable=False)  
    fee_type = db.Column(db.String(50), nullable=False)  #  'property_listing'
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    
    
    
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'))

    start_date = db.Column(db.DateTime, nullable=False) # Subscription start date
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)    # Indicates if the subscription is currently active
    payment_frequency = db.Column(db.String(20), nullable=False, default='monthly')  
     # Payment frequency
    subscription_status = db.Column(db.String(20), default='active', nullable=False)  # 'active', 'cancelled', 'expired'
    payments = db.relationship('Payment', back_populates='listing_fee')


   
    
    
    agent=db.relationship('Agent', back_populates='listing_fees')

    
    
    
   




class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    photo_url = db.Column(db.String, nullable=True)
    bio = db.Column(db.String, nullable=True)
    phone_number = db.Column(db.String, nullable=True)
    website = db.Column(db.String, nullable=True)

    user = db.relationship('User', back_populates='profile')

class AgentApplication(db.Model):
    __tablename__ = 'agent_applications'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
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



    
    
   


    user = db.relationship('User', back_populates='applications')










    
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

    properties = db.relationship('Property', back_populates='agent', cascade='all, delete-orphan')
    messages = db.relationship('ContactMessage', back_populates='agent', cascade='all, delete-orphan')
    listing_fees = db.relationship('ListingFee', back_populates='agent', cascade='all, delete-orphan')
    payments = db.relationship('Payment', back_populates = 'agent', cascade = 'all, delete-orphan')

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
    boosted = db.Column(db.Boolean, default=False)
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id', name='fk_property_agent'), nullable=False)

    photos = db.relationship('Photo', back_populates='property', cascade='all, delete-orphan')
    agent = db.relationship('Agent', back_populates='properties')
    saved_by = db.relationship('SavedProperty', back_populates='property')
    contact_messages = db.relationship('ContactMessage', back_populates='property', cascade = 'all, delete-orphan')
    

    
    feature = db.relationship('Feature', back_populates='properties', cascade = 'all, delete-orphan')


    # payments = db.relationship('Payment', back_populates='property')
    purchase_requests = db.relationship('PurchaseRequest', back_populates='property', cascade = 'all, delete-orphan')
    userpayment = db.relationship('UserPayment', back_populates = 'property', cascade = 'all, delete-orphan')



    


class BoostedProperty(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    boosted_at = db.Column(db.DateTime, default=datetime.utcnow)

class Photo(db.Model):
    __tablename__ = 'photos'
    id = db.Column(db.Integer, primary_key=True)
    photo_url = db.Column(db.String, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id', name='fk_photo_property'), nullable=False)
    
    property = db.relationship('Property', back_populates='photos')




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
    
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_review_user'), nullable=False)

    
    user = db.relationship('User', back_populates='reviews')

class Feature(db.Model):
    __tablename__ = 'features'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    description = db.Column(db.String, nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)

    properties = db.relationship('Property', back_populates='feature')


   

class Payment(db.Model):
    __tablename__ = 'payments'



    id = db.Column(db.Integer, primary_key=True)
   
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), nullable=False)
    payment_method = db.Column(db.String(50), nullable=False)
    payment_status = db.Column(db.String(20), nullable=False)
    transaction_id = db.Column(db.String, unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp(), nullable=True)
    # property = db.relationship('Property', back_populates='payments', uselist=False)
    listing_fee_id = db.Column(db.Integer, db.ForeignKey('listing_fees.id'), nullable=False)
    listing_fee = db.relationship('ListingFee', back_populates='payments')
    agent_id = db.Column(db.Integer, db.ForeignKey('agents.id'), nullable=False) 
    

    agent = db.relationship('Agent', back_populates='payments')

class PurchaseRequest(db.Model):
    __tablename__ = 'purchase_requests'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    request_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    status = db.Column(db.String(20), default='pending')  

    user = db.relationship('User', back_populates='purchase_requests')
    property = db.relationship('Property', back_populates='purchase_requests')


class UserPayment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', name='fk_payment_user'), nullable=False)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id', name='fk_payment_property'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    currency = db.Column(db.String(3), default='usd')
    payment_method = db.Column(db.String(50))
    payment_status = db.Column(db.String(20), default='pending')
    transaction_id = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    installment_amount = db.Column(db.Float, nullable=True)
    total_installments =  db.Column(db.Integer, nullable=True)
    property = db.relationship('Property', back_populates = 'userpayment')
    users = db.relationship('User', back_populates = 'userpayments')

    def __repr__(self):
        return f'<UserPayment {self.id}>'

