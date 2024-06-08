from flask import Blueprint

from controllers.webhookController import index

webhook_bp = Blueprint('webhook_bp', __name__)

webhook_bp.route('', methods=['GET','POST'])(index)