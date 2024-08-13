from flask_restful import Resource, Api
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Property, db
from flask import Blueprint

boost_bp = Blueprint("boost", __name__, url_prefix="/boost")
boost_bp_api = Api(boost_bp)

class BoostProperty(Resource):
    @jwt_required()
    def post(self):
        current_user_id = get_jwt_identity()
        
        property = Property.query.filter_by(agent_id=current_user_id).order_by(Property.created_at.desc()).first()
        
        if property:
            previous_boosted_property = Property.query.filter_by(boosted=False).first()
            if previous_boosted_property:
                previous_boosted_property.boosted = True
                db.session.commit()
            
            property.boosted = True
            db.session.commit()
            return {'message': 'Property boosted successfully', 'property_id': property.id}, 200
        
        return {'message': 'No properties found to boost'}, 404

class GetBoostedProperties(Resource):
    def get(self):
        boosted_properties = Property.query.filter_by(boosted=True).all()
        return [{
            'id': property.id,
            'address': property.address,
            'city': property.city,
            'square_footage': property.square_footage,
            'price': property.price,
            'property_type': property.property_type,
            'listing_status': property.listing_status,
            'rooms': property.rooms
        } for property in boosted_properties], 200

boost_bp_api.add_resource(BoostProperty, '/property') 
boost_bp_api.add_resource(GetBoostedProperties, '/properties') 