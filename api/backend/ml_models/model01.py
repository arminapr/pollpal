import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from backend.db_connection import db
import numpy as np
import json
import pickle


model = None
encoder = None

def train_party_model():
    cursor = db.get_db().cursor()
    cursor.execute("""SELECT V201228 FROM my_table""")
    rows = cursor.fetchall()

    temp = [row['V201228'] for row in rows]
    y = np.array(temp)


    cursor = db.get_db().cursor()
    cursor.execute('''SELECT V201014b, V201343, V201367, V201409, 
    V201412, V201416, V201417, V201427, V201510, V201575, 
    V201602, V201626, V201627, V201628, V202025, 
    V202172, V202173, V202174, V202224, V202240, V202249, 
    V202257, V202260, V202261, V202262, V202263, 
    V202265 FROM my_table''')

    rows = cursor.fetchall()
    
    df = pd.DataFrame.from_dict(rows)

    
    global encoder

    encoder = OneHotEncoder(handle_unknown='ignore')
    X_encoded = encoder.fit_transform(df)

    X_train, _, y_train, _ = train_test_split(X_encoded, y, test_size=0.2, random_state=42)
    

    
    global model

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    feature_importances = model.feature_importances_

    importances_json = json.dumps(feature_importances.tolist())

    cursor = db.get_db().cursor()
    cursor.execute("""
        INSERT INTO feature_importances (importances)
        VALUES (%s)
    """, (importances_json,))

    db.get_db().commit()

    with open('/model_files/encoder.pkl', 'wb') as f:
        pickle.dump(encoder, f)

    with open('/model_files/model.pkl', 'wb') as f:
        pickle.dump(model, f)

    return 'Model trained and feature importances stored!'


# Function to make predictions
def predict(user_input):
    global model, encoder

    if model is None or encoder is None:
        with open('model_files/encoder.pkl', 'rb') as f:
            encoder = pickle.load(f)
        with open('model_files/model.pkl', 'rb') as f:
            model = pickle.load(f)


    user_input_df = pd.DataFrame([user_input], columns=encoder.get_feature_names_out())
    user_input_encoded = encoder.transform(user_input_df)
    prediction = model.predict(user_input_encoded)
    return prediction[0]

