from flask import Blueprint, request
from flask_restful import Api, Resource
from flask_cors import CORS
from models import UserPayment, Property, db
import stripe
import os
from flask_jwt_extended import jwt_required
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize Stripe API key
stripe.api_key = os.getenv('STRIPE_API_KEY')

# Set up Flask Blueprint and API
userpayment_bp = Blueprint('userpayment', __name__, url_prefix='/userpayment')
userpayment_api = Api(userpayment_bp)
CORS(userpayment_bp)

class CreatePaymentIntent(Resource):
    def post(self):
        data = request.get_json()
        amount = data.get('amount')
        property_id = data.get('property_id')
        user_id = data.get('user_id')

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

userpayment_api.add_resource(CreatePaymentIntent, '/create-intent')

class ConfirmPayment(Resource):
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        amount = data.get('amount')
        property_id = data.get('property_id')
        payment_intent_id = data.get('payment_intent_id')

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
                    transaction_id=payment_intent.id
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



class GetAgentPayments(Resource):
    def get(self,property_id):
     payments = UserPayment.query.filter_by(property_id = property_id)
     if not payments:
       return {'message': 'Property does not have any payments'}
     return {
         
            'payments': [
                {
                    'id': payment.id,
                    'user_id': payment.user_id,
                    'property_id': payment.property_id,
                    'status': payment.payment_status,
                    'payment_method': payment.payment_method
                }
                for payment in payments
            ]
        }, 200
    
         
     
    
userpayment_api.add_resource(GetAgentPayments, '/agent/list/<int:property_id>')
