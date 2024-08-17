from flask_restful import Api, Resource, reqparse
from server.models import db, PurchaseRequest
from flask import Blueprint
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_mail import Message
from datetime import datetime

# Create a Blueprint
purchase_request_bp = Blueprint('purchase_request_bp', __name__, url_prefix='/purchase_request')
purchase_request_api = Api(purchase_request_bp)
CORS(purchase_request_bp)  # Enable CORS for the Blueprint

# Define request parser
purchase_request_args = reqparse.RequestParser()
purchase_request_args.add_argument('property_id', type=int, required=True, help='Property id is required')
purchase_request_args.add_argument('status', type=str, required=True, help='Status is required')

# Resource for handling purchase requests
class PurchaseRequestResource(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        args = purchase_request_args.parse_args()
        
        # Validate status field (optional)
        valid_statuses = ['Pending', 'Approved', 'Rejected']
        if args['status'] not in valid_statuses:
            return {'message': 'Invalid status value'}, 400

        purchase_request = PurchaseRequest(
            user_id=current_user_id,
            property_id=args['property_id'],
            status=args['status'],
        )
        
        try:
            db.session.add(purchase_request)
            db.session.commit()
            return {'message': 'Purchase request added successfully', 'purchase_request_id': purchase_request.id}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': 'An error occurred while processing your request', 'error': str(e)}, 500

purchase_request_api.add_resource(PurchaseRequestResource, '/list')

# Resource for approving/rejecting purchase requests
from flask import request
from flask_mail import Message
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
from server.models import PurchaseRequest, db

class ApprovePurchaseRequestResource(Resource):
    def __init__(self, mail):
        self.mail = mail

    # @jwt_required()
    def patch(self, request_id):
        # current_user = get_jwt_identity()

        # Uncomment and use if role-based access is required
        # if current_user['role_id'] != 2:  # Assuming role_id 2 is for agents
        #     return {'message': 'Access Denied'}, 403

        purchase_request = PurchaseRequest.query.get_or_404(request_id)

        # Generate the payment link with query parameters
        if purchase_request.status == 'Pending':
            purchase_request.status = 'Approved'
            payment_url = (f"https://phase-5-group-project-backend-24.onrender.com/payment?propertyId={purchase_request.property_id}"
                           f"&userId={purchase_request.user_id}")
            subject = "Property Purchase Approved"
            body = (f"Dear User,\n\n"
                    f"Your request to purchase property {purchase_request.property_id} has been approved. "
                    f"Please complete your payment by clicking the link: {payment_url}\n\n"
                    f"Best regards,\nProperty Management Team")
        else:
            purchase_request.status = 'Rejected'
            subject = "Property Purchase Request Rejected"
            body = (f"Dear User,\n\n"
                    f"We regret to inform you that your request to purchase property {purchase_request.property_id} "
                    f"has been rejected. Please contact support for more details.\n\n"
                    f"Best regards,\nProperty Management Team")

        purchase_request.updated_at = datetime.utcnow()
        db.session.commit()

        # Ensure email address exists
        if not purchase_request.user.email:
            return {'message': 'User email not found.'}, 400

        # Send email to the user with the appropriate message
        try:
            msg = Message(subject,
                          sender="mercy.oroo.ke@gmail.com",
                          recipients=[purchase_request.user.email])
            msg.body = body
            self.mail.send(msg)
        except Exception as e:
            db.session.rollback()  # Rollback the transaction on failure
            return {'message': f'Failed to send email: {str(e)}'}, 500

        return {'message': f'The purchase request has been {purchase_request.status.lower()} and an email has been sent to the user.'}, 200

def create_resources3(mail):
    purchase_request_api.add_resource(ApprovePurchaseRequestResource, '/agent/<int:request_id>/approve', resource_class_kwargs={'mail': mail})

class GetAgentPurchaseRequests(Resource):
    @jwt_required()
    def get(self, property_id):
        current_user = get_jwt_identity()
        
        
     

        # Query for purchase requests related to the given property_id
        purchase_requests = PurchaseRequest.query.filter_by(property_id=property_id).all()

        # If there are no purchase requests, return a message
        if not purchase_requests:
            return {'msg': 'This property has no purchase requests'}, 404
        
        # Return a list of purchase requests
        return {
            'purchase_requests': [
                {
                    'id': request.id,
                    'user_id': request.user_id,
                    'property_id': request.property_id,
                    'status': request.status
                }
                for request in purchase_requests
            ]
        }, 200

# Update the route parameter to match `property_id`
purchase_request_api.add_resource(GetAgentPurchaseRequests, '/agent/list/<int:property_id>')
