from flask import Blueprint

from controllers.apiController import get_keywords, get_keyword, create_keyword,delete_keyword, get_products, get_product, create_product, delete_product, get_all_rekomendasi,get_rekomendasi, create_rekomendasi, delete_rekomendasi

api_bp = Blueprint('api_bp', __name__)

api_bp.route('/keywords', methods=['GET'])(get_keywords)
api_bp.route('/keywords/<id>', methods=['GET'])(get_keyword)
api_bp.route('/keywords/create', methods=['POST'])(create_keyword)
api_bp.route('/keywords/delete/<id>', methods=['GET'])(delete_keyword)

api_bp.route('/products', methods=['GET'])(get_products)
api_bp.route('/products/<id>', methods=['GET'])(get_product)
api_bp.route('/products/create', methods=['POST'])(create_product)
api_bp.route('/products/delete/<id>', methods=['GET'])(delete_product)


api_bp.route('/rekomendasi', methods=['GET'])(get_all_rekomendasi)
api_bp.route('/rekomendasi/<id>', methods=['GET'])(get_rekomendasi)
api_bp.route('/rekomendasi/create', methods=['POST'])(create_rekomendasi)
api_bp.route('/rekomendasi/delete/<id>', methods=['GET'])(delete_rekomendasi)
