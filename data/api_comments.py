import flask

from flask import jsonify
from . import db_session
from .comments import Comments
from flask import make_response, request

blueprint = flask.Blueprint(
    'news_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/v2/comments')
def get_comments():
    db_sess = db_session.create_session()
    comments = db_sess.query(Comments).all()
    return jsonify(
        {
            'comments':
                [item.to_dict(only=('title', 'content', 'user.name'))
                 for item in comments]
        }
    )

@blueprint.route('/api/v2/comments/<int:comments_id>', methods=['GET'])
def get_one_comment(comments_id):
    db_sess = db_session.create_session()
    if isinstance(comments_id, int):
        comments = db_sess.query(Comments).get(comments_id)
        if not comments:
            return make_response(jsonify({'error': 'Not found'}), 404)
        return jsonify(
            {
                'comments': comments.to_dict(only=(
                    'title', 'content', 'user.name'))
            }
        )
    return make_response(jsonify({'error': 'Not found'}), 404)

@blueprint.route('/api/v2/comments', methods=['POST'])
def create_comments():
    if not request.json:
        return make_response(jsonify({'error': 'Empty request'}), 400)
    elif not all(key in request.json for key in
                 ['title', 'content', 'user_id']):
        return make_response(jsonify({'error': 'Bad request'}), 400)
    db_sess = db_session.create_session()
    comments = Comments(
        title=request.json['title'],
        content=request.json['content'],
        user_id=request.json['user_id']
    )
    db_sess.add(comments)
    db_sess.commit()
    return jsonify({'id': comments.id})

