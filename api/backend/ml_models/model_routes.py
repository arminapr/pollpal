from backend.ml_models.model1 import predict
from backend.ml_models.model1 import train 
from backend.ml_models.model2 import predict2
from backend.ml_models.model2 import train2 
from backend.db_connection import db
import numpy as np
import logging
from flask import Blueprint, request, jsonify, make_response, current_app
import json

ml_models = Blueprint('ml_models', __name__)

# prediction model route 1: hotel cost per night
@ml_models.route('/ml_models/1/<v1>/<v2>/<v3>/<v4>/<v5>', methods=['GET'])
def get_m1(v1,v2, v3, v4, v5):

    # Execute prediction
    response = predict(v1, v2, v3, v4, v5)
    
    # format and return the response
    return_dict = {'result': response}

    the_response = make_response(return_dict)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    #return str(the_response)
    return return_dict

# training model 1
@ml_models.route('/ml_models/1', methods=['GET'])
def train_m1():
    # Execute training
    response = train()
    return 'Sucess!'


# prediction model route 2: flight cost one-way
@ml_models.route('/ml_models/2/<v1>/<v2>/<v3>/<v4>/<v5>', methods=['GET'])
def get_m2(v1,v2, v3, v4, v5):

    # Execute prediction
    response = predict2(v1, v2, v3, v4, v5)
    
    # format and return the response
    return_dict = {'result': response}

    the_response = make_response(return_dict)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    #return str(the_response)
    return return_dict

# training model 2
@ml_models.route('/ml_models/2', methods=['GET'])
def train_m2():
    # Execute training
    response = train2()
    return 'Sucess!'