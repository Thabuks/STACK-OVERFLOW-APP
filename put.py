from flask import Flask, request
from flask_restful import Resource, Api
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app= Flask(__name__)
app.secret_key='Thabuks'
api= Api(app)
jwt = JWT(app, authenticate, identity)

questions=[]

class Questions(Resource):
    @jwt_required()
    def get(self, name):
        question= next(filter(lambda x: x['name'] == name, questions), None)
        return {'question':question}, 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, questions), None):
            return{'message': "An question with name '{}' already exists".format(name)}, 400
        data= request.get_json()
        question= {'name':name, 'science': data['Science']}
        questions.append(question)
        return question, 201

    @jwt_required()
    def delete(self, name):
        pass

    def put(self, name):
        data= request.get_json()
        question= next(filter(lambda x: x['name'] == name, questions), None)
        if question is None:
            question = {'name': name, 'science': data['Science']}
            questions.append(question)
        else:
            question.update(data)
        return question

class QuestionList(Resource):
    pass

api.add_resource(Questions, '/question/<string:name>')
api.add_resource(QuestionList, '/questions')
if __name__ == '__main__':
    app.run(debug=True)
