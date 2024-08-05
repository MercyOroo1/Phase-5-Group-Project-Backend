from flask_restful import Api, Resource, reqparse
from models import db, Photo
from flask import Blueprint
from flask_cors import CORS

photo_bp = Blueprint('photo_bp', __name__, url_prefix='/photo')
photo_api = Api(photo_bp)
CORS(photo_bp)

photo_parser = reqparse.RequestParser()
photo_parser.add_argument('photo_url', type=str, help='photo_url is optional')
photo_parser.add_argument('property_id', type=int, help='property_id is optional')

class PhotoResource(Resource):
    def get(self, id):
        photo = Photo.query.get_or_404(id)
        return {'id': photo.id, 'photo_url': photo.photo_url, 'property_id': photo.property_id}
   
    def put(self, id):
        photo = Photo.query.get_or_404(id)
        args = photo_parser.parse_args()
        photo.photo_url = args['photo_url'] if args['photo_url'] else photo.photo_url
        photo.property_id = args['property_id'] if args['property_id'] else photo.property_id
        db.session.commit()
        return {'id': photo.id, 'photo_url': photo.photo_url, 'property_id': photo.property_id}
   
    def delete(self, id):
        photo = Photo.query.get_or_404(id)
        db.session.delete(photo)
        db.session.commit()
        return {'message': 'Photo deleted'}

photo_api.add_resource(PhotoResource, '/<int:id>')

class PhotoListResource(Resource):
    def get(self):
        photos = Photo.query.all()
        return [{'id': photo.id, 'photo_url': photo.photo_url, 'property_id': photo.property_id} for photo in photos]
    
    def post(self):
        args = photo_parser.parse_args()
        if args['photo_url'] is None or args['property_id'] is None:
            return {'message': 'Both photo_url and property_id are required'}, 400
        photo = Photo(photo_url=args['photo_url'], property_id=args['property_id'])
        db.session.add(photo)
        db.session.commit()
        return {'message': 'Photo added successfully'}, 201
    
    def patch(self):
        args = photo_parser.parse_args()
        if args['property_id'] is None:
            return {'message': 'property_id is required to update photos'}, 400
        photos = Photo.query.filter_by(property_id=args['property_id']).all()
        if not photos:
            return {'message': 'No photos found for the given property_id'}, 404
        for photo in photos:
            if args['photo_url'] is not None:
                photo.photo_url = args['photo_url']
        db.session.commit()
        return {'message': 'Photos updated successfully'}

photo_api.add_resource(PhotoListResource, '/list')

class PhotosOfProperty(Resource):
    def get(self, property_id):
        photos = Photo.query.filter_by(property_id=property_id).all()
        if not photos:
            return {'message': 'No photos found for this property'}, 404
        return [{'id': photo.id, 'photo_url': photo.photo_url, 'property_id': photo.property_id} for photo in photos]

photo_api.add_resource(PhotosOfProperty, 'photos/<int:property_id>')
