# -*- coding: utf-8 -*-
# ##############################################################################
# Version: 0.0.1 (2019-01-13)
# Author: Eduardo Bustos (ebustos@minsait.com), minsait

'''
Simple flask-based API to automatically calculate math expressions.
'''

import os
import sys
import logging
from flask import Flask, request, jsonify
from flask_restful import Api, Resource
from microcalculator.MicroCalculator import MicroCalculator

app = Flask(__name__)
api = Api(app)

logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s', level=logging.INFO)

VERSION = os.path.basename(os.path.dirname(__file__))
BASE_ROOT = "/api/v{}".format(VERSION)

global model # simple class to evaluate math expressions
model = MicroCalculator()
model.version = VERSION

print("Model: {}".format(model.__class__.__name__))
print("Version: {}".format(VERSION))

@app.route(BASE_ROOT + '/information', methods=['GET'])
def get_version():
    return jsonify(model.getBasicInfo())

@app.route(BASE_ROOT + '/calculate', methods=['GET'])
def get_status():
    return jsonify(dict(success=True))


@app.route(BASE_ROOT + '/calculate', methods=['POST'])
def calculate():
    '''Processes the input txt document and returns the predicted classes and their probabilities'''
    body = request.get_json(force=True)
    expression = body['expression']

    result = model.calculate(expression)

    return jsonify(dict(expression=expression, result=result))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)