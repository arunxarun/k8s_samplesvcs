import sys
import os
from flask import Flask, request
from flask_restful import Resource, Api
import logging
from logging import Logger
from webargs import fields, validate
from webargs.flaskparser import use_args, use_kwargs, parser, abort
import json
from datetime import datetime
from datetime import timedelta
import requests

app = Flask(__name__)
api = Api(app)

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

if os.environ.has_key('SVC2_SERVICE_HOST') == False:
    logging.error("must set SVC2_SERVICE_HOST env var")
    exit(1)
else:
    if os.environ.has_key('SVC2_SERVICE_PORT') == False:
        logging.error("must set SVC2_SERVICE_PORT env var")
        exit(1)
    else:
        SVC2 = "http://%s:%s/resource"%(os.environ['SVC2_SERVICE_HOST'],os.environ['SVC2_SERVICE_PORT'])


class Svc2:
    """ wraps calls to SVC2,
    uses k8s env vars.
    """

    def get(self,value):
        logging.debug("sending requests to %s with value %s"%(SVC2,value))
        r = requests.get(SVC2, params={'value':value})
        return r.json()



class Svc1:
    """ simple caller class. Broken out from Res for testability
    """
    def __init__(self, svc2):
        self.svc2 = svc2

    def get(self, value):
        """ calls svc2 and returns svc2 json
        """
        logging.debug("in svc1 get!")

        resp = self.svc2.get('value1');
        #resp = {'response': 200 }
        logging.debug(resp)
        return {'service': 'SVC1', 'calling': SVC2, 'response': resp['response'],'value': value}


class Res(Resource):
    """ REST resource (GET is the only enabled verb)
    """
    def __init__(self) :
        self.svc1 = Svc1(Svc2())

    """ structure is used to map variables in the GET call below
    """
    publish_args = {
        'value': fields.String(required=True)
    }

    @use_kwargs(publish_args)
    def get(self, value):
        """ delegate to svc1
        """
        return self.svc1.get(value)


api.add_resource(Res, '/resource')

if __name__ == '__main__':
    logging.debug("starting up: SVC2 set to %s"%SVC2)
    app.run(host='0.0.0.0',port=8080,debug=True)
