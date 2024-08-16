from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from models import UserPayment, Property, db
import stripe
import os
from flask_jwt_extended import jwt_required, get_jwt_identity
from dotenv import load_dotenv
from datetime import datetime, timedelta


# Load environment variables from .env files
load_dotenv()

stripe.api_key = os.getenv('STRIPE_TEST_SECRET_KEY')

if not stripe.api_key:
    raise ValueError("Stripe API key is not set in environment variables.")


userpayment_bp = Blueprint('userpayment', __name__, url_prefix='/userpayment')
userpayment_api = Api(userpayment_bp)
CORS(userpayment_bp)


stripe.api_key = os.getenv('STRIPE_API_KEY')

payment_parser = reqparse.RequestParser()
payment_parser.add_argument('amount', type=float, required=True, help='Amount cannot be blank')
payment_parser.add_argument('property_id', type=int, required=True, help='Property ID cannot be blank')
payment_parser.add_argument('user_id', type=int, required=True, help='User ID cannot be blank')
payment_parser.add_argument('installment_amount', type=float, required=True, help='installment cannot be blank')





import logging

logging.basicConfig(level=logging.INFO)
class CreatePaymentIntent(Resource):
    def post(self):
        data = request.get_json()
        amount = data.get('amount')
        property_id = data.get('property_id')
        user_id = data.get('user_id')
        installment_amount = data.get('installment_amount')
        total_installments = data.get('total_installments', 1)

        if not amount or not property_id or not user_id:
            return {'message': 'Amount, property ID, and user ID are required'}, 400

        property_to_update = Property.query.filter_by(id=property_id).first()
        if not property_to_update:
            return {'message': 'Property not found'}, 404

        if amount <= 0 or (installment_amount and installment_amount <= 0):
            return {'message': 'Invalid amount or installment amount'}, 400

        if amount > property_to_update.price:
            return {'message': 'Amount exceeds property price'}, 400

        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=int(installment_amount * 100),  # Convert amount to cents
                currency='usd',
                description='User payment',
                metadata={
                    'user_id': user_id,
                    'installment_amount': installment_amount,
                    'total_installments': total_installments
                }
            )
            return {
                'client_secret': payment_intent.client_secret,
                'payment_intent_id': payment_intent.id
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
        installment_amount = data.get('installment_amount')
        total_installments = data.get('total_installments')

        if not user_id or not amount or not property_id or not payment_intent_id:
            return {'message': 'User ID, amount, property ID, and payment intent ID are required'}, 400

        if amount <= 0 or (installment_amount and installment_amount <= 0):
            return {'message': 'Invalid amount or installment amount'}, 400

        property_to_update = Property.query.filter_by(id=property_id).first()
        if not property_to_update:
            return {'message': 'Property not found'}, 404

        if property_to_update.listing_status == 'sold':
            return {'message': 'This property is already sold. No further payments can be made.'}, 400

        if amount > property_to_update.price:
            return {'message': 'Amount exceeds property price'}, 400

        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            if payment_intent.status == 'succeeded':
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

                # Update the property's listing status if it's the final installment
                if amount >= property_to_update.price:
                    property_to_update.listing_status = 'sold'
                    db.session.commit()

                return {'message': 'Payment succeeded and property status updated successfully'}, 200
            else:
                return {'message': 'Payment failed. Please try again.'}, 400
        except stripe.error.InvalidRequestError as e:
            return {'message': f"Stripe error: {e.user_message or str(e)}"}, 400
        except stripe.error.StripeError as e:
            return {'message': f"Stripe error: {e.user_message or str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            return {'message': f"An error occurred: {str(e)}"}, 500


userpayment_api.add_resource(ConfirmPayment, '/confirm-payment')
userpayment_api.add_resource(CreatePaymentIntent, '/create-intent')



class FullPayment(Resource):
    def post(self):
        data = request.get_json()
        user_id = data.get('user_id')
        property_id = data.get('property_id')
        payment_intent_id = data.get('payment_intent_id')

        if not user_id or not property_id or not payment_intent_id:
            return {'message': 'User ID, property ID, and payment intent ID are required'}, 400

        property_to_update = Property.query.filter_by(id=property_id).first()
        if not property_to_update:
            return {'message': 'Property not found'}, 404

        if property_to_update.listing_status == 'sold':
            return {'message': 'This property is already sold. No further payments can be made.'}, 400

        try:
            payment_intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            if payment_intent.status == 'succeeded':
                payment = UserPayment(
                    user_id=user_id,
                    amount=property_to_update.price,
                    property_id=property_id,
                    payment_method='stripe',
                    payment_status='successful',
                    transaction_id=payment_intent.id,
                    installment_amount=None,
                    total_installments=1
                )
                db.session.add(payment)
                db.session.commit()

                property_to_update.listing_status = 'sold'
                db.session.commit()

                return {'message': 'Full payment succeeded and property status updated successfully'}, 200
            else:
                return {'message': 'Payment failed. Please try again.'}, 400
        except stripe.error.StripeError as e:
            return {'message': f"Stripe error: {e.user_message or str(e)}"}, 400
        except Exception as e:
            db.session.rollback()
            return {'message': f"An error occurred: {str(e)}"}, 500


userpayment_api.add_resource(FullPayment, '/full-payment')
class PropertyDetails(Resource):
    def get(self, property_id):
        property_ = Property.query.filter_by(id=property_id).first()
        if not property_:
            return {'message': 'Property not found'}, 404

        return {
            'price': property_.price,
            'listing_status': property_.listing_status
        }, 200

userpayment_api.add_resource(PropertyDetails, '/property-details/<int:property_id>')

class Installments(Resource):
    def get(self, property_id):
        property_ = Property.query.filter_by(id=property_id).first()
        if not property_:
            return {'message': 'Property not found'}, 404

        installments = []
        total_installments = property_.price / property_.installment_amount
        for i in range(int(total_installments)):
            installment = {
                'amount': property_.installment_amount,
                'remaining_amount': property_.price - (i * property_.installment_amount),
                'due_date': (datetime.now() + timedelta(days=30 * (i+1))).strftime('%Y-%m-%d')
            }
            installments.append(installment)

        return {
            'installments': installments
        }, 200


userpayment_api.add_resource(Installments, '/installments/<int:property_id>')


class AgentUserPayments(Resource):
  @jwt_required()
  def get(self, property_id):
        agent_id = get_jwt_identity()

        properties = Property.query.filter_by(agent_id=agent_id).all()
        if not properties:
            return {'message': 'No properties found for the agent'}, 404
        # Retrieve the property from the database
      
        property_ids = [property_.id for property_ in properties]
        payments = UserPayment.query.filter(UserPayment.property_id.in_(property_ids)).first()
        # Retrieve all user payments for the specified property
       

        # Prepare the response data
        payment_list = []
        for payment in payments:
            payment_list.append({
                'id': payment.id,
                'amount': payment.amount,
                'property': payment.property_id,
                'installment_amount': payment.installment_amount,
                'total_installments':payment.total_installments,
                'payment_status': payment.payment_status,
                # 'payment_date': payment.payment_date.strftime('%Y-%m-%d'),
                'user_id': payment.user_id,
                'full_name': payment.users.full_name


            })

        return {
            'payments': payment_list
        }, 200
class AgentUserPayments(Resource):
    def get(self, property_id):
        # Retrieve the property from the database
        property_ = Property.query.filter_by(id=property_id).first()
        if not property_:
            return {'message': 'Property not found'}, 404

        # Retrieve all user payments for the specified property
        payments = UserPayment.query.filter_by(property_id=property_id).all()

        # Prepare the response data
        payment_list = []
        for payment in payments:
            payment_list.append({
                'id': payment.id,
                'amount': payment.amount,
                'property': payment.property_id,
                'installment_amount': payment.installment_amount,
                'total_installments': payment.total_installments,
                'payment_status': payment.payment_status,
                'full_name':payment.users.full_name,
                'user_id': payment.user_id,
            })

        return {'payments': payment_list}, 200

userpayment_api.add_resource(AgentUserPayments, '/agent/<int:property_id>')