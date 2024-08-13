from backend.ml_models.model import predict, train
from flask import Blueprint, request, jsonify, make_response

ml_models = Blueprint('ml_models', __name__)

# Prediction route for the ML model
@ml_models.route('/ml_models/predict', methods=['POST'])
def get_prediction():
    try:
        # Get JSON data from the request
        data = request.get_json()
        
        # Extract the variables (assuming they are in a list)
        variables = data.get('variables')
        if len(variables) != 28:
            return jsonify({'error': 'Exactly 28 variables are required'}), 400
        
        # Execute prediction
        response = predict(*variables)
        
        # Return the result
        return jsonify({'result': response}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Training route for the ML model
@ml_models.route('/ml_models/train', methods=['POST'])
def train_model():
    try:
        # Execute training
        train()
        return jsonify({'message': 'Model trained successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
