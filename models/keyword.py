from . import db
from datetime import datetime

class Keyword(db.Model):
    __tablename__ = 'keywords'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    keywords = db.Column(db.String(255), unique=True, nullable=False)
    answer = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f"<Keyword(id='{self.id}', keywords='{self.keywords}')>"

    @property
    def serialize(self):
        return {
            'id': self.id,
            'keywords': self.keywords,
            'answer': self.answer,
            'created_at': self.created_at
        }
