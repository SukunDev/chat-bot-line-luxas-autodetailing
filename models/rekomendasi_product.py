from . import db
from datetime import datetime

class RekomendasiProduct(db.Model):
    __tablename__ = 'rekomendasi_products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    product = db.relationship('Product', backref='products', uselist=False)

    def __repr__(self) -> str:
        return f"<RekomendasiProduct(id='{self.id}', product_id='{self.product_id}')>"

    @property
    def serialize(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'product': self.product.serialize,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


