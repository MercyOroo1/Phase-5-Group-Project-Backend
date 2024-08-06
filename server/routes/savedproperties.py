from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from models import SavedProperty, db, Property
from flask_cors import CORS
from flask_jwt_extended import jwt_required, get_jwt_identity

saved_bp = Blueprint("savedproperties", __name__, url_prefix="/savedproperties")
saved_api = Api(saved_bp)
CORS(saved_bp)

saved_parser = reqparse.RequestParser()
saved_parser.add_argument("property_id", type=int, required=True, help="property_id is required")

class SavedProperties(Resource):
    @jwt_required()
    def get(self, user_id):
        saved_properties = SavedProperty.query.filter_by(user_id=user_id).all()
        return [{
            'id': saved_property.id,
            'property_id': saved_property.property_id,
            'property': {
                'id': saved_property.property.id,
                'address': saved_property.property.address,
                'city': saved_property.property.city,
                'square_footage': saved_property.property.square_footage,
                'price': saved_property.property.price,
                'property_type': saved_property.property.property_type,
                'listing_status': saved_property.property.listing_status,
                'rooms': saved_property.property.rooms,
                'photos': [{'id': photo.id, 'photo_url': photo.photo_url} for photo in saved_property.property.photos]
            }
        } for saved_property in saved_properties], 200
    
saved_api.add_resource(SavedProperties, '/<int:user_id>')


class MoveSaved(Resource):
    @jwt_required()
    def post(self):
        args = saved_parser.parse_args()
        property = Property.query.get(args['property_id'])
        current_user_id = get_jwt_identity()

        if not property:
            return {'message': 'Property not found'}, 404
        
        if SavedProperty.query.filter_by(user_id=current_user_id, property_id=args['property_id']).first():
            return {'message': 'Property already saved'}, 400
        
        saved_property = SavedProperty(user_id=current_user_id, property_id=args['property_id'])
        db.session.add(saved_property)
        db.session.commit()
        return {'message': 'Property saved successfully'}, 201

saved_api.add_resource(MoveSaved, '/saved')
