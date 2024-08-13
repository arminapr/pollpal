from flask import Blueprint, request, jsonify, make_response
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import json

ml_models = Blueprint('ml_models', __name__)

# Global variables to store the model and encoder
model = None
encoder = None

# Function to train the model
def train_party_model(csv_path):
    columns_to_keep = [
        'V201228','V201014b', 'V201343', 'V201367','V201409', 
        'V201412', 'V201416', 'V201417', 'V201427', 'V201510', 'V201575', 
        'V201602', 'V201626', 'V201627', 'V201628', 'V202025', 'V202171', 
        'V202172', 'V202173', 'V202174', 'V202224', 'V202240', 'V202249', 
        'V202257', 'V202260', 'V202261', 'V202262', 'V202263', 'V202264', 
        'V202265', 'V202266', 'V202267', 'V202268', 'V202269', 'V202270', 
        'V202271', 'V202274', 'V202277', 'V202283', 'V202287', 'V202291', 
        'V202292', 'V202300', 'V202301', 'V202302', 'V202303', 'V202304', 
        'V202305', 'V202306', 'V202307', 'V202309', 'V202311', 'V202312', 
        'V202317', 'V202452', 'V202453', 'V202454', 'V202455', 'V202576', 
        'V202579'
    ]
    df = pd.read_csv(csv_path, usecols=columns_to_keep)
    X = df.drop('V201228', axis=1)
    y = df['V201228']
    encoder = OneHotEncoder(handle_unknown='ignore')
    X_encoded = encoder.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = accuracy_score(y_test, y_pred)
    return model, encoder, accuracy

# Function to make predictions
def predict_party(model, encoder, user_input):
    user_input_df = pd.DataFrame([user_input], columns=model.feature_names_in_)
    user_input_encoded = encoder.transform(user_input_df)
    prediction = model.predict(user_input_encoded)
    return prediction[0]

# Prediction model route 3: political party prediction
@ml_models.route('/ml_models/3/<user_input>', methods=['GET'])
def get_m3(user_input):
    global model, encoder
    user_input_list = json.loads(user_input)  # Assuming user_input is passed as a JSON string
    predicted_code = predict_party(model, encoder, user_input_list)
    party_mapping = {
        -9: "Refused",
        -8: "Don’t know",
        -4: "Technical error",
        0: "No preference",
        1: "Democrat",
        2: "Republican",
        3: "Independent",
        5: "Other party"
    }
    party_name = party_mapping.get(predicted_code, "Unknown")
    return jsonify({'result': party_name})

# Training model 3
@ml_models.route('/ml_models/3/train', methods=['GET'])
def train_m3():
    global model, encoder
    csv_path = '/Users/nalikapalayoor/Downloads/anes_timeseries_2020_csv_20220210/anes_timeseries_2020_csv_20220210.csv'
    model, encoder, accuracy = train_party_model(csv_path)
    return f'Success! Model trained with accuracy: {accuracy:.2f}'
