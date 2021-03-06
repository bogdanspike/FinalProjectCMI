import json

import flask
from PIL import Image
from bson import json_util
from certifi.__main__ import args
from flask import Flask, request, jsonify
from flask_restful import Resource, Api

from models.users import Users
from models.leads import Leads
from models.message import Message

app = Flask(__name__)
api = Api(app)


class Home(Resource):
    def get(self):
        return 'This is your homepage'


class Register(Resource):
    def post(self):
        try:
            username = request.form.get('username').lower()
            password = request.form.get('password')
            if not Users.objects(username=username):
                Users(username=username, password=password).save()
                return 'Success', 200
            else:
                return 'Username already existent', 200
        except Exception as e:
            if 'username' and 'password' in str(e):
                return 'There was a problem with both username and password', 500
            if 'password' in str(e):
                return 'There was a problem with password', 500
            if 'username' in str(e):
                return 'There was a problem with username', 500
            return f':{e}', 500


class Login(Resource):
    def post(self):
        try:
            username = request.form.get('username').lower()
            password = request.form.get('password')
            if Users.objects.get(username=username, password=password):
                return 'Success', 200
        except Exception as e:
            if 'Users matching query does not exist' in str(e):
                return 'Invalid username and password combination', 500


class ChangePassword(Resource):
    def patch(self):
        try:
            username = request.form.get('username').lower()
            password = request.form.get('password')
            new_password = request.form.get('new_password')
            conf_new_password = request.form.get('conf_new_password')
            if Users.objects.get(username=username, password=password) and new_password == conf_new_password:
                Users.objects(username=username, password=password).update(password=new_password)
                return 'Success', 200
        except Exception as e:
            if 'username' and 'password' in str(e):
                return 'There was a problem with both username and password', 500
            if 'password' in str(e):
                return 'There was a problem with your password', 500
            if 'username' in str(e):
                return 'There was a problem with your username', 500


class LeadsResource(Resource):
    def get(self):
        username = request.args.get("username")
        retrieved_photo = Leads.objects(username=username).first()
        # x = retrieved_photo.image.read()
        # with open('plm.png', 'wb') as img:
        #     img.write(x)
        print(retrieved_photo.username)
        return retrieved_photo, 200

    # not done
    # TODO: get must contain all leads for an user

    def post(self):
        try:
            username = request.form.get('username')
            name = request.form.get('name')
            image = request.files['image']
            type = request.form.get('type')
            new_lead = Leads(username=username, name=name, type=type)
            my_image = image
            new_lead.image.replace(my_image)
            new_lead.save()
            return 'Success', 200
        except Exception as e:
            return f':{e}', 500


class LeadsAndSales(Resource):
    def get(self):
        return 'This is the page for Leads&Sales'


class ChatHistory(Resource):
    def get(self):
        sender = request.args.get("sender")
        receiver = request.args.get("receiver")
        conv_id = sender + receiver
        list_of_msg = Message.objects(conv_id=conv_id).scalar('message', 'sender', 'receiver')
        msg_to_json = [json.loads(Message(message=obj[0], sender=obj[1], receiver=obj[2]).to_json()) for obj in
                       list_of_msg]
        return {'result': msg_to_json}, 200

    def post(self):
        try:
            sender = request.form.get('sender')
            receiver = request.form.get('receiver')
            message = request.form.get('message')
            # TODO: transform this into a hash
            conv_id = sender + receiver
            messages = Message.objects(conv_id=conv_id)
            if not messages:
                Message(sender=sender, receiver=receiver, message=message, conv_id=conv_id, msg_number=1).save()
            else:
                msg_number = messages[len(messages) - 1].msg_number + 1
                Message(sender=sender, receiver=receiver, message=message, conv_id=conv_id,
                        msg_number=msg_number).save()
            return 'Success', 200
        except Exception as e:
            return f':{e}', 500


api.add_resource(Home, '/home')
api.add_resource(Register, '/register')
api.add_resource(Login, '/login')
api.add_resource(ChangePassword, '/changepw')
api.add_resource(LeadsResource, '/leads')
api.add_resource(LeadsAndSales, '/leads_and_sales')
api.add_resource(ChatHistory, '/chat')

if __name__ == '__main__':
    app.run()
