from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from models import db, ContactMessage
from flask_jwt_extended import jwt_required, get_jwt_identity
contact_bp = Blueprint('contact', __name__, url_prefix='/contact')
contact_api = Api(contact_bp)

contact_parser = reqparse.RequestParser()
contact_parser.add_argument('name', type=str, required=True, help='Name is required')
contact_parser.add_argument('email', type=str, required=True, help='Email is required')
contact_parser.add_argument('subject', type=str, required=True, help='Subject is required')
contact_parser.add_argument('message', type=str, required=True, help='Message is required')
contact_parser.add_argument('property_id', type=int, required=True, help='Property ID is required')
contact_parser.add_argument('agent_id', type=int, required=True, help='Agent ID is required')


class ContactMessageResource(Resource):
    @jwt_required() 
    def post(self):
        args = contact_parser.parse_args()
        current_user_id = get_jwt_identity()
        
        contact_message = ContactMessage(
            name=args['name'],
            email=args['email'],
            subject=args['subject'],
            message=args['message'],
            property_id=args['property_id'],
            user_id= current_user_id,
            agent_id=args['agent_id']
        )
        
        db.session.add(contact_message)
        db.session.commit()
        
        return {'message': 'Your message has been sent!'}, 201

contact_api.add_resource(ContactMessageResource, '/messages')


class AgentMessages(Resource):
    @jwt_required()
    def get(self):
        current_user_id = get_jwt_identity()
        messages = ContactMessage.query.filter_by(agent_id = current_user_id )
        if not messages:
            return {'msg': 'You have no messages'}
        return [{'id': message.id, 'name': message.name, 'email': message.email, 'subject': message.subject, 'message': message.message,'property_id': message.property_id, 'user_id': message.user_id, "user_name":message.user.full_name} for message in messages]
    
contact_api.add_resource(AgentMessages, '/agent')    