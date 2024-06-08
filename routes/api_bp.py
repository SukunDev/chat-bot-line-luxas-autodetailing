from flask import Blueprint

from controllers.apiController import get_keywords, get_keyword, create_keyword

api_bp = Blueprint('api_bp', __name__)

api_bp.route('/keywords', methods=['GET'])(get_keywords)
api_bp.route('/keywords/<id>', methods=['GET'])(get_keyword)
api_bp.route('/keywords/create', methods=['POST'])(create_keyword)