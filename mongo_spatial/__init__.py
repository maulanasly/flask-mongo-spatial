from flask import Flask, jsonify
from flask_restful import Api
from flask_restful_swagger import swagger
from flask_pymongo import PyMongo
from mongo_spatial.config import config
from mongo_spatial.exceptions import BaseExceptions

import os


app = Flask(__name__, instance_relative_config=True)

environment = os.getenv('APP_CONFIGURATION', 'development')
config_file = environment + '.cfg'
app.config.from_object(config[environment])
app.config.from_pyfile(config_file, silent=True)

api = swagger.docs(Api(app), apiVersion='0.1', api_spec_url='/spec', description="basic authentications")
mongo = PyMongo(app)


from mongo_spatial.resources.malls import MallCreationAPI, MallAPI, MallListAPI

api.add_resource(MallCreationAPI, '/mall')
api.add_resource(MallAPI, '/mall/<int:mall_id>')
api.add_resource(MallListAPI, '/mall/list')


@app.errorhandler(BaseExceptions)
def handle_exception(error):
    data = {
        "code": error.code,
        "reason": error.message,
        "extra_info": error.extra
    }
    response = jsonify(data)
    response.status_code = error.status_code
    return response
