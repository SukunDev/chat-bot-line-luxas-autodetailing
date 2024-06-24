from . import db
from datetime import datetime


class LineUser(db.Model):
    __tablename__ = 'line_users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.String(255), unique=True, nullable=False)
    display_name = db.Column(db.String(255)) 
    language = db.Column(db.String(255))
    last_action = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now())

    pelanggan = db.relationship('Pelanggan', backref='pelanggan', uselist=False)
    transaksi = db.relationship('Transaksi', backref='transaksi')

    def __repr__(self) -> str:
        return f"<LineUser(id='{self.id}', display_name='{self.display_name}')>"

    @property
    def serialize(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'display_name': self.display_name,
            'language': self.language,
            'last_action': self.last_action,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
