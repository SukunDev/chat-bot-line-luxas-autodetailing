import sys
from flask import jsonify


def index():
    return jsonify({"status": True, "message": "Line Chat Bot Is Ready"})