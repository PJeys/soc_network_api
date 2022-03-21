from soc_network.models.user_action import UserAction
from soc_network.models import db
from sqlalchemy import func


class UserActionService:
    def get_last_login(self, user_id):
        date = db.session.query(func.max(UserAction.action_date)).filter(
            UserAction.action == 'login', UserAction.user_id == user_id).first()[0]
        self.add_action(user_id, 'login')
        return date

    def get_last_request(self, user_id):
        date = db.session.query(func.max(UserAction.action_date)).filter(
            UserAction.action == 'req', UserAction.user_id == user_id).first()[0]
        self.add_action(user_id, 'req')
        return date

    def add_action(self, user_id, action):
        us_act = UserAction(user_id=user_id, action=action)
        db.session.add(us_act)
        db.session.commit()
