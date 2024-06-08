from . import db
from datetime import datetime

class Product(db.Model):
    __tablename__ = 'products'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    thumbnail = db.Column(db.String(255))
    description = db.Column(db.String(255))
    price = db.Column(db.Integer)
    created_at = db.Column(db.DateTime)

    def __repr__(self) -> str:
        return f"<Product(id='{self.id}', name='{self.name}')>"

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
