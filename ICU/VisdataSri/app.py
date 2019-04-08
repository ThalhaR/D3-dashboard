from flask import Flask, request
from flask_restful import Api

from flask_cors import CORS
from flask_pymongo import PyMongo

from .HelloWorld import HelloWorld
from .visdata import VizData


def create_app():
    app = Flask(__name__)
    # app.config["MONGO_URI"] = "mongodb://ishara1:ishara1@ds127704.mlab.com:27704/protect_cardiac"
    app.config["MONGO_URI"] = "mongodb://139.59.62.22:27017/patients"
    
    mongo = PyMongo(app)
    app.db = mongo
    CORS(app)
    api = Api(app)

    api.add_resource(HelloWorld, '/')
    api.add_resource(VizData, '/vizdata')

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', debug=True)
