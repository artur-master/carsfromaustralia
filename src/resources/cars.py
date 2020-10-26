import json
from flask import make_response, jsonify
from flask_restful import Resource, reqparse
from flask_jwt_extended import jwt_required, jwt_refresh_token_required, get_jwt_identity

from src.models.cars import Car

from src.utils.common_responses import *


class GetCarResource(Resource):
    # @jwt_required
    def get(self, id):
        try:
            car = Car.objects(id=id).first()
            if car is None:
                return error_404()

            response = car.serialize(excludes=[])
            return make_response(response, 200)
        except Exception as e:
            print(e)
            return error_500()


class GetCarsResource(Resource):
    # @jwt_required
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('PageSize', type=int, location='args')
        parser.add_argument('Offset', type=int, location='args')
        data = parser.parse_args()

        page_size = data['PageSize']
        offset = data['Offset']

        try:
            car_list = Car.objects()
            if car_list is None:
                return error_404()

            cars = []
            for car in car_list:
                item = car.serialize(excludes=[
                    'description', 'contact', 'advKms', 'ancap', 'build_year', 'engneNo', 'features', 'induction',
                    'gear', 'redbookCode', 'rego', 'regoExpiry', 'series', 'variant', 'vin', 'wovr', 'builtDate',
                    'compliance'
                ])
                item['image'] = item['images'][0] if len(item['images']) > 0 else None
                del item['images']

                cars.append(item)

            if page_size is None and offset is None:
                response = jsonify(cars)
            elif page_size is not None and offset is not None:
                response = jsonify(cars[offset:offset + page_size])
            else:
                return error_400("Both page size and offset required!")

            return make_response(response, 200)
        except Exception as e:
            print(e)
            return error_500()
