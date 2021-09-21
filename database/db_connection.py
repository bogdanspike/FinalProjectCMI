import os
import urllib.parse
from mongoengine import connect

client_orm = connect(
    host="mongodb+srv://"+os.environ['username']+":" + urllib.parse.quote(
        os.environ['password']) + "@cluster0.xqv3e.mongodb.net/main_db?retryWrites=true&w=majority")
