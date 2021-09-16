import urllib.parse
from mongoengine import connect

client_orm = connect(
    host="mongodb+srv://username:" + urllib.parse.quote(
        'password') + "@cluster0.xqv3e.mongodb.net/main_db?retryWrites=true&w=majority")
