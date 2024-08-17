import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from backend.db_connection import db
import numpy as np
from flask import current_app
import json

def train_party_model():
    cursor = db.get_db().cursor()
    cursor.execute("""SELECT V201228 FROM my_table""")
    
    rows = cursor.fetchall()
    
    y = np.array([row['V201228'] for row in rows])
    
    cursor.execute('''SELECT V201228, V201343,V201409, V201417,
        V201427, V201510, V201602, V202224,
        V202249, V202257, V202260, V202261,
        V202262, V202263, V202265 FROM my_table''')
    
    rows = cursor.fetchall()
    
    
    df = pd.DataFrame(rows, columns=[
        'V201228', 'V201343','V201409', 'V201417', 
        'V201427', 'V201510', 'V201602', 'V202224', 
        'V202249', 'V202257', 'V202260', 'V202261', 
        'V202262', 'V202263', 'V202265'
    ])
    
    encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)  
    X_encoded = encoder.fit_transform(df)

    encoded_columns = encoder.get_feature_names_out(df.columns)
    X_encoded_df = pd.DataFrame(X_encoded, columns=encoded_columns)
    
    X_train, X_test, y_train, y_test = train_test_split(X_encoded_df, y, test_size=0.2, random_state=42)
    
    rf = RandomForestClassifier(n_estimators=100, max_depth=None, random_state=42)  
    rf.fit(X_train, y_train)
    
    return rf, encoder


def predict(user_input):
    model, encoder = train_party_model()  
    
    expected_columns = encoder.get_feature_names_out()
    
    user_input_dict = {}
    
    for column in expected_columns:
        if column in user_input:
            user_input_dict[column] = user_input[column]
        else:
            user_input_dict[column] = 0  
    
    user_input_df = pd.DataFrame([user_input_dict], columns=expected_columns)
    
    prediction = model.predict(user_input_df)
    return prediction[0]