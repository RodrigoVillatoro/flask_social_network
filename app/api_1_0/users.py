from flask import current_app, jsonify, request, url_for
from . import api
from ..models import Post, User


@api.route('/users/<int:id>')
def get_user(id):
    user = User.query.get_or_404(id)
    return jsonify(user.to_json())


@api.route('/users/<int:id>/posts/')
def get_user_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.posts.order_by(Post.timestamp.desc()).paginate(
        page,
        per_page=current_app.config['APP_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    prev_page = None
    if pagination.has_prev:
        prev_page = url_for('api.get_posts', page=page-1, _external=True)
    next_page = None
    if pagination.has_next:
        next_page = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev_page,
        'next': next_page,
        'count': pagination.total
    })


@api.route('/users/<int:id>/timeline/')
def get_user_followed_posts(id):
    user = User.query.get_or_404(id)
    page = request.args.get('page', 1, type=int)
    pagination = user.followed_posts.order_by(Post.timestamp.desc()).paginate(
        page,
        per_page=current_app.config['APP_POSTS_PER_PAGE'],
        error_out=False
    )
    posts = pagination.items
    prev_page = None
    if pagination.has_prev:
        prev_page = url_for('api.get_posts', page=page-1, _external=True)
    next_page = None
    if pagination.has_next:
        next_page = url_for('api.get_posts', page=page+1, _external=True)
    return jsonify({
        'posts': [post.to_json() for post in posts],
        'prev': prev_page,
        'next': next_page,
        'count': pagination.total
    })