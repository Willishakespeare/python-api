from flask import Flask, request, jsonify, Response
from flask_pymongo import PyMongo
import jwt
from werkzeug.security import generate_password_hash,check_password_hash
from bson import json_util
from bson.objectid import ObjectId

app = Flask(__name__)
app.config['MONGO_URI']='urlMongo'
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
                jwt_encode = jwt.encode({'id':str(id),'email': email,'password': hash_password,'fullname': fullname,'country': country,'skills':[]}, 'secret', algorithm='HS256')
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
                    jwt_encode = jwt.encode({'id': str(userExist['_id']),'email': userExist['email'],'password': userExist['password'],'fullname': userExist['fullname'],'country': userExist['country'],'skills':userExist['skills']}, 'secret', algorithm='HS256')
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
            
@app.route('/api/skills/register', methods=['POST'])
def create_skill():
        # Auth User
        bearer = request.headers.get('bearer')
        if bearer:
            jwt_decode = jwt.decode(bearer, 'secret', algorithms=['HS256'])
            if jwt_decode:
                skill = request.json['skill']
                skillExist = mongo.db.skills.find_one({'name':skill})
                if skillExist:
                    return {'menssage': 'Skill Exist'}
                else:
                    mongo.db.skills.insert_one({
                    'name': skill
                })
                    return {'menssage': 'Skill Agreed'}
            else:
                 return {'menssage':'You Need are Logged'}
        else: 
            return {'menssage':'Incorrect Credencials'}

@app.route('/api/skills', methods=['GET'])
def get_skills():
        # Auth User
        bearer = request.headers.get('bearer')
        if bearer:
            jwt_decode = jwt.decode(bearer, 'secret', algorithms=['HS256'])
            if jwt_decode:
                skills = mongo.db.skills.find()
                response = json_util.dumps(skills)
                return Response(response, mimetype='application/json')
            else:
                 return {'menssage':'You Need are Logged'}
        else: 
            return {'menssage':'Incorrect Credencials'}
@app.route('/api/user/skills', methods=['POST'])
def addSkill_user():
        # Auth User
        bearer = request.headers.get('bearer')
        if bearer:
            jwt_decode = jwt.decode(bearer, 'secret', algorithms=['HS256'])
            if jwt_decode:
                idUser = request.json['id']
                skill = request.json['skill']
                skillExist = mongo.db.skills.find_one({'name':skill})
                if skillExist: 
                   userExist = mongo.db.users.find_one({'_id': ObjectId(idUser)})
                   tempSkillsUser = userExist['skills']
                   existSkillUser = False
                   for item in tempSkillsUser:
                       if item['name'] == skill:
                           existSkillUser = True
                   if existSkillUser:
                       return {'menssage':'You already have that skill'}
                   else:
                        tempSkillsUser.append({'name': skill})
                        userUpdate = mongo.db.users.find_one_and_update({'_id': ObjectId(idUser)},{"$set":{'skills': tempSkillsUser}},upsert=True)
                        response = json_util.dumps(userUpdate)
                        print(tempSkillsUser)
                        return {'menssage':'Added Skill User','data': response} 
                else:
                    return {'menssage':'Skill not Exist'}
        else: 
            return {'menssage':'Incorrect Credencials'}

if __name__ == "__main__":
    app.run(debug=True)
