from flask_restful import Api, Resource, reqparse
from server.models import Property, db, Photo
from flask import Blueprint
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity
from server.boostproperty import BoostProperty, GetBoostedProperties  


property_bp = Blueprint('property_bp', __name__, url_prefix='/property')
property_api = Api(property_bp)
CORS(property_bp)

property_args = reqparse.RequestParser()
property_args.add_argument('address', type=str, required=True, help='address is required')
property_args.add_argument('city', type=str, required=True, help='city is required')
property_args.add_argument('square_footage', type=int, required=True, help='square_footage is required')
property_args.add_argument('price', type=int, required=True, help='price is required')
property_args.add_argument('property_type', type=str, required=True, help='property_type is required')
property_args.add_argument('listing_status', type=str, required=True, help='listing_status is required')


# property_args.add_argument('rooms', type=str, required=True, help='rooms is required')
# property_args.add_argument('agent_id', type=int, required=True, help='agent_id is required')

class PropertyResource(Resource):
    
    def get(self, id):
        property = Property.query.get_or_404(id)
        return {
            'id': property.id,
            'address': property.address,
            'city': property.city,
            'square_footage': property.square_footage,
            'price': property.price,
            'property_type': property.property_type,
            'listing_status': property.listing_status,

            'agent_id': property.agent_id
        }

    @jwt_required()
    def patch(self, id):
     property = Property.query.get_or_404(id)
    
    # Use partial argument parsing to allow updating one field at a time
     patch_parser = reqparse.RequestParser()

    # Define only the fields you want to allow to be updated
     patch_parser.add_argument('address', type=str, store_missing=False)
     patch_parser.add_argument('city', type=str, store_missing=False)
     patch_parser.add_argument('square_footage', type=int, store_missing=False)
     patch_parser.add_argument('price', type=int, store_missing=False)
     patch_parser.add_argument('property_type', type=str, store_missing=False)
     patch_parser.add_argument('listing_status', type=str, store_missing=False)

    # Parse arguments
     args = patch_parser.parse_args()

    # Update the property fields with the provided arguments
     if 'address' in args:
        property.address = args['address']
     if 'city' in args:
        property.city = args['city']
     if 'square_footage' in args:
        property.square_footage = args['square_footage']
     if 'price' in args:
        property.price = args['price']
     if 'property_type' in args:
        property.property_type = args['property_type']
     if 'listing_status' in args:
        property.listing_status = args['listing_status']

     db.session.commit()

     return {'msg': 'Property updated successfully'}


    @jwt_required()
    def delete(self, id):
        property = Property.query.get_or_404(id)
        db.session.delete(property)
        db.session.commit()
        return {'message': 'Property deleted'}

property_api.add_resource(PropertyResource, '/<int:id>')


class PropertyListResource(Resource):
   
    def get(self):
        properties = Property.query.all()
        return [{
            'id': property.id,
            'address': property.address,
            'city': property.city,
            'square_footage': property.square_footage,
            'price': property.price,
            'property_type': property.property_type,
            'listing_status': property.listing_status,

            


        } for property in properties]

    @jwt_required()
    def post(self):
     current_user_id = get_jwt_identity()
     args = property_args.parse_args()
     property = Property(
        address=args['address'], 
        city=args['city'], 
        square_footage=args['square_footage'], 
        price=args['price'], 
        property_type=args['property_type'], 
        listing_status=args['listing_status'], 


        

        agent_id=3
    )
     db.session.add(property)
     db.session.commit()
     return {'message': 'Property added successfully', 'property_id': property.id}, 201


property_api.add_resource(PropertyListResource, '/list')

class PhotosOfProperty(Resource):
   
    def get(self, id):
        property = Property.query.get_or_404(id)
        photos = property.photos
        return [{'id': photo.id, 'photo_url': photo.photo_url} for photo in photos]

    @jwt_required()
    def post(self, id):
        property = Property.query.get_or_404(id)
        args = reqparse.RequestParser()
        args.add_argument('photo_url', type=str, required=True, help='photo_url is required')
        args = args.parse_args()
        photo = Photo(photo_url=args['photo_url'], property_id=property.id)
        db.session.add(photo)
        db.session.commit()
        return {"message": "Photo was successfully created"}, 201

property_api.add_resource(PhotosOfProperty, '/<int:id>/photos')

class GetPropertyByCity(Resource):

    def get(self, city):
        properties = Property.query.filter_by(city=city).all()
        return [{'id': property.id, 'address': property.address, 'city': property.city, 'square_footage': property.square_footage, 'price': property.price, 'property_type': property.property_type, 'listing_status': property.listing_status} for property in properties]

property_api.add_resource(GetPropertyByCity, '/city/<string:city>')

class GetPropertyByPriceRange(Resource):
    
    def get(self, min_price, max_price):
        properties = Property.query.filter(Property.price >= min_price, Property.price <= max_price).all()
        return [{'id': property.id, 'address': property.address, 'city': property.city, 'square_footage': property.square_footage, 'price': property.price, 'property_type': property.property_type, 'listing_status': property.listing_status} for property in properties]

property_api.add_resource(GetPropertyByPriceRange, '/price/<int:min_price>/<int:max_price>')

class GetPropertyForSale(Resource):
    
    def get(self):
        properties = Property.query.filter_by(listing_status='for sale').all()
        return [{'id': property.id, 'address': property.address, 'city': property.city, 'square_footage': property.square_footage, 'price': property.price, 'property_type': property.property_type, 'listing_status': property.listing_status} for property in properties]

property_api.add_resource(GetPropertyForSale, '/for-sale')



class GetRentals(Resource):

    def get(self):
        properties = Property.query.filter_by(listing_status='rental').all()
        return [{'id': property.id, 'address': property.address, 'city': property.city, 'square_footage': property.square_footage, 'price': property.price, 'property_type': property.property_type, 'listing_status': property.listing_status} for property in properties]
    

property_api.add_resource(GetRentals,'/rentals')


class GetAgentPropeties(Resource):
   
    @jwt_required()  
    def get(self):
        current_user_id = get_jwt_identity()
        properties = Property.query.filter_by(agent_id = current_user_id )
        return [{'id': property.id, 'address': property.address, 'city': property.city, 'square_footage': property.square_footage, 'price': property.price, 'property_type': property.property_type, 'listing_status': property.listing_status } for property in properties]
    
property_api.add_resource(GetAgentPropeties, '/agents')
property_api.add_resource(BoostProperty, '/boost')
property_api.add_resource(GetBoostedProperties, '/boosted')
