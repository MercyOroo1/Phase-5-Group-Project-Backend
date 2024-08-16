import uuid
from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from server.models import db, Payment, Property
from flask_jwt_extended import jwt_required, get_jwt_identity

payments_bp = Blueprint('payments', __name__, url_prefix='/payments')
payments_api = Api(payments_bp)

payment_args = reqparse.RequestParser()

payment_args.add_argument('amount', type=float, required=True, help='amount is required')
payment_args.add_argument('currency', type=str, required=True, help='currency is required')
payment_args.add_argument('payment_method', type=str, required=True, help='payment_method is required')
payment_args.add_argument('property_id', type=int, required=True, help='property_id is required')
payment_args.add_argument('user_id', type=int, required=True, help='user_id is required')


class Payments(Resource):
    
    def post(self):
    
        args = payment_args.parse_args()
        
        # Check if a payment already exists for this user and property
        existing_payment = Payment.query.filter_by(user_id = args ['user_id'],property_id=args['property_id']).first()
        if existing_payment:
            return {"message": "Payment already made for this property."}, 400
        
        # Create a new payment
        new_payment = Payment(
            user_id= args['user_id'],
            property_id=args['property_id'],
            amount=args['amount'],
            currency=args['currency'],
            payment_method=args['payment_method'],
            payment_status='completed',  # Mock payments are always completed
            transaction_id=str(uuid.uuid4())  # Generate a unique transaction ID
        )

        try:
            # Add the new payment
            db.session.add(new_payment)
            db.session.commit()

            # Update the property's listing status
            property_to_update = Property.query.filter_by(id=args['property_id']).first()
            if property_to_update:
                property_to_update.listing_status = 'sold'  # Or 'false', depending on your schema
                db.session.commit()
            else:
                # Rollback if property is not found
                db.session.rollback()
                return jsonify({"message": "Property not found."}), 404

            return {"message": "Payment created and property status updated successfully!"}, 201

        except Exception as e:
            db.session.rollback()
            return {"message": "Failed to create payment"}, 500

payments_api.add_resource(Payments, '/make-payments')
