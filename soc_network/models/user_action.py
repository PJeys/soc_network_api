from sqlalchemy import PrimaryKeyConstraint, Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from soc_network.models import db


class UserAction(db.Model):
    __tablename__ = 'user_actions'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
    )
    id = Column(Integer, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    action = Column(String(40))
    action_date = Column(DateTime, default=datetime.utcnow())

    users = relationship('User')
