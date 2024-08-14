from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from dotenv import load_dotenv
from flask_cors import CORS
from flask_bcrypt import Bcrypt

# Import blueprints
from routes.auth import auth_bp, bcrypt, create_resources
from routes.contactmessage import contact_bp
from routes.features import features_bp
from routes.profile import profile_bp
from routes.photo import photo_bp
from routes.admin import admin_bp, create_resources2

from routes.property import property_bp
from routes.agent import agent_bp
from routes.user import user_bp
from routes.savedproperties import saved_bp
from routes.review import review_bp
from routes.boostproperty import boost_bp
from routes.payments import payments_bp
from routes.purchaserequest import purchase_request_bp, create_resources3
from routes.userpayments import userpayment_bp
from routes.listingFee import listingfee_bp,create_resources4
import os
from models import db, User

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# App configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///property.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = "We are winners"
app.config['JWT_SECRET_KEY'] = 'We are winners' 
app.config['PROPAGATE_EXCEPTIONS'] = True  # Ensures exceptions are propagated (useful for debugging)

jwt = JWTManager(app)



db.init_app(app)

migrate = Migrate(app=app, db=db)

jwt = JWTManager(app)
app.config['JWT_SECRET_KEY'] = 'We are winners' 
bcrypt = Bcrypt()
bcrypt.init_app(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = ('mercy.oroo.ke@gmail.com')
app.config['MAIL_PASSWORD'] = ('jovo vvao mluj fthh')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})


@app.route('/profile', methods=['OPTIONS'])
def handle_profile_options():
    response = jsonify({'status': 'ok'})
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, DELETE, OPTIONS')
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    return response

# Register blueprints
app.register_blueprint(auth_bp)
app.register_blueprint(agent_bp)
app.register_blueprint(saved_bp)
app.register_blueprint(review_bp)
app.register_blueprint(photo_bp)
app.register_blueprint(user_bp)
app.register_blueprint(property_bp)
app.register_blueprint(contact_bp)
app.register_blueprint(admin_bp)
app.register_blueprint(profile_bp)
app.register_blueprint(features_bp)
app.register_blueprint(boost_bp)
app.register_blueprint(payments_bp)
app.register_blueprint(purchase_request_bp)
app.register_blueprint(userpayment_bp)
app.register_blueprint(listingfee_bp)
# Create resources
create_resources(mail)
create_resources2(mail)
create_resources3(mail)
create_resources4(mail)

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5050, debug=True)
