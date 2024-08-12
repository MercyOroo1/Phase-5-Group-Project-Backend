from flask_restful import Api, Resource, reqparse
from models import User, db, AgentApplication, Agent
from flask import Blueprint
from routes.auth import allow
from flask_jwt_extended import jwt_required
from flask_mail import Message


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
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': 'An error occurred', 'error': str(e)}, 500

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
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            return {'message': 'An error occurred', 'error': str(e)}, 500

        return {'message': 'User reactivated successfully'}

admin_api.add_resource(ReactivateUserResource, "/users/<int:user_id>/reactivate")
class AgentApplicationAdminResource(Resource):
    
    def __init__(self, mail):
        self.mail = mail

    @jwt_required()
    @allow(1)
    def patch(self, application_id):
        parser = reqparse.RequestParser()
        parser.add_argument('status', required=True, help="Status cannot be blank.")
        data = parser.parse_args()

        application = AgentApplication.query.get_or_404(application_id)

        if data['status'] not in ['approved', 'rejected']:
            return {'message': 'Invalid status.'}, 400

        application.status = data['status']
        new_agent_id = None

        # If approved, create an agent record
        if data['status'] == 'approved':
            new_agent = Agent(
                user_id=application.user_id,
                license_number=application.license_number,
                full_name=application.full_name,
                email=application.email,
                experience=application.experience,
                phone_number=application.phone_number,
                languages=application.languages,
                agency_name=application.agency_name,
                photo_url=application.photo_url,

                for_sale=0,  # Initial value
                sold=0,      # Initial value
                listed_properties=0  # Initial value
            )
            new_role = User.query.get(application.user_id)
            new_role.role_id = 2
            db.session.add(new_agent)
            db.session.add(new_role)
            db.session.flush()  
            new_agent_id = new_agent.id

        try:
            db.session.commit()

            
            subject = ""
            body = ""
            if data['status'] == 'approved':
                subject = "Agent Application Approved"
                body = f"Dear {application.full_name},\n\nWe are pleased to inform you that your application to become an agent has been approved. Welcome to the team!"
            elif data['status'] == 'rejected':
                subject = "Agent Application Rejected"
                body = f"Dear {application.full_name},\n\nWe regret to inform you that your application to become an agent has been rejected. Thank you for your interest."

            msg = Message(subject,
                          sender="mercy.oroo.ke@gmail.com",
                          recipients=[application.email])
            msg.body = body
            self.mail.send(msg)

        except Exception as e:
            db.session.rollback()
            return {'message': 'An error occurred', 'error': str(e)}, 500

        return {
            'message': 'Application status updated successfully.',
            'application_status': application.status,
            'new_agent_id': new_agent_id
        }, 200


def create_resources2(mail):
 admin_api.add_resource(AgentApplicationAdminResource, "/applications/<int:application_id>", resource_class_kwargs={'mail': mail})

class GetApplicationList(Resource):
    @jwt_required()
    @allow(1)  
    def get(self):
        applications = AgentApplication.query.all()
        if not applications:
            return {'msg': 'No applications found'}, 404
        
        return {
            'applications': [{
                'id': application.id,
                'license_number': application.license_number,
                'full_name': application.full_name,
                'email': application.email,
                'experience': application.experience,
                'phone_number': application.phone_number,
                'languages': application.languages,
                'agency_name': application.agency_name,
                'status': application.status
            } for application in applications]
        }, 200

admin_api.add_resource(GetApplicationList, '/applications')

