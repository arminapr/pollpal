import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from backend.db_connection import db
import numpy as np
import json


# Global variables to store the model and encoder
model = None
encoder = None

# Function to train the model
def train_party_model():
    # Fetch political party data
    cursor = db.get_db().cursor()
    cursor.execute("""SELECT V201228 FROM my_table""")
    rows = cursor.fetchall()
    
    if not rows:
        raise ValueError("No data found for political party. Please check your database query.")

    print("Political Party Data:", rows)  # Debug: Check if data is fetched correctly

    temp = [row['V201228'] for row in rows]
    print("Political Party Array:", temp)  # Debug: Check the array content

    y = np.array(temp)


    # Fetch all questions data
    cursor = db.get_db().cursor()
    cursor.execute('''SELECT V201228, V201014b, V201343, V201367, V201409, 
    V201412, V201416, V201417, V201427, V201510, V201575, 
    V201602, V201626, V201627, V201628, V202025, 
    V202172, V202173, V202174, V202224, V202240, V202249, 
    V202257, V202260, V202261, V202262, V202263, 
    V202265 FROM my_table''')

    rows = cursor.fetchall()
    
    if not rows:
        raise ValueError("No data found for questions. Please check your database query.")

    print("All Questions Data:", rows)  # Debug: Check if data is fetched correctly

    df = pd.DataFrame.from_dict(rows)
    print("DataFrame Shape:", df.shape)  # Debug: Check the shape of DataFrame

    # Check if DataFrame is empty
    if df.empty:
        raise ValueError("The DataFrame is empty. Please check the data fetching process.")

    encoder = OneHotEncoder(handle_unknown='ignore')
    X_encoded = encoder.fit_transform(df)

    # Ensure y and X_encoded have the same number of samples
    if len(y) != X_encoded.shape[0]:
        raise ValueError("Mismatch between the number of samples in X and y.")

    # If you're not using X_test and y_test, you can remove them
    X_train, _, y_train, _ = train_test_split(X_encoded, y, test_size=0.2, random_state=42)
    
    # Ensure X_train is not empty
    if X_train.shape[0] == 0:
        raise ValueError("Training set is empty after train_test_split. Adjust the test_size or check the data.")

    model = RandomForestClassifier()
    model.fit(X_train, y_train)

    # Get feature importances
    feature_importances = model.feature_importances_

    importances_json = json.dumps(feature_importances.tolist())

    # Store feature importances
    cursor = db.get_db().cursor()
    cursor.execute("""
        INSERT INTO feature_importances (importances)
        VALUES (%s)
    """, (importances_json,))

    db.get_db().commit()

    return 'Model trained and feature importances stored!'


# Function to make predictions
def predict(user_input):
    global model, encoder
    user_input_df = pd.DataFrame([user_input], columns=encoder.get_feature_names_out())
    user_input_encoded = encoder.transform(user_input_df)
    prediction = model.predict(user_input_encoded)
    return prediction[0]

