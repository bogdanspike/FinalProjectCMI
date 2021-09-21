from mongoengine import DynamicDocument, StringField, EmailField, IntField
from database.db_connection import client_orm
from models.users import validate_username


class Message(DynamicDocument):
    conv_id: StringField()
    sender: EmailField(min_length=5, max_length=30, required=True)
    receiver: EmailField(min_length=5, max_length=30, required=True)
    message: StringField(min_length=1, max_length=100, required=True)
    msg_number: IntField()