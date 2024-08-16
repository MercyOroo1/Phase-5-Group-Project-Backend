from werkzeug.security import generate_password_hash
from app import  app  # Import your Flask app and db
from models import db, User, Role, Agent, Property, ListingFee, AgentApplication, Profile, SavedProperty, ContactMessage, Review, Feature, Payment, PurchaseRequest, UserPayment
import datetime

def seed_roles():
    roles = ['Admin', 'Agent', 'Buyer']
    for role_name in roles:
        role = Role(name=role_name)
        db.session.add(role)
    db.session.commit()

def seed_users():
    admin_role = Role.query.filter_by(name='Admin').first()
    agent_role = Role.query.filter_by(name='Agent').first()
    
    buyer_role = Role.query.filter_by(name='Buyer').first()

    users = [
        User(full_name='Admin User', email='admin@example.com', password=generate_password_hash('password'), role=admin_role),
        User(full_name='Agent User', email='agent@example.com', password=generate_password_hash('password'), role=agent_role),
        User(full_name='Buyer User', email='buyer@example.com', password=generate_password_hash('password'), role=buyer_role)
    ]
    
    for user in users:
        db.session.add(user)
    db.session.commit()

def seed_agents():
    agent = Agent(
        user_id=User.query.filter_by(email='agent@example.com').first().id,
        license_number='ABC123',
        full_name='Agent User',
        photo_url='https://example.com/photo.jpg',
        email='agent@example.com',
        experience='5 years',
        phone_number='123-456-7890',
        for_sale=5,
        sold=10,
        languages='English',
        agency_name='Best Realty',
        listed_properties=15
    )
    db.session.add(agent)
    db.session.commit()

def seed_properties():
    agent = Agent.query.first()
    properties = [
        Property(
            address='123 Main St',
            city='Hometown',
            square_footage=1200,
            price=250000,
            property_type='House',
            listing_status='For Sale',
            agent=agent
        ),
        Property(
            address='456 Oak St',
            city='Hometown',
            square_footage=1500,
            price=350000,
            property_type='House',
            listing_status='For Sale',
            agent=agent
        )
    ]
    for property in properties:
        db.session.add(property)
    db.session.commit()

def seed_listing_fees():
    agent = Agent.query.first()
    fee = ListingFee(
        fee_amount=100.00,
        fee_type='property_listing',
        agent_id=agent.id,
        start_date=datetime.datetime(2023, 1, 1),
        end_date=datetime.datetime(2023, 12, 31),
        payment_frequency='monthly',
        subscription_status='active'
    )
    db.session.add(fee)
    db.session.commit()

def seed_reviews():
    user = User.query.filter_by(email='buyer@example.com').first()
    review = Review(
        rating=5,
        comment='Great property!',
        user=user
    )
    db.session.add(review)
    db.session.commit()

def seed_all():
    with app.app_context():
        seed_roles()
        seed_users()
        seed_agents()
        seed_properties()
        seed_listing_fees()
        seed_reviews()

if __name__ == '__main__':
    seed_all()
    print("Seeding completed!")
