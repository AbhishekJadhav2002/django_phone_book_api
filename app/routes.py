from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import db, SpamReport
from app.utils import search_by_name, search_by_phone
from app import limiter

bp = Blueprint('routes', __name__)

@bp.route('/health', methods=['GET'])
def health():
    return jsonify({'status': 'ok'})

@bp.route('/search/name', methods=['GET'])
@jwt_required()
@limiter.limit("10 per minute")
def search_name():
    query = request.args.get('q')
    results = search_by_name(query)
    return jsonify(results)

@bp.route('/search/phone', methods=['GET'])
@jwt_required()
@limiter.limit("10 per minute")
def search_phone():
    phone_number = request.args.get('phone_number')
    results = search_by_phone(phone_number)
    return jsonify(results)

@bp.route('/mark_spam', methods=['POST'])
@jwt_required()
@limiter.limit("5 per minute")
def mark_spam():
    data = request.get_json()
    phone_number = data['phone_number']
    user_id = get_jwt_identity()

    spam_report = SpamReport(phone_number=phone_number, reported_by=user_id)
    db.session.add(spam_report)
    db.session.commit()

    return jsonify({'message': 'Number marked as spam'}), 201
