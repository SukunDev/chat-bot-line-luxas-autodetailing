from . import db
from datetime import datetime

class Setting(db.Model):
    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), unique=True, nullable=False)
    value = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f"<Setting(id='{self.id}', name='{self.name}')>"

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'value': self.value,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
