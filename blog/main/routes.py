from flask import render_template,redirect, request, Blueprint
from blog.models import Post
from sqlalchemy import desc
from flask_login import current_user, login_required
from blog import db

main = Blueprint('main', __name__)


@main.route('/', methods=['POST'])
@login_required
def post_with_app():
    if request.method == 'POST':
        pokemon1 = request.json['pokemon1']
        pokemon2 = request.json['pokemon2']
        pokemon3 = request.json['pokemon3']
        new_pokemon = Post(pokemon1=pokemon1, pokemon2=pokemon2,
                           pokemon3=pokemon3, author=current_user)

        try:
            db.session.add(new_pokemon)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return str(e)
    else:
        page = request.args.get('page', 1, type=int)
        posts = Post.query.order_by(
            Post.date_posted.desc()).paginate(page=page, per_page=5)
        return render_template('index.html', title="Home", posts=posts)

@main.route('/', methods=['GET'])
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(
    Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('index.html', title="Home", posts=posts)


@main.route('/about')
def about():
    return render_template('about.html', title="About")


@main.route('/top')
def top_posts():
    posts = Post.query.all()
    top_posts = []
    for i in range(3):
        top = max(post.likes.count() for post in posts)
        for post in posts:
            if post.likes.count() >= top:
                top_posts.append(post)
                posts.remove(post)

    return render_template('top.html', title="Top", posts=top_posts)


@main.route('/most_commented')
def most_commented():
    posts = Post.query.all()

    top_posts = []
    for i in range(3):
        top = max(post.comments.count() for post in posts)
        for post in posts:
            print(post)
            if post.comments.count() >= top:
                top_posts.append(post)
                posts.remove(post)

    return render_template('top.html', title="Top", posts=top_posts)
