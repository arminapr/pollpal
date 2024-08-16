import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from backend.db_connection import db
import numpy as np
import json
import pickle


# Function to train the model
def train_party_model():
    cursor = db.get_db().cursor()
    cursor.execute("""SELECT V201228 FROM my_table""")
    rows = cursor.fetchall()
    
    # Extracting 'V201228' values
    y = np.array([row[0] for row in rows])  # Use index 0 as rows are tuples

    cursor.execute('''SELECT V201014b, V201343, V201367, V201409, 
        V201412, V201416, V201417, V201427, V201510, V201575, 
        V201602, V201626, V201627, V201628, V202025, 
        V202172, V202173, V202174, V202224, V202240, V202249, 
        V202257, V202260, V202261, V202262, V202263, 
        V202265 FROM my_table''')
    
    rows = cursor.fetchall()
    df = pd.DataFrame(rows, columns=[
        'V201014b', 'V201343', 'V201367', 'V201409', 
        'V201412', 'V201416', 'V201417', 'V201427', 
        'V201510', 'V201575', 'V201602', 'V201626', 
        'V201627', 'V201628', 'V202025', 'V202172', 
        'V202173', 'V202174', 'V202224', 'V202240', 
        'V202249', 'V202257', 'V202260', 'V202261', 
        'V202262', 'V202263', 'V202265'
    ])
    
    encoder = OneHotEncoder(handle_unknown='ignore')
    X_encoded = encoder.fit_transform(df).toarray()

    X_train, X_test, y_train, y_test = train_test_split(X_encoded, y, test_size=0.2, random_state=42)
    
    rf = RandomForestClassifier(n_estimators=10, max_depth=3, random_state=42)
    rf.fit(X_train, y_train)
    
    return rf, encoder

# Function to make predictions
def predict(user_input):
    model, encoder = train_party_model()  # Train the model and get encoder
    
    user_input_df = pd.DataFrame([user_input], columns=encoder.get_feature_names_out())
    user_input_encoded = encoder.transform(user_input_df).toarray()
    
    prediction = model.predict(user_input_encoded)
    return prediction[0]