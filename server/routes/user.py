from flask_restful import Api, Resource
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, db
from sqlalchemy.exc import SQLAlchemyError

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')
user_api = Api(user_bp)

class GetUserById(Resource):
    @jwt_required()
    def delete(self, id):
        # Get the ID of the currently logged-in user
        current_user_id = get_jwt_identity()

        # Check if the current user is trying to delete their own account
        if current_user_id != id:
            return {'message': 'Unauthorized to delete this account'}, 403

        try:
            # Fetch the user with the specified ID
            user = User.query.get_or_404(id)
            
            # Delete the user
            db.session.delete(user)
            db.session.commit()
            
            return {'message': 'User deleted'}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred', 'error': str(e)}, 500

user_api.add_resource(GetUserById, '/<int:id>/delete')
