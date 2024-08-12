import logging
logger = logging.getLogger()

import streamlit as st
import requests
import logging
logger = logging.getLogger()


# Predefined questions and choices
questions = {
    1: "How satisfied are you with the current state of the economy?",
    2: "Do you support the current government policies?",
    3: "How do you rate the healthcare system?",
    # Add more questions here
}

choices = {
    1: ['Very dissatisfied', 'Dissatisfied', 'Neutral', 'Satisfied', 'Very satisfied'],
    2: ['Yes', 'No'],
    3: ['Poor', 'Fair', 'Good', 'Very good', 'Excellent'],
    # Add more choices here
}

# Define the numeric values for each choice
choice_values = {
    1: [1, 2, 3, 4, 5],
    2: [1, 0],
    3: [1, 2, 3, 4, 5],
    # Add more numeric values here
}

# Streamlit app layout
st.title("Political Party Predictor")

st.write("Please answer the following questions:")

# Collect user responses
user_inputs = []
for q_id, question in questions.items():
    # Display the question as the label for the radio buttons
    selected_option = st.radio(
        question,
        options=choices[q_id],
        key=f"q{q_id}"
    )
    
    # Convert the selected option to the corresponding numeric value
    user_input_value = choice_values[q_id][choices[q_id].index(selected_option)]
    user_inputs.append(user_input_value)

if st.button("Predict"):
    # Convert user inputs to DataFrame
    num_questions = len(questions)
    user_input_df = pd.DataFrame([user_inputs], columns=[f'Q{i+1}' for i in range(num_questions)])
    
    # One-hot encode the inputs
    user_input_encoded = encoder.transform(user_input_df)
    
    # Predict
    prediction_code = model.predict(user_input_encoded)[0]
    
    # Convert prediction code to party name
    party_name = party_mapping.get(prediction_code, "Unknown")
    
    st.write(f'Predicted Party: {party_name}')