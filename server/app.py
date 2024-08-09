from flask import Flask
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db

from routes.auth import auth_bp, bcrypt, jwt
from routes.contactmessage import contact_bp
from routes.features import features_bp
from routes.profile import profile_bp
from routes.photo import photo_bp
from routes.admin import admin_bp, create_resources2
from routes.property import property_bp
from routes.agent import agent_bp
from routes.user import user_bp
from flask_mail import Mail
from dotenv import load_dotenv
from flask_cors import CORS
from routes.savedproperties import saved_bp
from routes.review import review_bp
from routes.boostproperty import boost_bp
from routes.auth import create_resources  

load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///property.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "We are winners"

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

migrate = Migrate(app=app, db=db)
db.init_app(app)
jwt.init_app(app)
bcrypt.init_app(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = ('mercy.oroo.ke@gmail.com')
app.config['MAIL_PASSWORD'] = ('jovo vvao mluj fthh')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)

create_resources(mail)
create_resources2(mail)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050, debug=True)
