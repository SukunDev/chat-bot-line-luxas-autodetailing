from . import db
from datetime import datetime

class RichMenu(db.Model):
    __tablename__ = 'rich_menus'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    rich_menu_id = db.Column(db.String(255), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())

    def __repr__(self) -> str:
        return f"<RichMenu(id='{self.id}', name='{self.name}')>"

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'rich_menu_id': self.rich_menu_id,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S')
        }
