from flask_restful import Api,Resource,reqparse
from models import Property, db
from flask import Blueprint



property_bp = Blueprint('property_bp', __name__, url_prefix='/property')
property_api = Api(property_bp)

property_args = reqparse.RequestParser()
property_args.add_argument('address', type=str, required=True, help='address is required')
property_args.add_argument('city', type=str, required=True, help='city is required')
property_args.add_argument('square_footage', type=int, required=True, help='square_footage is required')
property_args.add_argument('price', type=int, required=True, help='price is required')
property_args.add_argument('property_type', type=str, required=True, help='property_type is required')
property_args.add_argument('listing_status', type=str, required=True, help='listing_status is required')
property_args.add_argument('rooms', type=str, required=True, help='rooms is required')
