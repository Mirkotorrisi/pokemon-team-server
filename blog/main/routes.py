from flask import render_template,redirect, request, Blueprint, abort
from blog.models import Post, Pokemon
from sqlalchemy import desc
from flask_login import current_user, login_required
from blog import db

main = Blueprint('main', __name__)


@main.route('/', methods=['POST'])
def post_with_app():
    if current_user.is_authenticated:
        post = Post(author=current_user)


        try:
            db.session.add(post)
            db.session.flush()
            pokemon1 = Pokemon(hp = request.json['pokemon1']['hp'], attack = request.json['pokemon1']['attack'],
            defense = request.json['pokemon1']['defense'],special_attack = request.json['pokemon1']['special_attack'],
            special_defense = request.json['pokemon1']['special_defense'],speed = request.json['pokemon1']['speed'],
            sprite = request.json['pokemon1']['sprite'],type1 = request.json['pokemon1']['type1'],type2 = request.json['pokemon1']['type2'],
            post_id="cristoleso")
        
            pokemon2 = Pokemon(hp = request.json['pokemon2']['hp'], attack = request.json['pokemon2']['attack'],
            defense = request.json['pokemon2']['defense'],special_attack = request.json['pokemon2']['special_attack'],
            special_defense = request.json['pokemon2']['special_defense'],speed = request.json['pokemon2']['speed'],
            sprite = request.json['pokemon2']['sprite'],type1 = request.json['pokemon2']['type1'],type2 = request.json['pokemon1']['type2'],post_id=post.id)
        
            pokemon3 = Pokemon(hp = request.json['pokemon3']['hp'], attack = request.json['pokemon3']['attack'],
            defense = request.json['pokemon3']['defense'],special_attack = request.json['pokemon3']['special_attack'],
            special_defense = request.json['pokemon3']['special_defense'],speed = request.json['pokemon3']['speed'],
            sprite = request.json['pokemon3']['sprite'],type1 = request.json['pokemon3']['type1'],type2 = request.json['pokemon1']['type2'],post_id=post.id)
            db.session.add(pokemon1)
            db.session.add(pokemon2)
            db.session.add(pokemon3)
            db.session.commit()
            return redirect('/')
        except Exception as e:
            return render_template('errors/500.html', error=str(e))
    else:
        abort(403)


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
