from app import db
from datetime import datetime
import enum

class CategoryEnum(enum.Enum):
    news = 'news'
    publication = 'publication'
    tech = 'tech'
    other = 'other'

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)
    content = db.Column(db.Text, nullable=False)
    posted = db.Column(db.DateTime, default=datetime.utcnow)
    category = db.Column(db.Enum(CategoryEnum), default=CategoryEnum.other)
    is_active = db.Column(db.Boolean, default=True)
    author = db.Column(db.String(20), default='Anonymous')

    def __repr__(self):
        return f"Post('{self.title}', '{self.posted}')"
