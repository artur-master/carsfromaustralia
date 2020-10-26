import json
from datetime import datetime
from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity

from src.models.users import User

from src.utils.common_responses import *


class GetProfileResource(Resource):
    @jwt_required
    def get(self):
        email = get_jwt_identity()
        try:
            user = User.objects(email=email).first()
            if user is None:
                return error_404()

            response = user.serialize(excludes=['password'])
            return make_response(response, 200)
        except Exception as e:
            print(e)
            return error_500()


class UpdateProfileResource(Resource):
    @jwt_required
    def put(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email')
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        data = parser.parse_args()

        try:
            email = get_jwt_identity()
            session_user = User.objects(email=email).first()

            if email == data['email']:
                session_user.update(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    updated_at=datetime.utcnow()
                )
            else:
                user = User.objects(email=data['email']).first()
                if user is not None:
                    return error_409("Email already exist!")

                session_user.update(
                    email=data['email'],
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    updated_at=datetime.utcnow()
                )

            user = User.objects(email=data['email']).first()
            response = user.serialize(excludes=['password'])
            return make_response(response, 200)

        except Exception as e:
            print(e)
            return error_500()
