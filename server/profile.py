from flask import Blueprint, request, jsonify
from flask_restful import Api, Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity
from  server.models import db, Profile, User

profile_bp = Blueprint('profile', __name__, url_prefix='/profile')
profile_api = Api(profile_bp)

profile_parser = reqparse.RequestParser()
profile_parser.add_argument('photo_url', type=str, required=False, help='This field cannot be left blank')
profile_parser.add_argument('bio', type=str, required=False, help='This field cannot be left blank')
profile_parser.add_argument('phone_number', type=str, required=False, help='This field cannot be left blank')
profile_parser.add_argument('website', type=str, required=False, help='This field cannot be left blank')

class UserProfile(Resource):
    
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        profile = Profile.query.filter_by(user_id=user_id).first()
        if profile is None:
            return {'message': 'Profile not found'}, 404
        return jsonify({
            'full_name': profile.user.full_name,
            "email":profile.user.email,
            'photo_url': profile.photo_url,
            'bio': profile.bio,
            'phone_number': profile.phone_number,
            'website': profile.website
        })

    @jwt_required()
    def post(self):
        user_id = get_jwt_identity()
        args = profile_parser.parse_args()
        profile = Profile.query.filter_by(user_id=user_id).first()

        if profile:
            return {'message': 'Profile already exists'}, 400

        profile = Profile(
            user_id=user_id,
            photo_url=args.get('photo_url'),
            bio=args.get('bio'),
            phone_number=args.get('phone_number'),
            website=args.get('website')
        )
        db.session.add(profile)
        db.session.commit()

        return jsonify({
            'photo_url': profile.photo_url,
            'bio': profile.bio,
            'phone_number': profile.phone_number,
            'website': profile.website
        }), 201

    @jwt_required()
    def put(self):
        user_id = get_jwt_identity()
        args = profile_parser.parse_args()
        profile = Profile.query.filter_by(user_id=user_id).first()

        if profile:
            # Update existing profile
            profile.photo_url = args.get('photo_url', profile.photo_url)
            profile.bio = args.get('bio', profile.bio)
            profile.phone_number = args.get('phone_number', profile.phone_number)
            profile.website = args.get('website', profile.website)
            db.session.commit()
        else:
            # Create new profile
            profile = Profile(
                user_id=user_id,
                photo_url=args.get('photo_url'),
                bio=args.get('bio'),
                phone_number=args.get('phone_number'),
                website=args.get('website')
            )
            db.session.add(profile)
            db.session.commit()

        return jsonify({
            'photo_url': profile.photo_url,
            'bio': profile.bio,
            'phone_number': profile.phone_number,
            'website': profile.website
        })

    @jwt_required()
    def delete(self):
        user_id = get_jwt_identity()
        profile = Profile.query.filter_by(user_id=user_id).first()
        user = User.query.filter_by(id=user_id).first()

        if profile is None:
            return {'message': 'Profile not found'}, 404

        db.session.delete(profile)
        db.session.commit()

        if user:
            db.session.delete(user)
            db.session.commit()

        return {'message': 'Profile and User deleted successfully.'}, 200

profile_api.add_resource(UserProfile, '/')
