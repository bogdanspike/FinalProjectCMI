from mongoengine import DynamicDocument, StringField
from database.db_connection import client_orm


class Chat(DynamicDocument):
    pass