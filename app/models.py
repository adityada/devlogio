from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login 

@login.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    hashed_password = db.Column(db.String(128))
    games = db.relationship('Game', backref='creator', lazy=True)

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def __repr__(self):
        return f'<User {self.username}>'
    
class Game(db.Model):
    __tablename__ = "Game"
    id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'))
    posts = db.relationship('Post', backref='game', lazy=True)

    def __repr__(self):
        return f'<Game {self.game_name}>'

class Post(db.Model):
    __tablename__ = "Post"
    id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('Game.id'))
    title = db.Column(db.String(128))
    date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    log = db.Column(db.String())

    def __repr__(self):
        return f'<Post {self.title}>'

db.create_all()
