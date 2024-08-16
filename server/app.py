from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from dotenv import load_dotenv
from flask_cors import CORS
from flask_bcrypt import Bcrypt

# Import blueprints
from server.auth import auth_bp, bcrypt, create_resources
from contactmessage import contact_bp
from features import features_bp
from profile import profile_bp
from photo import photo_bp
from admin import admin_bp, create_resources2

from property import property_bp
from agent import agent_bp
from user import user_bp
from savedproperties import saved_bp
from review import review_bp
from boostproperty import boost_bp
from payments import payments_bp
from purchaserequest import purchase_request_bp, create_resources3
from userpayments import userpayment_bp
from listingFee import listingfee_bp,create_resources4
import os
from server.models import db, User

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# App configurations
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///property.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# app.config['SECRET_KEY'] = "We are winners"
app.config['JWT_SECRET_KEY'] = 'We are winners' 
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
    app.run(host='0.0.0.0', port=5050, debug=True)
