from flask import Blueprint
from flask_restful import Api, Resource, reqparse
from models import Review, db
from flask_jwt_extended import jwt_required, get_jwt_identity
from flask_cors import CORS

review_bp = Blueprint("reviews", __name__, url_prefix="/reviews")
review_api = Api(review_bp)

CORS(review_bp)


review_parser = reqparse.RequestParser()
review_parser.add_argument("rating", type=int, required=True, help="Rating is required")
review_parser.add_argument("comment", type=str, required=True, help="Comment is required")

class ReviewResource(Resource):
    @jwt_required()
    def post(self):
        args = review_parser.parse_args()
        current_user_id = get_jwt_identity()  

        new_review = Review(
        
            user_id=current_user_id,
            rating=args['rating'],
            comment=args['comment']
        )
        
        db.session.add(new_review)
        db.session.commit()
        return {'message': 'Review added successfully'}, 201
    
    
    def get(self):
        reviews = Review.query.all()
        if not reviews :
            return {'message': 'No reviews yet'}
        
        return {[{'user_id': review.user_id, 'rating' : review.rating, 'comment': review.comment} for review in reviews]},200
        
review_api.add_resource(ReviewResource, '/gotten')