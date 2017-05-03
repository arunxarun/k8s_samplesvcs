import sys
from flask import Flask, request
from flask_restful import Resource, Api
import logging
from logging import Logger
from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort
import json
from datetime import datetime
from datetime import timedelta

app = Flask(__name__)
api = Api(app)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


class Res(Resource):

    publish_args = {
        'value': fields.String(required=True)
    }

    @use_kwargs(publish_args)
    def get(self, value):
        logging.debug("SVC2.get() called with %s"%value)
        logging.debug("returning response now...")
        return {'response': {'service':'SVC2', 'value': value}}


api.add_resource(Res, '/resource')

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080,debug=True)  # 0.0.0.0 because I am assigned an IP.
