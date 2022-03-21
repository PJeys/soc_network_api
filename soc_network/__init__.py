from flask import Flask, jsonify, request, make_response
from soc_network.config import Config
from soc_network.models import init_DB
from soc_network.sevices.user_actions_service import UserActionService
from soc_network.sevices.user_service import UserService
from soc_network.sevices.post_service import PostService
from soc_network.sevices.user_actions_service import UserActionService
from functools import wraps
from datetime import datetime


def create_app(test_config=None):
    app = Flask('soc_network')

    app.config.from_object(Config())
    if test_config:
        app.config.update(test_config)

    init_DB(app)

    return app


application = create_app()


def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None
        # jwt is passed in the request header
        if 'x-access-token' in request.headers:
            token = request.headers['x-access-token']
        if not token:
            return jsonify({'message': 'Token is missing !!'}), 401

        u = UserService().check_token(token)
        if not u:
            return jsonify({
                'message': 'Token is invalid !!'
            }), 401
        return f(u, *args, **kwargs)

    return decorated


@application.post('/api/register')
def register():
    data = request.args
    email, password = data.get('email'), data.get('password')
    print(data)
    u = UserService().register(email, password)
    if u == 0:
        return jsonify({'message': 'User already registered. Login, please'}), 200
    if u == -1:
        return jsonify({'registration error': 'Invalid email.'}), 403
    if u == -2:
        return jsonify({'registration error': 'Invalid password. Length must be between 6 and 18 symbols'}), 403
    return jsonify({'message':'Successfully registered'}), 201


@application.post('/api/login')
def login():
    auth = request.args
    resp = UserService().login(auth.get('email'), auth.get('password'))
    if not resp:
        return make_response(jsonify({'auth error': 'Could not verify'}), 403)
    return make_response(jsonify({'token': resp}), 201)


@application.post('/api/create_post')
@token_required
def create_post(user):
    args = request.args
    text, media = args.get('text'), args.get('media')
    if not text:
        return jsonify({'error': 'no text provided'}), 403
    user_id = user.id
    post = PostService().create_post(user_id, text, media)
    if not post:
        return make_response(jsonify({'error': 'Invalid text length'}), 403)
    return jsonify({'message': 'Post created successfully'}), 200


@application.post('/api/like_post')
@token_required
def like_post(user):
    args = request.args
    post_id = args.get('post_id')
    act = PostService().like_post(post_id, user.id)
    if not act:
        return make_response(jsonify({'message': 'Error! This post does not exist'}), 403)
    return jsonify({'message': 'Successfully liked a post'}), 200


@application.post('/api/unlike_post')
@token_required
def unlike_post(user):
    args = request.args
    post_id = args.get('post_id')
    act = PostService().unlike_post(post_id, user.id)
    if not act:
        return make_response(jsonify({'message': 'Error! This post does not exist'}), 403)
    return jsonify({'message': 'Successfully unliked a post'}), 200


@application.get('/api/like_stats')
@token_required
def like_stats(user):
    args = request.args
    date_from, date_to = args.get('date_from'), args.get('date_to')
    if date_to and date_from:
        date_from_dt = datetime.strptime(date_from, '%Y-%m-%d')
        date_to_dt = datetime.strptime(date_to, '%Y-%m-%d')
        likes = PostService().get_like_stats(date_from_dt, date_to_dt)
        return jsonify({'like_number': likes}), 200
    return jsonify({'error': 'Provide date from and date to to get the analytics'}), 403


@application.get('/api/user_stats')
@token_required
def user_stats(user):
    args = request.args
    public_user_id = args.get('user_id')
    if not public_user_id:
        return jsonify({'error': 'Provide user public id'}), 403
    user_id = UserService().get_user_id_by_pubid(public_user_id)
    last_login = UserActionService().get_last_login(user_id)
    last_req = UserActionService().get_last_login(user_id)
    return jsonify({'last_login': last_login, 'last_request':last_req}), 200
