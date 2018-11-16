from flask import Flask, render_template, flash, url_for, redirect
from app import app, db

from app.models import User, Post, Game

# Dummy Data
user = User(username="Admin123", hashed_password="BDHSAHDSAGD62183918")
user.set_password('password123')
db.session.add(user)
db.session.commit()
admin = User.query.filter_by(username="Admin123").first()
game1 = Game(game_name="Rails of the Dead", creator=admin)
game2 = Game(game_name="Zoinks 2", creator=admin)
db.session.add(game1)
db.session.add(game2)
db.session.commit()

def getCurrentUser():
    return admin

from app.forms import LogForm, LoginForm


@app.route("/", methods=['GET', 'POST'])
def index():
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
    form = LoginForm()
    if form.validate_on_submit():
        flash(f"Login requested for user {form.username.data}, remember_me={form.remember_me.data}")
        return redirect("/")
        print("FORM VALIDATED")
    print(form.errors)
    return render_template("login.html", form=form)