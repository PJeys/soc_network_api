from sqlalchemy import PrimaryKeyConstraint, Column, Integer, String, DateTime, UniqueConstraint

from soc_network.models import db


class User(db.Model):
    __tablename__ = 'users'
    __table_args__ = (
        PrimaryKeyConstraint('id'),
        UniqueConstraint('token')
    )
    id = Column(Integer, autoincrement=True)
    public_id = Column(String(50))
    first_name = Column(String(100))
    last_name = Column(String(100))
    status = Column(String(255))
    birth_date = Column(DateTime)
    email = Column(String(50))
    password = Column(String(30))
    token = Column(String(60))
