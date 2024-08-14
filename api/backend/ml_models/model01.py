import pandas as pd
from sklearn.model_selection import train_test_split
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from backend.db_connection import db
import numpy as np
import json

def train_party_model():
    cursor = db.get_db().cursor()
    
    # Fetch target variable (political party)
    cursor.execute("""SELECT V201228 FROM my_table""")
    rows = cursor.fetchall()
    temp = [row[0] for row in rows]  # Use index 0 for the first column
    y = np.array(temp)
    
    # Fetch features
    cursor.execute('''SELECT V201014b, V201343, V201367, V201409, 
    V201412, V201416, V201417, V201427, V201510, V201575, 
    V201602, V201626, V201627, V201628, V202025, 
    V202172, V202173, V202174, V202224, V202240, V202249, 
    V202257, V202260, V202261, V202262, V202263, 
    V202265 FROM my_table''')
    
    rows = cursor.fetchall()

    # Get column names from the cursor description
    columns = [desc[0] for desc in cursor.description]
    
    # Create DataFrame
    df = pd.DataFrame(rows, columns=columns)
    
    # Ensure there are no missing values or inappropriate data types
    df = df.fillna(0)  # or another appropriate method
    
    # One-hot encode features
    encoder = OneHotEncoder(handle_unknown='ignore')
    X_encoded = encoder.fit_transform(df)
    
    # Split data
    X_train, _, y_train, _ = train_test_split(X_encoded, y, test_size=0.2, random_state=42)
    
    # Train model
    model = RandomForestClassifier()
    model.fit(X_train, y_train)
    
    # Get feature importances
    feature_importances = model.feature_importances_
    importances_json = json.dumps(feature_importances.tolist())
    
    # Store feature importances in database
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
