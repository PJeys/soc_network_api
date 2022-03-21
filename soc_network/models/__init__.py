from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
# flake8: noqa
db = SQLAlchemy()
migrate = Migrate()


def init_DB(app):
    db.init_app(app)
    with app.app_context():
        if db.engine.url.drivername == 'sqlite':
            migrate.init_app(app, db, render_as_batch=True)
        else:
            migrate.init_app(app, db)


from soc_network.models.post import Post
from soc_network.models.user import User
from soc_network.models.post_action import PostAction
from soc_network.models.user_action import UserAction
