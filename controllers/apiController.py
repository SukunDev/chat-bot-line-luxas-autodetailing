from flask import jsonify, request
from models import db, Keyword

def get_keywords():
    all_keywords = Keyword.query.all()
    keywords = []
    for keyword in all_keywords:
        keywords.append(keyword.serialize)
    return jsonify({"status": True, "messages": "success to get keywords", "result": keywords}), 200

def get_keyword(id):
    keyword = Keyword.query.filter_by(id=id).first()
    if keyword is None:
         return jsonify({"status": False, "message": "keyword not found"}), 404
    return jsonify({"status": True, "messages": "success to get keywords", "result": keyword.serialize}), 200

def create_keyword():
    keyword = request.get_json().get("keywords")
    if keyword is None:
        return jsonify({"status": False, "message": "keyword field cannot empty"}), 400
    answer = request.get_json().get("answer")
    if answer is None:
        return jsonify({"status": False, "message": "answer field cannot empty"}), 400
    keyword = str(keyword).lower()
    check_keywords = Keyword.query.filter_by(keywords=keyword).first()
    if check_keywords is not None:
        return jsonify({"status": False, "message": "keywords has been created"}), 302
    try:
        new_keywords = Keyword(keywords=keyword, answer=answer)
        db.session.add(new_keywords)
        db.session.commit()
        return jsonify({"status": True, "message": "success to create keywords", "result":new_keywords.serialize}), 201
    except Exception as e:
        return jsonify({"status": False, "message": e}), 400