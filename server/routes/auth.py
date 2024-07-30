from flask import Blueprint, jsonify,session
from flask_restful import Api, Resource, reqparse
from models import User, db
from flask_bcrypt import Bcrypt
from flask_jwt_extended import create_access_token, JWTManager, create_refresh_token, jwt_required, current_user
from functools import wraps



auth_bp = Blueprint('auth_bp', __name__, url_prefix='/auth')
auth_api = Api(auth_bp)
bcrypt = Bcrypt()
jwt = JWTManager()


@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).first()


register_args = reqparse.RequestParser()
register_args.add_argument('full_name',type=str, required=True, help='Full name is required')
register_args.add_argument('email',type=str, required=True, help='email name is required')
register_args.add_argument('password',type=str, required=True, help='password is required')
register_args.add_argument('password2',type=str, required=True, help='Please enter your password again')


login_args = reqparse.RequestParser()
login_args.add_argument('email')
login_args.add_argument('password')



class Register(Resource):

    def post(self):
        data = register_args.parse_args()
        # hash the password
        if data.get('password') != data.get('password2'):
            return {"msg": "Passwords do not match"}
        hashed_password = bcrypt.generate_password_hash(data.get('password'))
        new_user = User(full_name = data.get('full_name'),email = data.get('email'),password = hashed_password )
        db.session.add(new_user)
        db.session.commit()


        return {"msg": "user registration successful"}
    

class Login(Resource):
      def post(self):
        data = login_args.parse_args()

        user = User.query.filter_by(email = data.get('email')).first()

        if not user:
            return {"msg":"User does not Exist"}
        if not bcrypt.check_password_hash(user.password,data.get('password')):
            return {"msg":"Passwords Does not Exit"}

        token = create_access_token(identity=user.id)
        refresh_token = create_refresh_token(identity=user.id)

        return {"token":token,"refresh_token":refresh_token}


      @jwt_required(refresh=True)
      def get(self):
        token = create_access_token(identity= current_user.id )
        return {"token":token}
      

class Logout(Resource):
    def delete(self):
        session.pop('user_id', None)
        return {'msg': 'You have successfully logged out'},200
    
auth_api.add_resource(Register, '/register')
auth_api.add_resource(Login, '/login')
auth_api.add_resource(Logout, '/logout')
