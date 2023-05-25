from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DecimalRangeField,PasswordField,BooleanField
from wtforms.validators import DataRequired, NumberRange, Email, Length, EqualTo

class SettingsForm(FlaskForm):
    api_key = StringField('API Key', validators=[DataRequired()])
    temperature = DecimalRangeField('Temperature:', validators=[NumberRange(min=0.10, max=1.00)], default=0.70)
    setting = StringField('Setting / Story Locations')
    save_button = SubmitField('Save')

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')