from backend.ml_models.model01 import predict
from backend.ml_models.model01 import train_party_model
from flask import Blueprint, request, jsonify, make_response

ml_models = Blueprint('ml_models', __name__)


# Prediction route for the ML model
@ml_models.route('/ml_model/<v1>/<v2>/<v3>/<v4>/<v5>/<v6>/<v7>/<v8>/<v9>/<v10>/<v11>/<v12>/<v13>/<v14>/<v15>/<v16>/<v17>/<v18>/<v19>/<v20>/<v21>/<v22>/<v23>/<v24>/<v25>/<v26>/<v27>/<v28>',methods = ['GET'])
def get_m(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28):

    response = predict(v1, v2, v3, v4, v5, v6, v7, v8, v9, v10, v11, v12, v13, v14, v15, v16, v17, v18, v19, v20, v21, v22, v23, v24, v25, v26, v27, v28)


    return_dict = {'result':response}
    the_response = make_response(return_dict)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return return_dict

@ml_models.route('/ml_models/train', methods=['GET'])
def train_m():
    response = train_party_model()
    return 'Sucess!'