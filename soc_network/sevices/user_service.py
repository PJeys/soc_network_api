from datetime import datetime, timedelta
from os import getenv
from dotenv import load_dotenv
from soc_network.models import User, db
from soc_network.utils.validator import email_validator, password_validator
from soc_network.sevices.post_service import PostService
import jwt
import uuid
from typing import Union
from soc_network.sevices.user_actions_service import UserActionService


class UserService:
    def register(self, email: str, password: str):
        if self.is_exist(email):
            return 0                                # 0 means that user already registered
        if not email_validator(email):
            return -1
        if not password_validator(password):
            return -2
        user = User(email=email, password=password, public_id=str(uuid.uuid4()))
        db.session.add(user)
        db.session.commit()
        UserActionService().add_action(user.id, 'reg')
        return 1

    def login(self, email: str, password: str):
        u = User.query.filter(User.email == email, User.password == password).first()
        if u:
            UserActionService().add_action(u.id, 'login')
            return self.generate_token(u.public_id)
        return False

    @staticmethod
    def is_exist(email: str):
        u = User.query.filter(User.email == email).first()
        if u:
            return True
        return False

    @staticmethod
    def create_post(public_id: str, text: int, media: int=None):
        user = User.query.filter(User.public_id == public_id).first()
        PostService().create_post(author_id=user.id, text=text, media=media)

    @staticmethod
    def check_token(token: str) -> Union[User, bool]:
        load_dotenv()
        key = getenv('SECRET_KEY')
        decoded_token = jwt.decode(token, key, algorithms=['HS256'])['public_id']
        print(decoded_token)
        u = User.query.filter(User.public_id == decoded_token).first()
        if not u:
            return False
        return u

    @staticmethod
    def generate_token(pub_id: str):
        load_dotenv()
        token = jwt.encode({
            'public_id': pub_id,
            'exp': datetime.utcnow() + timedelta(minutes=30)
        }, getenv('SECRET_KEY'))
        return token

    @staticmethod
    def like_post(pub_id: str, post_id: int):
        user = User.query.filter(User.public_id == pub_id).first()
        if user:
            p = PostService().like_post(post_id, user_id=user.id)
            return p
        return False

    @staticmethod
    def unlike_post(pub_id: str, post_id: int):
        user = User.query.filter(User.public_id == pub_id).first()
        if user:
            p = PostService().unlike_post(post_id, user_id=user.id)
            return p
        return False

    def get_user_id_by_token(self, token: str):
        u = self.check_token(token)
        if u is not False:
            return u.id

    @staticmethod
    def get_user_id_by_pubid(pub_id: str):
        u = User.query.filter(User.public_id == pub_id).first()
        return u.id
