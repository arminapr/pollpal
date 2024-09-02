from backend.ml_models.model01 import predict, train_party_model

from flask import Blueprint, request, jsonify, make_response

ml_models = Blueprint('ml_models', __name__)

@ml_models.route('/ml_model/<v1>/<v2>/<v3>/<v4>/<v5>/<v6>/<v7>/<v8>/<v9>/<v10>/<v11>/<v12>/<v13>/<v14>', methods=['GET'])
def get_m(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14):
    params = [v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14]
    response = predict(params)
    
    return_dict = {'result': response}
    the_response = make_response(jsonify(return_dict))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


@ml_models.route('/ml_model/train', methods=['GET'])
def train():
    model, encoder = train_party_model()
    return_dict = {'message': 'Model trained successfully'}
    return jsonify(return_dict)