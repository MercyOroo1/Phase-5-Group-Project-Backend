from flask import Blueprint, request
from flask_restful import Api, Resource, reqparse
from flask_cors import CORS
from models import ListingFee, db, Payment,Agent,AgentApplication,User
from flask_jwt_extended import jwt_required, get_jwt_identity


from datetime import datetime
import os
import stripe
from flask_mail import Message


listingfee_bp = Blueprint('listingfee', __name__, url_prefix='/listingfee')
listingfee_api = Api(listingfee_bp)
CORS(listingfee_bp)

listingfee_parser = reqparse.RequestParser()
listingfee_parser.add_argument('fee_amount', type=float, required=True, help='Amount cannot be blank')
listingfee_parser.add_argument('fee_type', type=str, required=True, help='Fee type cannot be blank')
listingfee_parser.add_argument('start_date', type=str, required=True, help='Start date cannot be blank')
listingfee_parser.add_argument('end_date', type=str, required=True, help='End date cannot be blank')
listingfee_parser.add_argument('is_active', type=bool, default=True)
listingfee_parser.add_argument('payment_frequency', type=str, default='monthly')
listingfee_parser.add_argument('subscription_status', type=str, default='active')


stripe.api_key = os.getenv('STRIPE_API_KEY')  

class ListingFeeResource(Resource):
    def post(self):
        args = listingfee_parser.parse_args()
        
        start_date = datetime.strptime(args['start_date'], "%Y-%m-%dT%H:%M:%S")
        end_date = datetime.strptime(args['end_date'], "%Y-%m-%dT%H:%M:%S")
        
        fee = ListingFee(
            fee_amount=args['fee_amount'],
            fee_type=args['fee_type'],
            start_date=start_date,
            end_date=end_date,
            is_active=args['is_active'],
            payment_frequency=args['payment_frequency'],
            subscription_status=args['subscription_status']
        )
        
        db.session.add(fee)
        db.session.commit()
        return {'message': 'Listing fee added successfully', 'id': fee.id}, 201



payment_parser = reqparse.RequestParser()
payment_parser.add_argument('agent_id', type=float, required=True, help='Agent ID cannot be blank')
payment_parser.add_argument('application_id', type=float, required=True, help='Application ID cannot be blank')

listingfee_api.add_resource(ListingFeeResource,'/')

class PaymentResource(Resource):
    def __init__(self, mail):
        self.mail = mail

    def post(self, id):
        # Parse the arguments from the request
        args = payment_parser.parse_args()
        application_id = args['application_id']
        
        # Fetch the listing fee based on the provided ID
        fee = ListingFee.query.get_or_404(id)
        amount = int(fee.fee_amount * 100)  # Convert amount to cents
        if amount <= 0:
            return {'message': 'Invalid amount'}, 400
        
        try:
            # Create a PaymentIntent with Stripe
            payment_intent = stripe.PaymentIntent.create(
                amount=amount,
                currency='usd',
                description='Listing fee payment',
                metadata={'listing_fee_id': id}
            )

            # Save the payment to the database
            payment = Payment(
                agent_id=args['agent_id'],
                listing_fee_id=id,
                amount=fee.fee_amount,
                currency='usd',
                payment_method='stripe',
                payment_status="successful",
                transaction_id=payment_intent.id
            )
            db.session.add(payment)
            db.session.commit()

            # Fetch the agent application based on the provided application_id
            application = AgentApplication.query.get_or_404(application_id)
            payment = Payment.query.filter_by(agent_id=application.user_id).first()

            # Check if the payment was successful
            if payment.payment_status == 'successful':
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

                # Update the user's role to 'agent'
                new_role = User.query.get(application.user_id)
                new_role.role_id = 2  # Change the role to agent

                db.session.add(new_agent)
                db.session.add(new_role)
                db.session.commit()

                # Send a confirmation email to the new agent
                subject = "Agent Account Activated"
                body = (
                    f"Dear {application.full_name},\n\n"
                    "Thank you for completing your subscription payment. "
                    "Your agent account has been successfully activated. "
                    "You can now start listing properties on our platform.\n\n"
                    "Welcome aboard!"
                )

                msg = Message(
                    subject,
                    sender="mercy.oroo.ke@gmail.com",
                    recipients=[application.email]
                )
                msg.body = body
                self.mail.send(msg)

                return {
                    'client_secret': payment_intent.client_secret,
                    'message': 'Payment intent created successfully and agent account created'
                }, 200

        except stripe.error.StripeError as e:
            print(f"Stripe error: {e}")
            return {'message': f"Payment failed: {e.user_message or str(e)}"}, 400

# Adding the PaymentResource to the API
def create_resources4(mail):
    listingfee_api.add_resource(PaymentResource, '/<int:id>/pay', resource_class_kwargs={'mail': mail})


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




