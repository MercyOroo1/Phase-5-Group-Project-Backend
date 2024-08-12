from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from models import ListingFee, db, Payment
from datetime import datetime
import os
import stripe

listingfee_bp = Blueprint('listingfee', __name__, url_prefix='/listingfee')
listingfee_api = Api(listingfee_bp)
CORS(listingfee_bp)


stripe.api_key = os.getenv('STRIPE_API_KEY')


listingfee_parser = reqparse.RequestParser()
listingfee_parser.add_argument('fee_amount', type=float, required=True, help='Amount cannot be blank')
listingfee_parser.add_argument('fee_type', type=str, required=True, help='Fee type cannot be blank')
listingfee_parser.add_argument('start_date', type=str, required=True, help='Start date cannot be blank')
listingfee_parser.add_argument('end_date', type=str, required=True, help='End date cannot be blank')
listingfee_parser.add_argument('is_active', type=bool, default=True)
listingfee_parser.add_argument('payment_frequency', type=str, default='monthly')
listingfee_parser.add_argument('subscription_status', type=str, default='active')

class ListingFeeResource(Resource):
    def post(self):
        args = listingfee_parser.parse_args()

        try:
            start_date = datetime.strptime(args['start_date'], "%Y-%m-%dT%H:%M:%S")
            end_date = datetime.strptime(args['end_date'], "%Y-%m-%dT%H:%M:%S")
        except ValueError as e:
            return {'message': f'Invalid date format: {str(e)}'}, 400

        fee = ListingFee(
            fee_amount=args['fee_amount'],
            fee_type=args['fee_type'],
            start_date=start_date,
            end_date=end_date,
            is_active=args['is_active'],
            payment_frequency=args['payment_frequency'],
            subscription_status=args['subscription_status']
        )

        try:
            db.session.add(fee)
            db.session.commit()
            return {'message': 'Listing fee added successfully', 'id': fee.id}, 201
        except Exception as e:
            db.session.rollback()
            return {'message': f'Error adding listing fee: {str(e)}'}, 500
    
    def get(self, id):
        fee = ListingFee.query.get_or_404(id)

        def format_datetime(dt):
            return dt.strftime("%Y-%m-%dT%H:%M:%S") if dt else None

        return {
            'fee_amount': fee.fee_amount,
            'fee_type': fee.fee_type,
            'start_date': format_datetime(fee.start_date),
            'end_date': format_datetime(fee.end_date),
            'is_active': fee.is_active,
            'payment_frequency': fee.payment_frequency,
            'subscription_status': fee.subscription_status
        }

class PaymentResource(Resource):
    def post(self, id):
        fee = ListingFee.query.get_or_404(id)

        amount = int(fee.fee_amount * 100)  # Convert amount to cents  ==>stripe is in cents
        if amount <= 0:
            return {'message': 'Invalid amount'}, 400
        
        try:
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                description='Listing fee payment',
                metadata={'listing_fee_id': id}
            )

            payment = Payment(
                listing_fee_id=id,
                amount=fee.fee_amount,
                currency='usd',
                payment_method='stripe',
                payment_status='pending',
                transaction_id=payment_intent.id
            )
            db.session.add(payment)
            db.session.commit()

            return {
                'client_secret': payment_intent.client_secret,
                'message': 'Payment intent created successfully'
            }, 200
        
        except stripe.error.StripeError as e:
            return {'message': f"Payment failed: {e.user_message or str(e)}"}, 400
        

class GetListingFeeResource(Resource):
    def get(self, id):
        fee = ListingFee.query.get_or_404(id)
        def format_datetime(dt):
            return dt.strftime("%Y-%m-%dT%H:%M:%S") if dt else None
        
        return {
            'fee_amount': fee.fee_amount,
            'fee_type': fee.fee_type,
            'created_at': format_datetime(fee.created_at),
            'start_date': format_datetime(fee.start_date),
            'end_date': format_datetime(fee.end_date),
            'is_active': fee.is_active,
            'payment_frequency': fee.payment_frequency,
            'subscription_status': fee.subscription_status
        }
    
listingfee_api.add_resource(GetListingFeeResource, '/<int:id>')

#  resources 
listingfee_api.add_resource(ListingFeeResource, '/')
listingfee_api.add_resource(PaymentResource, '/<int:id>/pay')
