from functools import wraps
from flask import Blueprint, jsonify, request, session
from flask_restful import Api, Resource, reqparse
from models import User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, JWTManager, create_refresh_token, jwt_required, current_user
from werkzeug.security import generate_password_hash
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadSignature
from flask_mail import Message
from datetime import datetime, timedelta

serializer = URLSafeTimedSerializer('We are winners')

auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')
auth_api = Api(auth_bp)
bcrypt = Bcrypt()
jwt = JWTManager()

@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()

register_args = reqparse.RequestParser()
register_args.add_argument('full_name', type=str, required=True, help='Full name is required')
register_args.add_argument('email', type=str, required=True, help='Email is required')
register_args.add_argument('password', type=str, required=True, help='Password is required')
register_args.add_argument('password2', type=str, required=True, help='Please enter your password again')

login_args = reqparse.RequestParser()
login_args.add_argument('email')
login_args.add_argument('password')

class ResetPasswordRequest(Resource):
    def __init__(self, mail):
        self.mail = mail
    
    def post(self):
        data = request.get_json()
        email = data.get('email')
        user = User.query.filter_by(email=email).first()
        if user and user.active:
            token = serializer.dumps(email, salt='reset-password')
            user.reset_token = token
            reset_url = f"http://localhost:5173/reset-password?token={token}"
            msg = Message("Password Reset Request",
                          sender="mercy.oroo.ke@gmail.com",
                          recipients=[email])
            msg.body = f"Use this link to reset your password: {reset_url}"
            self.mail.send(msg)

        return jsonify({'message': 'If the email exists and the account is active, a reset link has been sent.'})

class ResetPassword(Resource):
    def post(self):
        data = request.get_json()
        token = data.get('token')
        new_password = data.get('password')
        
        try:
            email = serializer.loads(token, salt='reset-password', max_age=3600)
        except SignatureExpired:
            return jsonify({'message': 'The reset link is invalid or expired.'}), 400

        user = User.query.filter_by(email=email).first()
        if user and user.active:
            user.password = bcrypt.generate_password_hash(new_password)
            db.session.commit()
            return jsonify({'message': 'Password has been reset.'})
        return jsonify({'message': 'User not found or account is not active.'}), 404

class Register(Resource):

    def __init__(self, mail):
        self.mail = mail

    def post(self):
        data = register_args.parse_args()
        # Hash the password
        if data.get('password') != data.get('password2'):
            return {"msg": "Passwords do not match"}
        
        hashed_password = bcrypt.generate_password_hash(data.get('password')).decode('utf-8')
        new_user = User(full_name=data.get('full_name'), email=data.get('email'), password=hashed_password, confirmed=False, active=True)
        db.session.add(new_user)
        db.session.commit()
        
        # Generate confirmation token
        token = serializer.dumps(data.get('email'), salt='email-confirm')
        confirm_url = f"http://localhost:5173/confirm-email?token={token}"
        msg = Message("Email Confirmation", sender="mercy.oroo.ke@gmail.com", recipients=[data.get('email')])
        msg.body = f"Please confirm your email by clicking on the following link: {confirm_url}"
        self.mail.send(msg)
        
        return {"msg": "User registration successful. A confirmation email has been sent."}, 201

class ConfirmEmail(Resource):
    def get(self):
        token = request.args.get('token')
        if not token:
            return {"msg": "No confirmation token provided."}, 400
        
        try:
            email = serializer.loads(token, salt='email-confirm', max_age=3600)
        except SignatureExpired:
            return {"msg": "The confirmation link has expired."}, 400
        except BadSignature:
            return {"msg": "Invalid confirmation token."}, 400
        
        # Find the user by email and confirm their email
        user = User.query.filter_by(email=email).first_or_404()
        if user.confirmed:
            return {"msg": "Account already confirmed."}, 200
        
        user.confirmed = True
        db.session.commit()
        return {"msg": "Your email has been confirmed. Thank you!"}, 200

class Login(Resource):
    def post(self):
        data = login_args.parse_args()
        user = User.query.filter_by(email=data.get('email')).first()

        if not user:
            return {"msg": "User does not exist"}
        if not bcrypt.check_password_hash(user.password, data.get('password')):
            return {"msg": "Password does not match"}
        if not user.active:
            return {"msg": "Your account is deactivated. Please contact support."}

        token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)
        return {"token": token, "refresh_token": refresh_token, 'role_id': user.role_id}

    @jwt_required(refresh=True)
    def get(self):
        token = create_access_token(identity=current_user.id)
        return {"token": token}
      
class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {'msg': 'You have successfully logged out'}, 200




def allow(*allowed_roles):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            user = current_user
            # Fetch the role associated with the user's role_id
            user_role = user.role_id
            
            # Check if the user's role_id is in the allowed_roles
            if user_role in allowed_roles:
                return fn(*args, **kwargs)
            
            # If the role is not allowed, deny access
            return {"msg": "Access Denied"}, 403
        
        return wrapper
    return decorator
# Register resources
def create_resources(mail):
    
    auth_api.add_resource(Register, '/register', resource_class_kwargs={'mail': mail})
    auth_api.add_resource(Login, '/login')
    auth_api.add_resource(Logout, '/logout')
    auth_api.add_resource(ResetPasswordRequest, '/reset-password-request', resource_class_kwargs={'mail': mail})
    auth_api.add_resource(ResetPassword, '/reset-password')
    auth_api.add_resource(ConfirmEmail, '/confirm-email')
