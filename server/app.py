from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from models import db
from routes.auth import auth_bp,bcrypt, jwt,create_resources
from flask_mail import Mail
from dotenv import load_dotenv
from flask_cors import CORS
load_dotenv()

app = Flask(__name__)
CORS(app)

app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///property.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = "We are winners"

app.register_blueprint(auth_bp)
bcrypt.init_app(app)
jwt.init_app(app)

migrate = Migrate(app = app, db= db)
db.init_app(app)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = ('mercy.oroo.ke@gmail.com')
app.config['MAIL_PASSWORD'] = ('jovo vvao mluj fthh')
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False

mail = Mail(app)




create_resources(mail)
# @app.route('/send-test-email')
# def send_test_email():
#     try:
#         msg = Message('Test Email',
#                       sender=('mercy.oroo.ke@gmail.com'),
#                       recipients=['oroomercy@gmail.com'])
#         msg.body = 'This is a test email sent from Flask app using Gmail.'
#         mail.send(msg)
#         return 'Test email sent!'
#     except Exception as e:
#         # You might want to log the error instead of returning it in production
#         return f'An error occurred: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
