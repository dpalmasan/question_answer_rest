from flask import request
from flask import g
from flask import Blueprint
from flask import json
from flask import Response
from ..shared.Authentication import Auth
from ..models.QuestionModel import QuestionModel
from ..models.QuestionModel import QuestionSchema

question_api = Blueprint('question_api', __name__)
question_schema = QuestionSchema()

@question_api.route('/', methods=['POST'])
@Auth.auth_required
def create():
    """
    Create Question Function
    """
    req_data = request.get_json()
    req_data['owner_id'] = g.user.get('id')
    data, error = question_schema.load(req_data)

    if error:
        return custom_response(error,400)

    post = QuestionModel(data)
    post.save()
    data = question_schema.dump(post).data
    return custom_response(data, 201)

@question_api.route('/<int:question_id>', methods=['PUT'])
@Auth.auth_required
def update(question_id):
    """
    Updates a Question
    """
    req_data = request.get_json()
    question = QuestionModel.get_one_question(question_id)

    if not question:
        return custom_response({'error': 'Question not found'}, 404)

    data = question_schema.dump(question).data

    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'permission denied'}, 400)

    data, error = question_schema.load(req_data, partial=True)

    if error:
        return custom_response(error, 400)

    question.update(data)

    data = question_schema.dump(question).data
    return custom_response(data, 200)

@question_api.route('/<int:question_id>', methods=['DELETE'])
@Auth.auth_required
def delete(question_id):
    """
    Delete a Question
    """
    question = QuestionModel.get_one_question(question_id)
    if not question:
        return custom_response({'error': 'Question not found'}, 404)

    data = question_schema.dump(question).data
    if data.get('owner_id') != g.user.get('id'):
        return custom_response({'error': 'Permission denied'}, 400)

    question.delete()
    return custom_response({'message': 'deleted'}, 204)


@question_api.route('/', methods=['GET'])
def get_all():
    """
    Get all questions
    """
    questions = QuestionModel.get_all_questions()
    data = question_schema.dump(questions, many=True).data
    return custom_response(data, 200)

@question_api.route('/<int:question_id>', methods=['GET'])
def get_one(question_id):
    """
    Gets a question by ID
    """
    question = QuestionModel.get_one_question(question_id)
    if not question:
        return custom_response({'error': 'Question not found'}, 404)
    data = question_schema.dump(question).data
    return custom_response(data, 200)


def custom_response(res, status_code):
    """
    Custom Response Function
    """
    return Response(
        mimetype="application/json",
        response=json.dumps(res),
        status=status_code
    )
