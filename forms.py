# forms.py - WTForms for validation

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SelectField, TextAreaField, DecimalField, IntegerField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional, EqualTo


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')


class RegisterForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email     = StringField('Email',     validators=[DataRequired(), Email()])
    username  = StringField('Username',  validators=[DataRequired(), Length(min=3, max=50)])
    password  = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm   = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    phone     = StringField('Phone', validators=[Optional(), Length(max=20)])
    address   = TextAreaField('Address', validators=[Optional()])


class ProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email     = StringField('Email',     validators=[DataRequired(), Email()])
    phone     = StringField('Phone',     validators=[Optional(), Length(max=20)])
    address   = TextAreaField('Address', validators=[Optional()])


class ProductForm(FlaskForm):
    product_name = StringField('Product Name', validators=[DataRequired(), Length(max=150)])
    description  = TextAreaField('Description', validators=[Optional()])
    price        = DecimalField('Price', validators=[DataRequired(), NumberRange(min=0.01)])
    stock        = IntegerField('Stock',  validators=[DataRequired(), NumberRange(min=0)])
    image_url    = StringField('Image URL', validators=[Optional()])
    category_id  = SelectField('Category', coerce=int, validators=[DataRequired()])
    brand_id     = SelectField('Brand',    coerce=int, validators=[DataRequired()])
    is_active    = BooleanField('Active', default=True)


class CategoryForm(FlaskForm):
    category_name = StringField('Category Name', validators=[DataRequired(), Length(max=100)])
    description   = TextAreaField('Description', validators=[Optional()])


class BrandForm(FlaskForm):
    brand_name = StringField('Brand Name', validators=[DataRequired(), Length(max=100)])
    country    = StringField('Country',    validators=[Optional(), Length(max=50)])


class ReviewForm(FlaskForm):
    rating  = SelectField('Rating', coerce=int, choices=[(1,'1'),(2,'2'),(3,'3'),(4,'4'),(5,'5')], validators=[DataRequired()])
    comment = TextAreaField('Comment', validators=[Optional()])


class CheckoutForm(FlaskForm):
    shipping_address = TextAreaField('Shipping Address', validators=[DataRequired()])
    method_id        = SelectField('Payment Method', coerce=int, validators=[DataRequired()])


class AddManagerForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email     = StringField('Email',     validators=[DataRequired(), Email()])
    username  = StringField('Username',  validators=[DataRequired(), Length(min=3, max=50)])
    password  = PasswordField('Password', validators=[DataRequired(), Length(min=6)])


class DiscountForm(FlaskForm):
    discount_name    = StringField('Discount Name',    validators=[DataRequired()])
    discount_percent = DecimalField('Discount %',      validators=[DataRequired(), NumberRange(min=0.01, max=100)])
    is_active        = BooleanField('Active', default=True)
