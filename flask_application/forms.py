from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import Email, DataRequired, Length, EqualTo


class FormLogin(FlaskForm):
    email = StringField('Email ', validators=[Email(message='Wrong email format')], render_kw={"placeholder": "Email"})
    password = PasswordField('Password ',
                             validators=[DataRequired(), Length(min=4, max=32)],
                             render_kw={"placeholder": "Password"})
    remember = BooleanField('Remain me', default=False)
    submit = SubmitField('Log in')


class FormRegister(FlaskForm):
    name = StringField('Name ', validators=[Length(min=2, max=32, message='Wrong name format')],
                       render_kw={"placeholder": "Name"})
    email = StringField('Email ', validators=[Email(message='Wrong email format')], render_kw={"placeholder": "Email"})
    password = PasswordField('Password ',
                             validators=[DataRequired(), Length(min=4, max=32)],
                             render_kw={"placeholder": "Password"})
    password2 = PasswordField('Repeat password ',
                              validators=[DataRequired(), EqualTo('password', message='Passwords did not match')],
                              render_kw={"placeholder": "Repeat password"})
    submit = SubmitField('Sign up')
