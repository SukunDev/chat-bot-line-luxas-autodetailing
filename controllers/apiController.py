from flask import jsonify, request
from werkzeug.utils import secure_filename
from models import db, Keyword, Product, RekomendasiProduct
import os

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
    keyword = request.form.get("keywords")
    if keyword is None:
        return jsonify({"status": False, "message": "keyword field cannot empty"}), 400
    answer = request.form.get("answer")
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

def delete_keyword(id):
    try:
        keyword = Keyword.query.get(id)
        if keyword is None:
            return jsonify({"status": False, "message": "Keyword not found"}), 404

        db.session.delete(keyword)
        db.session.commit()
        return jsonify({"status": True, "message": "Keyword deleted successfully"}), 200
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 400


def get_products():
    all_product = Product.query.all()
    products = []
    for product in all_product:
        products.append(product.serialize)
    return jsonify({"status": True, "messages": "success to get products", "result": products}), 200

def get_product(id):
    product = Product.query.filter_by(id=id).first()
    if product is None:
         return jsonify({"status": False, "message": "product not found"}), 404
    return jsonify({"status": True, "messages": "success to get product", "result": product.serialize}), 200



def create_product():
    def allowed_file(filename):
        return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg'}
    name = request.form.get("name")
    if name is None:
        return jsonify({"status": False, "message": "name field cannot be empty"}), 400
    
    thumbnail = request.files.get("thumbnail")
    if thumbnail is None or thumbnail.filename == '':
        return jsonify({"status": False, "message": "thumbnail field cannot be empty"}), 400
    if not allowed_file(thumbnail.filename):
        return jsonify({"status": False, "message": "Invalid file type for thumbnail"}), 400

    price = request.form.get("price")
    if price is None:
        return jsonify({"status": False, "message": "price field cannot be empty"}), 400

    description = request.form.get("description")
    if description is None:
        return jsonify({"status": False, "message": "description field cannot be empty"}), 400

    check_name_product = Product.query.filter_by(name=name).first()
    if check_name_product is not None:
        return jsonify({"status": False, "message": "Product has been created"}), 302

    try:
        filename = secure_filename(thumbnail.filename)
        file_path = os.path.join("./assets/product/", filename)
        thumbnail.save(file_path)
        thumbnail_url = os.path.join("/assets/product/", filename)
        new_product = Product(name=name, thumbnail=thumbnail_url, price=price, description=description)
        db.session.add(new_product)
        db.session.commit()
        return jsonify({"status": True, "message": "success to create product", "result": new_product.serialize}), 201
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 400


def delete_product(id):
    try:
        product = Product.query.get(id)
        if product is None:
            return jsonify({"status": False, "message": "Product not found"}), 404
        db.session.delete(product)
        db.session.commit()
        return jsonify({"status": True, "message": "Product deleted successfully"}), 200
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 400

def get_all_rekomendasi():
    all_rekomendasi = RekomendasiProduct.query.all()
    rekomendasi = []
    for product in all_rekomendasi:
        rekomendasi.append(product.serialize)
    return jsonify({"status": True, "messages": "success to get products", "result": rekomendasi}), 200

def get_rekomendasi(id):
    rekomendasi = RekomendasiProduct.query.filter_by(id=id).first()
    if rekomendasi is None:
         return jsonify({"status": False, "message": "rekomendasi not found"}), 404
    return jsonify({"status": True, "messages": "success to get rekomendasi", "result": rekomendasi.serialize}), 200


def create_rekomendasi():
    product_id = request.form.get("product_id")
    if product_id is None:
        return jsonify({"status": False, "message": "product_id field cannot be empty"}), 400
    check_name_rekomendasi = RekomendasiProduct.query.filter_by(product_id=product_id).first()
    if check_name_rekomendasi is not None:
        return jsonify({"status": False, "message": "Rekomendasi has been created"}), 302
    product = Product.query.filter_by(id=product_id).first()
    if product is None:
         return jsonify({"status": False, "message": "product not found"}), 404
    try:
        new_rekomendasi_product = RekomendasiProduct(product_id=product_id)
        db.session.add(new_rekomendasi_product)
        db.session.commit()
        return jsonify({"status": True, "message": "success to create Rekomendasi Product", "result": new_rekomendasi_product.serialize}), 201
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 400

def delete_rekomendasi(id):
    try:
        rekomendasi = RekomendasiProduct.query.get(id)
        if rekomendasi is None:
            return jsonify({"status": False, "message": "Rekomendasi Product not found"}), 404
        db.session.delete(rekomendasi)
        db.session.commit()
        return jsonify({"status": True, "message": "Rekomendasi Product deleted successfully"}), 200
    except Exception as e:
        return jsonify({"status": False, "message": str(e)}), 400