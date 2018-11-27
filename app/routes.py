from flask import Flask, render_template, flash, url_for, redirect, request
from app import app, db
from flask_login import current_user, login_user, login_required

from app.models import User, Post, Game
user = current_user;

# This is the index route - the main page, which includes posts and the WriteLog form
# Since this page shows posts from creators the user follows, users need to log in or sign up beforehand. 
@app.route("/", methods=['GET', 'POST'])
@login_required
def index():
    if current_user.is_authenticated:
        user = current_user
        from app.forms import LogForm
        form = LogForm()
    posts = Post.query.all()
    posts = list(reversed(posts))
    # If post is validated
    if form.validate_on_submit():
        # Take the data of the forms and append it to the posts list
        post = Post(game_id=Game.query.filter_by(game_name=form.game.data).first().id, title=form.title.data, log=form.log.data)
        db.session.add(post)
        db.session.commit()
        # Insert post object above to the beginning of posts list. 
        return render_template("index.html", form=form, posts=posts, game=Game)
    return render_template("index.html", form=form, posts=posts, game=Game)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        user = current_user
        return redirect(url_for("index"))
    else:
        user = None
    from app.forms import LoginForm
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        # If the user does not exist, or password is incorrect
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        # Set next_page to the route the user was directed from
        next_page = request.args.get('next')
        # If the user isn't redirected to the login route from other routes, go back to index.
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template("login.html", form=form)

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        user = current_user
        return redirect(url_for("index"))
    else:
        user = None
    from app.forms import RegisterForm
    form = RegisterForm(request.form)
    if form.validate_on_submit():
        user = User(username = form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations! You have sucessfuly registered to this site.')
        return redirect(url_for('login'))
    flash(form.errors)
    print("something failed " + request.method)
    return render_template("register.html", form=form)
