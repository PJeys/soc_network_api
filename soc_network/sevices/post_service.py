from soc_network.models.post import Post, db
from soc_network.models.post_action import PostAction
from soc_network.sevices.user_actions_service import UserActionService


class PostService:
    def create_post(self, author_id, text, media=None):
        if len(text) >= 255:
            return False
        post = Post(author_id=author_id, post_text=text, media_ref=media)
        db.session.add(post)
        db.session.commit()
        UserActionService().add_action(author_id, 'req')
        return True

    def is_post_liked(self, user_id, post_id):
        act = PostAction().query.filter(PostAction.user_id == user_id, PostAction.post_id == post_id).first()
        if act:
            return True
        return False

    def like_post(self, post_id, user_id):
        post = Post.query.filter(Post.id == post_id).first()
        if self.is_post_liked(user_id, post_id):
            return True
        if post:
            post.likes += 1
            db.session.commit()
            self.add_action(post_id, user_id, 'like')
            UserActionService().add_action(user_id, 'req')
            return True
        return False

    def remove_like(self, post_id, user_id):
        act = PostAction().query.filter(PostAction.post_id == post_id, PostAction.user_id == user_id).first()
        db.session.delete(act)
        db.session.commit()

    def unlike_post(self, post_id, user_id):
        post = Post.query.filter(Post.id == post_id).first()
        if not self.is_post_liked(user_id, post_id):
            return False
        if post:
            post.likes -= 1
            db.session.commit()
            self.remove_like(post_id, user_id)
            UserActionService().add_action(user_id, 'req')
            return True
        return False

    def add_action(self, post_id, user_id, action):
        act = PostAction(action=action, post_id=post_id, user_id=user_id)
        db.session.add(act)
        db.session.commit()

    def get_like_stats(self, date_from, date_to):
        num = PostAction.query.filter(PostAction.date_of_action.between(date_from, date_to)).count()
        return num
