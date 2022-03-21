from sqlalchemy import PrimaryKeyConstraint, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from soc_network.models import db


class PostAction(db.Model):
    __tablename__ = 'post_actions'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
    )
    id = Column(Integer, autoincrement=True)
    action = String(20)
    post_id = Column(Integer, ForeignKey('posts.id'))
    user_id = Column(Integer, ForeignKey('users.id'))
    date_of_action = Column(DateTime, default=datetime.utcnow())

    users = relationship('User')
    posts = relationship('Post')
