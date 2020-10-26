import json
from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity

from src.models.users import User

from src.utils.common_responses import *


class GetUserResource(Resource):
    @jwt_required
    def get(self, id):
        try:
            user = User.objects(id=id, active=True).first()
            if user is None:
                return error_404()

            response = user.serialize(excludes=['password'])
            return make_response(response, 200)
        except Exception as e:
            print(e)
            return error_500()


class GetUsersResource(Resource):
    @jwt_required
    def get(self):
        try:
            user_list = User.objects(active=True)
            if user_list is None:
                return error_404()

            users = []
            for user in user_list:
                users.append(user.serialize(excludes=['password']))

            print(users)
            response = jsonify(users)
            return make_response(response, 200)
        except Exception as e:
            print(e)
            return error_500()


class UpdateUserResource(Resource):
    @jwt_required
    def put(self, id):
        parser = reqparse.RequestParser()
        roles = ("Admin", "User")
        parser.add_argument('role', choices=roles, required=True, help='Invalid role!')
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        data = parser.parse_args()

        try:
            email = get_jwt_identity()
            session_user = User.objects(email=email).first()

            user = User.objects(id=id, active=True).first()
            if user is None:
                return error_404()

            user.first_name = data['first_name']
            user.last_name = data['last_name']
            user.role = data['role']
            user.updated_at = datetime.utcnow()
            user.save()

            response = user.serialize(excludes=['password'])
            return make_response(response, 200)

        except Exception as e:
            print(e)
            return error_500()


class DeleteUserResource(Resource):
    @jwt_required
    def delete(self, id):
        try:
            email = get_jwt_identity()
            session_user = User.objects(email=email).first()

            user = User.objects(id=id, active=True).first()
            if user is None:
                return error_404()

            user.active = False
            user.save()
            response = {'message': 'User deleted'}
            return make_response(response, 204)

        except Exception as e:
            print(e)
            return error_500()
