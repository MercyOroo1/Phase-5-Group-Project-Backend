from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from models import User, Profile, db

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')
profile_api = Api(profile_bp)

profile_parser = reqparse.RequestParser()
profile_parser.add_argument('photo_url', type=str, required=True, help='This field cannot be left blank')
profile_parser.add_argument('bio', type=str, required=True, help='This field cannot be left blank')
profile_parser.add_argument('phone_number', type=str, required=True, help='This field cannot be left blank')
profile_parser.add_argument('website', type=str, required=True, help='This field cannot be left blank')

class UserProfile(Resource):
    def get(self, user_id):
        # user = User.query.get_or_404(id)
        profile = Profile.query.filter_by(user_id=user_id).first()

        if profile is None:
            return {'message': 'Profile not found'}, 404
        
        return {
            'photo_url': profile.photo_url,
            'bio': profile.bio,
            'phone_number': profile.phone_number,
            'website': profile.website
        }, 200
    
    def put(self, user_id):
        user = User.query.get_or_404(user_id)
        args = profile_parser.parse_args()

        profile = Profile.query.filter_by(user_id=user_id).first()

        if profile:
            # Update existing profile
            profile.photo_url = args['photo_url']
            profile.bio = args['bio']
            profile.phone_number = args['phone_number']
            profile.website = args['website']
        else:
            # Create new profile
            profile = Profile(
                user_id=user_id,
                photo_url=args['photo_url'],
                bio=args['bio'],
                phone_number=args['phone_number'],
                website=args['website']
            )
            db.session.add(profile)

        db.session.commit()

        return {
            'photo_url': profile.photo_url,
            'bio': profile.bio,
            'phone_number': profile.phone_number,
            'website': profile.website
        }, 200
    
    def delete(self, user_id):
        user = User.query.get_or_404(user_id)
        profile = Profile.query.filter_by(user_id=user_id).first()

        if profile is None:
            return {'message': 'Profile not found'}, 404
        
        db.session.delete(profile)
        db.session.commit()

        return {'message': 'Profile deleted successfully.'}, 200
    def post(self, user_id):
        args = profile_parser.parse_args()
        profile = Profile(
            user_id=user_id,
            photo_url=args['photo_url'],
            bio=args['bio'],
            phone_number=args['phone_number'],
            website=args['website']
        )
        db.session.add(profile)
        db.session.commit()

       

profile_api.add_resource(UserProfile, '/<int:user_id>')
