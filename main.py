import os
import requests
from flask import Flask, json, request, jsonify, Response
from flask_restful import Api, Resource, reqparse

from dotenv import load_dotenv

app = Flask(__name__)
api = Api(app)

load_dotenv(verbose=True)

headers = {
    "X-NCP-APIGW-API-KEY-ID":os.environ.get("NCLOUD_MAP_CLIENT_ID"),
    "X-NCP-APIGW-API-KEY":os.environ.get("NCLOUD_MAP_CLIENT_SECRET")
}

class Routes(Resource):
    def get(self):
        parse = reqparse.RequestParser()
        parse.add_argument('start', required=True)
        parse.add_argument('goal', required=True)
        args = parse.parse_args()
        start = args['start']
        goal = args['goal']
        r = requests.get(f'https://naveropenapi.apigw.ntruss.com/map-direction-15/v1/driving?start={start}&goal={goal}', headers=headers)
        response = api.make_response(r.json(), code=200)
        response.headers["Access-Control-Allow-Origin"] = "*"

        return response


api.add_resource(Routes, "/routes")


if __name__ == '__main__':
    app.run()