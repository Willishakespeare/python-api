from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
import jwt
from werkzeug.security import generate_password_hash,check_password_hash
from bson import json_util

app = Flask(__name__)
app.config['MONGO_URI']='mongodb+srv://root:root@cluster0.b0qwy.azure.mongodb.net/pythonapimongodb?retryWrites=true&w=majority'
mongo = PyMongo(app)

@app.route('/api/user/register', methods=['POST'])
def create_user():
        # Create User
        email = request.json['email']
        password = request.json['password']
        fullname = request.json['fullname']
        country = request.json['country']
       

        if fullname and email and password and country:
            userExist = mongo.db.users.find_one({'email':email})
            if userExist:
                return {'menssage': 'The user has already been used'}
            else:
                hash_password = generate_password_hash(password)
                id = mongo.db.users.insert_one({
                    'email': email,
                    'password': hash_password,
                    'fullname': fullname,
                    'country': country,
                    'skills': []
                })
                jwt_encode = jwt.encode({'email': email,'password': hash_password,'fullname': fullname,'country': country,'skills':[]}, 'secret', algorithm='HS256')
                return jwt_encode
        else:
         return {'menssage': 'Please Send All Inputs'}    

@app.route('/api/user/login', methods=['POST'])
def login_user():
        # Create User
        email = request.json['email']
        password = request.json['password']
       

        if email and password :
            userExist = mongo.db.users.find_one({'email':email})
            if userExist:
                check_password = check_password_hash(userExist['password'],password)
                if check_password:
                    jwt_encode = jwt.encode({'email': userExist['email'],'password': userExist['password'],'fullname': userExist['fullname'],'country': userExist['country'],'skills':userExist['skills']}, 'secret', algorithm='HS256')
                    return jwt_encode
                else:
                    return "The password is incorrect"
            else:
                return {'menssage': 'The user not Exist'}
         
        else:
         return {'menssage': 'Please Send All Inputs'}    


@app.route('/api/user/auth', methods=['GET'])
def auth_user():
        # Auth User
        bearer = request.headers.get('bearer')
        if bearer:
            jwt_decode = jwt.decode(bearer, 'secret', algorithms=['HS256'])
            return jwt_decode
        else: 
            return {'menssage':'Incorrect Credencials'}
            

if __name__ == "__main__":
    app.run(debug=True)