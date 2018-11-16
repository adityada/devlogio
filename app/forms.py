from flask_wtf import FlaskForm
from app.routes import getCurrentUser
from wtforms import SelectField, StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired

class LogForm(FlaskForm):
    #game, title, log, submit
    game = SelectField(u'Select Game', default='', coerce=str, choices=[(game.game_name, game.game_name) for game in getCurrentUser().games])
    game.choices = [(game.game_name, game.game_name) for game in getCurrentUser().games]
    title = StringField('Title', validators=[DataRequired()])
    log = TextAreaField('Game log', validators=[DataRequired()])
    submit = SubmitField('Update')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")
