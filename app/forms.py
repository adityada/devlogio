from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, SubmitField, TextAreaField, PasswordField, BooleanField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo
from flask_login import current_user
from app.routes import user
from app.models import User

class LogForm(FlaskForm):
    #game, title, log, submit
    if user is not None:
        game = SelectField(u'Select Game', default='', coerce=str, choices=[(game.game_name, game.game_name) for game in user.games])
        game.choices = [(game.game_name, game.game_name) for game in user.games]
        title = StringField('Title', validators=[DataRequired()])
        log = TextAreaField('Game log', validators=[DataRequired()])
        submit = SubmitField('Update')

class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    password_confirm = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if(user is not None):
            raise ValidationError("That username already exists")

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField("Remember me")
    submit = SubmitField("Sign in")
    
