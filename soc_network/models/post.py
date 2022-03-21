from sqlalchemy import PrimaryKeyConstraint, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from soc_network.models import db


class Post(db.Model):
    __tablename__ = 'posts'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
    )
    id = Column(Integer, autoincrement=True)
    author_id = Column(Integer, ForeignKey('users.id'))
    date_created = Column(DateTime, default=datetime.utcnow())
    post_text = Column(String(255))
    likes = Column(Integer, default=0)
    media_ref = Column(String(255))

    user = relationship('User')
