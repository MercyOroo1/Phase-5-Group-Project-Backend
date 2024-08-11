from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models import Review, db

review_bp = Blueprint('reviews', __name__, url_prefix='/reviews')

@review_bp.route('/gotten', methods=['POST'])
@jwt_required()
def add_review():
    data = request.get_json()
    user_id = get_jwt_identity()

    new_review = Review(
        property_id=data['property_id'],
        user_id=user_id,
        rating=data['rating'],
        comment=data['comment']
    )

    db.session.add(new_review)
    db.session.commit()

    return jsonify({'message': 'Review added successfully'}), 201
