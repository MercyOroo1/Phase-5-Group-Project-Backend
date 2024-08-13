from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from models import db ,Feature



features_bp = Blueprint('feature', __name__,url_prefix='/features')
features_api = Api(features_bp)
features_parser=reqparse.RequestParser()
features_parser.add_argument('name', type=str, required=True, help='Name of the feature is required')
features_parser.add_argument('description', type=str, required=True, help='Description of the feature is required')
features_parser.add_argument('property_id', type=int, required=True, help='Property id of the feature is required')

class FeatureResource(Resource):
    def get(self, property_id):
        features = Feature.query.filter_by(property_id=property_id)
        return [{'name': feature.name,'description': feature.description} for feature in features]
    
    def put(self, property_id):
        args = features_parser.parse_args()
        feature = Feature.query.filter_by(property_id=property_id)
        feature.name = args['name']
        feature.description = args['description']
        db.session.commit()
        return {'message':'feature updated' }
    
    def delete(self, property_id):
        feature = Feature.query.filter_by(property_id=property_id)
        db.session.delete(feature)
        db.session.commit()
        return {'message': 'Feature deleted successfully'}
    

features_api.add_resource(FeatureResource, '/<int:property_id>')

class FeatureListResource(Resource):
    def get(self):
        features = Feature.query.all()
        return[{ 'name':feature.name,'description':feature.description}for feature in features]
    def post(self):
        args = features_parser.parse_args()
        feature = Feature(name=args['name'], description=args['description'], property_id=args['property_id'])
        db.session.add(feature)
        db.session.commit()
        return {'message':'Feature added successfully' }
    

features_api.add_resource(FeatureListResource, '/list')
    