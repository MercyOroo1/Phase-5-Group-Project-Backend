from flask_restful import Api, Resource, reqparse
from flask import Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import User, db, AgentApplication, Agent
from sqlalchemy.exc import SQLAlchemyError

user_bp = Blueprint('user_bp', __name__, url_prefix='/user')
user_api = Api(user_bp)

class GetUserById(Resource):
    @jwt_required()
    def delete(self, id):
        current_user_id = get_jwt_identity()

        if current_user_id != id:
            return {'message': 'Unauthorized to delete this account'}, 403

        try:
            user = User.query.get_or_404(id)
            db.session.delete(user)
            db.session.commit()
            return {'message': 'User deleted'}
        except SQLAlchemyError as e:
            db.session.rollback()
            return {'message': 'An error occurred', 'error': str(e)}, 500

user_api.add_resource(GetUserById, '/<int:id>/delete')

class AgentApplicationResource(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        parser = reqparse.RequestParser()
        parser.add_argument('license_number', required=True, help="License number is required.")
        parser.add_argument('full_name', required=True, help="Full name is required.")
        parser.add_argument('email', required=True, help="Email is required.")
        parser.add_argument('experience', required=True, help="Experience is required.")
        parser.add_argument('phone_number', required=True, help="Phone number is required.")
        parser.add_argument('languages', required=True, help="Languages are required.")
        parser.add_argument('agency_name', required=True, help="Agency name is required.")
        data = parser.parse_args()
        
        new_application = AgentApplication(
            user_id=current_user_id,
            license_number=data['license_number'],
            full_name=data['full_name'],
            email=data['email'],
            experience=data['experience'],
            phone_number=data['phone_number'],
            languages=data['languages'],
            agency_name=data['agency_name']
        )
        db.session.add(new_application)
        db.session.commit()
        
        return {'message': 'Agent application submitted successfully.'}, 201
        
user_api.add_resource(AgentApplicationResource, '/agent-application')

class GetAgentApplicationById(Resource):
    @jwt_required()
    def get(self, application_id):
        current_user_id = get_jwt_identity()
        application = AgentApplication.query.filter_by(id=application_id, user_id=current_user_id).first()
        if not application:
            return {'message': 'Application not found or not authorized.'}, 404
        
        return {
            'id': application.id,
            'license_number': application.license_number,
            'full_name': application.full_name,
            'email': application.email,
            'experience': application.experience,
            'phone_number': application.phone_number,
            'languages': application.languages,
            'agency_name': application.agency_name,
            'status': application.status
        }, 200

user_api.add_resource(GetAgentApplicationById, '/agent-application/<int:application_id>')
