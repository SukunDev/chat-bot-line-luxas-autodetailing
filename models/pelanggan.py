from . import db
from datetime import datetime


class Pelanggan(db.Model):
    __tablename__ = 'pelanggan'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    line_user_id = db.Column(db.Integer, db.ForeignKey('line_users.id'), nullable=False)
    name = db.Column(db.String(255))
    no_hp = db.Column(db.String(255))
    alamat = db.Column(db.String(255))
    kota_kab = db.Column(db.String(255))
    provinsi = db.Column(db.String(255))
    kode_pos = db.Column(db.String(255))
    rt = db.Column(db.String(255))
    rw = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now())

    

    def __repr__(self) -> str:
        return f"<Pelanggan(id='{self.id}', name='{self.name}')>"

    @property
    def serialize(self):
        return {
            'id': self.id,
            'line_user_id': self.line_user_id,
            'name': self.name,
            'no_hp': self.no_hp,
            'alamat': self.alamat,
            'kota_kab': self.kota_kab,
            'provinsi': self.provinsi,
            'kode_pos': self.kode_pos,
            'rt': self.rt,
            'rw': self.rw,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
