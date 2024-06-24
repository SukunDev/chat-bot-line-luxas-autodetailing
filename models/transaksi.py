from . import db
from datetime import datetime
import enum

class StatusTransaksi(enum.Enum):
    PENDING = "pending"
    BERHASIL = "berhasil"
    GAGAL = "gagal"

class StatusPembayaran(enum.Enum):
    PENDING = "pending"
    BERHASIL = "berhasil"
    GAGAL = "gagal"


class Transaksi(db.Model):
    __tablename__ = 'transaksi'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    line_user_id = db.Column(db.Integer, db.ForeignKey('line_users.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    status_transaksi = db.Column(db.Enum(StatusTransaksi), nullable=False)
    status_pembayaran = db.Column(db.Enum(StatusPembayaran), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    product = db.relationship('Product', backref='product', uselist=False)

    def __repr__(self) -> str:
        return f"<Transaksi(id='{self.id}')>"

    @property
    def serialize(self):
        return {
            'id': self.id,
            'line_user_id': self.line_user_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }


