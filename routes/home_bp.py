from flask import Blueprint

from controllers.homeController import index

home_bp = Blueprint('home_bp', __name__)

home_bp.route('/', methods=['GET'])(index)