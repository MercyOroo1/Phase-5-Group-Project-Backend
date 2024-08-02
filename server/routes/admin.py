from flask_restful import Api,Resource,reqparse
from models import User, db
from flask import Blueprint
from routes.auth import allow
from flask_jwt_extended import jwt_required


admin_bp = Blueprint('admin_bp', __name__, url_prefix='/admin')
admin_api = Api(admin_bp)


class UserListResource(Resource):
    @jwt_required()
    @allow(1)
    def get(self):
        users = User.query.all()
        return [{
            'id': user.id,
            'FullName': user.full_name,
            'Email': user.email,
            'created_at': user.created_at.isoformat() if user.created_at else None,
            'updated_at': user.updated_at.isoformat() if user.updated_at else None,
            'active': user.active,
            'confirmed': user.confirmed,
            'role_id': user.role_id,
            'role': user.role.name if user.role else None
        } for user in users]

admin_api.add_resource(UserListResource, "/users")


class DeactivateUserResource(Resource):
    @jwt_required()
    @allow(1)
    def post(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        
        user.active = False
        db.session.commit()
        
        return {'message': 'User deactivated successfully'}

admin_api.add_resource(DeactivateUserResource, "/users/<int:user_id>/deactivate")

     
class ReactivateUserResource(Resource):
    @jwt_required()
    @allow(1)
    def post(self, user_id):
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404
        
        
        user.active = True
        db.session.commit()
        
        return {'message': 'User reactivated successfully'}

admin_api.add_resource(ReactivateUserResource, "/users/<int:user_id>/reactivate")