from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    title = StringField('Titolo', validators=[DataRequired()])
    body = TextAreaField('Post', validators=[DataRequired()])
    submit = SubmitField('Pubblica')


class CommentForm(FlaskForm):
    body = StringField('Commenta', validators=[DataRequired()])
    submit = SubmitField('Invia')

