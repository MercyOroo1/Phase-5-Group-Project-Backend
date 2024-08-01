from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from models import db, ContactMessage
from flask_jwt_extended import jwt_required, current_user

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
        
        contact_message = ContactMessage(
            name=args['name'],
            email=args['email'],
            subject=args['subject'],
            message=args['message'],
            property_id=args['property_id'],
            user_id=current_user.id, 
            agent_id=args['agent_id']
        )
        
        db.session.add(contact_message)
        db.session.commit()
        
        return {'message': 'Your message has been sent!'}, 201

contact_api.add_resource(ContactMessageResource, '/messages')

