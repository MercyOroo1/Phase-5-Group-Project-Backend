from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from models import db ,Features



features_bp = Blueprint('features', __name__,url_prefix='/features')
features_api = Api(features_bp)
features_parser=reqparse.RequestParser()
features_parser.add_argument('name', type=str, required=True, help='Name of the feature is required')
features_parser.add_argument('description', type=str, required=True, help='Description of the feature is required')
features_parser.add_argument('property_id', type=int, required=True, help='Property id of the feature is required')

class FeaturesResource(Resource):
    def get(self, property_id):
        feature = Features.query.filter_by(property_id=property_id)
        return {'name': feature.name,'description': feature.description}
    
    def put(self, property_id):
        args = features_parser.parse_args()
        feature = Features.query.filter_by(property_id=property_id)
        feature.name = args['name']
        feature.description = args['description']
        db.session.commit()
        return {'message':'feature updated' }
    
    def delete(self, property_id):
        feature = Features.query.filter_by(property_id=property_id)
        db.session.delete(feature)
        db.session.commit()
        return {'message': 'Feature deleted successfully'}
    

features_api.add_resource(FeaturesResource, '/<int:id>')

class FeaturesListResource(Resource):
    def get(self):
        features = Features.query.all()
        return[{ 'name':feature.name,'description':feature.description}for feature in features]
    def post(self):
        args = features_parser.parse_args()
        feature = Features(name=args['name'], description=args['description'], property_id=args['property_id'])
        db.session.add(feature)
        db.session.commit()
        return {'message':'Feature added successfully' }
    

features_api.add_resource(FeaturesListResource, '/list')
    