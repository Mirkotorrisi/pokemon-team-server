from flask import flash
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flask_login import current_user
from blog.models import User

def my_strip_filter(value):
    if value is not None and hasattr(value, 'strip'):
        return value.strip()
    return value
class MyBaseForm(FlaskForm):        
    class Meta:
        def bind_field(self, form, unbound_field, options):
            filters = unbound_field.kwargs.get('filters', [])
            if my_strip_filter not in filters:
                filters.append(my_strip_filter)
            return unbound_field.bind(form=form, filters=filters, **options)

class RegistrationForm(MyBaseForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[
                                     DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            flash('Username already in use', 'danger')
            raise ValidationError()

    def validate_email(self, email):
        email = User.query.filter_by(email=email.data).first()
        if email:
            flash('Email already in use', 'danger')
            raise ValidationError()


class LoginForm(MyBaseForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    remember = BooleanField('Stay logged ')
    submit = SubmitField('Log In')


class UpdateAccountForm(MyBaseForm):
    username = StringField('Username', validators=[
                           DataRequired(), Length(min=2, max=10)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField('Change Image', validators=[
                        FileAllowed(['jpg', 'png'])])
    submit = SubmitField('Update')

    def validate_username(self, username):
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                flash('Username already in use', 'danger')
                raise ValidationError()

    def validate_email(self, email):
        if email.data != current_user.email:
            email = User.query.filter_by(email=email.data).first()
            if email:
                flash('Email already in use', 'danger')
                raise ValidationError()


class RequestResetForm(MyBaseForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    submit = SubmitField('Reset Password', )

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is None:
            flash('No account linked to this email', 'danger')
            raise ValidationError()


class ResetPasswordForm(MyBaseForm):
    password = PasswordField('Password', validators=[
                             DataRequired(), Length(min=6)])
    conf_password = PasswordField('Confirm Password', validators=[
                                  DataRequired(), EqualTo('password')])
    submit = SubmitField('Reset Password')
