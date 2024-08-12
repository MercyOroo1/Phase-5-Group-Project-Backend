from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from models import UserPayment, Property, db
import stripe
import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Stripe API key
stripe.api_key = os.getenv('STRIPE_API_KEY')

# Set up Flask Blueprint and API
userpayment_bp = Blueprint('userpayment', __name__, url_prefix='/userpayment')
userpayment_api = Api(userpayment_bp)
CORS(userpayment_bp)

# Define request parser
payment_parser = reqparse.RequestParser()
payment_parser.add_argument('amount', type=float, required=True, help='Amount cannot be blank')
payment_parser.add_argument('property_id', type=int, required=True, help='Property ID cannot be blank')
payment_parser.add_argument('user_id', type=int, required=True, help='User ID cannot be blank')


# class UserPaymentResource(Resource):
#     # @jwt_required()
#     def post(self):
#         args = payment_parser.parse_args()
#         user_id = args['user_id']  # Use get_jwt_identity() if JWT is required
#         amount = args['amount']
#         property_id = args['property_id']

#         if amount <= 0:
#             return {'message': 'Invalid amount'}, 400

#         # Fetch the property and validate the amount
#         property_to_update = Property.query.filter_by(id=property_id).first()
#         if not property_to_update:
#             return {'message': 'Property not found'}, 404
        
#         if property_to_update.listing_status == 'sold':
#             return {'message': 'This property is already sold. No further payments can be made.'}, 400
        
#         if amount != property_to_update.price:
#             return {'message': f'Amount does not match property price. The correct price is {property_to_update.price}'}, 400

#         try:
#             # Create PaymentIntent with Stripe
#             payment_intent = stripe.PaymentIntent.create(
#                 amount=int(amount * 100),  # Convert amount to cents
#                 currency='usd',
#                 description='User payment',
#                 metadata={'user_id': user_id}
#             )

#             # Save payment to the database
#             payment = UserPayment(
#                 user_id=user_id,
#                 amount=amount,
#                 property_id=property_id,
#                 payment_method='stripe',
#                 payment_status='successful',
#                 transaction_id=payment_intent.id
#             )
#             db.session.add(payment)
#             db.session.commit()

#             # Update the property's listing status
#             property_to_update.listing_status = 'sold' 
#             db.session.commit()

#             return {
#                 'client_secret': payment_intent.client_secret,
#                 'message': 'Payment intent created and property status updated successfully'
#             }, 200

#         except stripe.error.StripeError as e:
#             return {'message': f"Payment failed: {e.user_message or str(e)}"}, 400
#         except Exception as e:
#             db.session.rollback()
#             return {'message': f"An error occurred: {str(e)}"}, 500

#     def get(self, id):
#         payment = UserPayment.query.get_or_404(id)
#         return {
#             'user_id': payment.user_id,
#             'amount': payment.amount,
#             'property_id': payment.property_id,
#             'currency': payment.currency,
#             'payment_method': payment.payment_method,
#             'payment_status': payment.payment_status,
#             'transaction_id': payment.transaction_id,
#             'created_at': payment.created_at.strftime("%Y-%m-%dT%H:%M:%S")
#         }

# # Add resource routes to the API
# userpayment_api.add_resource(UserPaymentResource, '/')

class CreatePaymentIntent(Resource):
    def post(self):
        data = request.get_json()
        amount = data.get('amount')
        property_id = data.get('property_id')
        user_id = data.get('user_id')
        total_installments = data.get('total_installments', 3)  # Default to 3 installment 

        if not amount or not property_id or not user_id:
            return {'message': 'Amount, property ID, and user ID are required'}, 400

        # Fetch the property and validate the amount
        property_to_update = Property.query.filter_by(id=property_id).first()
        if not property_to_update:
            return {'message': 'Property not found'}, 404

        if amount <= 0:
            return {'message': 'Invalid amount'}, 400

        if amount != property_to_update.price:
            return {'message': f'Amount does not match property price. The correct price is {property_to_update.price}'}, 400

        try:
            # Create PaymentIntent with Stripe
            payment_intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert amount to cents
                currency='usd',
                description='User payment',
                metadata={'user_id': user_id}
            )

            return {
                'client_secret': payment_intent.client_secret
            }, 200

        except stripe.error.StripeError as e:
            return {'message': f"Stripe error: {e.user_message or str(e)}"}, 400
        except Exception as e:
            return {'message': f"An error occurred: {str(e)}"}, 500


class ConfirmPayment(Resource):
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        amount = data.get('amount')
        property_id = data.get('property_id')
        payment_intent_id = data.get('payment_intent_id')
        total_installments = data.get('total_installments', 1)
        installment_amount = data.get('installment_amount', amount / total_installments)

        if not user_id or not amount or not property_id or not payment_intent_id:
            return {'message': 'User ID, amount, property ID, and payment intent ID are required'}, 400

        if amount <= 0:
            return {'message': 'Invalid amount'}, 400

        # Fetch the property and validate the amount
        property_to_update = Property.query.filter_by(id=property_id).first()
        if not property_to_update:
            return {'message': 'Property not found'}, 404

        if property_to_update.listing_status == 'sold':
            return {'message': 'This property is already sold. No further payments can be made.'}, 400

        if amount != property_to_update.price:
            return {'message': f'Amount does not match property price. The correct price is {property_to_update.price}'}, 400

        try:
            # Retrieve the PaymentIntent from Stripe
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)

            # Check the payment status
            if payment_intent.status == 'succeeded':
                # Save payment to the database
                payment = UserPayment(
                    user_id=user_id,
                    amount=amount,
                    property_id=property_id,
                    payment_method='stripe',
                    payment_status='successful',
                    transaction_id=payment_intent.id,
                    installment_amount=installment_amount,
                    total_installments=total_installments
                )
                db.session.add(payment)
                db.session.commit()

                # Update the property's listing status
                property_to_update.listing_status = 'sold'
                db.session.commit()

                return {'message': 'Payment succeeded and property status updated successfully'}, 200
            else:
                return {'message': 'Payment failed. Please try again.'}, 400
        except stripe.error.StripeError as e:
            return {'message': f"Stripe error: {e.user_message or str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            return {'message': f"An error occurred: {str(e)}"}, 500

        
userpayment_api.add_resource(ConfirmPayment, '/confirm-payment')