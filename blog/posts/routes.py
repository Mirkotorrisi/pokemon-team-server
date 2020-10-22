from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from blog import db
from blog.models import Post, Comment
from blog.posts.forms import PostForm, CommentForm

posts = Blueprint('posts', __name__)


@posts.route('/post/<int:post_id>', methods=['GET', 'POST'])
def post(post_id):
    post = Post.query.get_or_404(post_id)
    form = CommentForm()
    if form.validate_on_submit():
        comment = Comment(content=form.body.data,
                          author=current_user.username, post_id=post.id)
        db.session.add(comment)
        db.session.commit()
        flash('Comment published', 'success')
        return redirect(url_for('posts.post', post_id=post.id, comments=post.comments))
    return render_template('post.html', pokemons=post.pokemons, post=post, form=form, comments=post.comments, legend="Comments")


@posts.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted', 'info')
    return redirect(url_for('main.index'))
