from mongoengine import ValidationError, EmailField, DynamicDocument, StringField
from database.db_connection import client_orm


def validate_username(username):
    if Users.objects(username=username):
        raise ValidationError


def validate_password(password):
    allowed_symbols = ['!', '@', '#', '$', '%', '^', '&', '*']
    if not any(char.isdigit() for char in password):
        raise ValidationError
    if not any(char.isupper() for char in password):
        raise ValidationError
    if not any(char.islower() for char in password):
        raise ValidationError
    if not any(char in allowed_symbols for char in password):
        raise ValidationError


class Users(DynamicDocument):
    username = EmailField(min_length=5, max_length=30, required=True, validation=validate_username),
    password = StringField(min_length=8, max_length=20, required=True, validation=validate_password)
