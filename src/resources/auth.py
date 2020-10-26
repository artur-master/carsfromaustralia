import uuid
import json
from datetime import datetime
from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, jwt_refresh_token_required, \
    get_jwt_identity, get_raw_jwt
from src.models.users import User
from src.models.revoked_tokens import RevokedToken

from src.utils.hash import generate_hash, verify_hash

from src.utils.common_responses import *


class SignUpResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='Email required!')
        parser.add_argument('password', required=True, help='Password required!')
        roles = ("Admin", "User")
        parser.add_argument('role', choices=roles, required=True, help='Invalid role!')
        parser.add_argument('first_name')
        parser.add_argument('last_name')
        data = parser.parse_args()

        try:
            user = User.objects(email=data['email']).first()
            if user is not None:
                return error_409("User already exist!")

            user = User(
                email=data['email'],
                password=generate_hash(data['password']),
                role=data['role'],
                first_name=data['first_name'],
                last_name=data['last_name'],
                verified=False,

                active=True,
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow()
            )
            user.save()
            response = {
                'access_token': create_access_token(identity=data['email']),
                'refresh_token': create_refresh_token(identity=data['email'])
            }
            return make_response(response, 201)
        except Exception as e:
            print(e)
            return error_500()


class SignInResource(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help='Email required!')
        parser.add_argument('password', required=True, help='Password required!')
        data = parser.parse_args()

        try:
            user = User.objects(email=data['email']).first()
            if user is None:
                return error_404("User not found!")

            if verify_hash(data['password'], user.password):
                response = {
                    'access_token': create_access_token(identity=data['email']),
                    'refresh_token': create_refresh_token(identity=data['email'])
                }
                return make_response(response, 200)
            else:
                return error_400("Invalid password!")
        except Exception as e:
            print(e)
            return error_500()


class SignOutResource(Resource):
    @jwt_required
    def post(self):
        jti = get_raw_jwt()['jti']
        try:
            revoked_token = RevokedToken(jti=jti)
            revoked_token.save()
            response = {'message': 'Token revoked'}
            return make_response(response, 204)
        except Exception as e:
            print(e)
            return error_500()


class TokenRefreshResource(Resource):
    @jwt_refresh_token_required
    def post(self):
        try:
            email = get_jwt_identity()
            response = {
                'access_token': create_access_token(identity=email),
                'refresh_token': create_refresh_token(identity=email)
            }
            return make_response(response, 200)
        except Exception as e:
            print(e)
            return error_500()
