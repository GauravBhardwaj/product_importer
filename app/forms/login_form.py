from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class ProductForm(FlaskForm):
    product_name = StringField('Name')
    product_sku = StringField('SKU')
    product_description = StringField('Description')
    product_is_active = BooleanField('Active')
    create = SubmitField('Create Product')