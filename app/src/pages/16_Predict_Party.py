import streamlit as st
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
import requests

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

questions = {
    1: "1. What state do you reside in?",
    2: "2. Do you favor or oppose the death penalty for persons convicted of murder?",
    3: "3. How important is it that the executive, legislative, and judicial branches of government keep one another from having too much power?",
    4: "4. Should transgender people - that is, people who identify themselves as the sex or gender different from the one they were born as - have to use the bathrooms of the gender they were born as, or should they be allowed to use the bathrooms of their identified gender?",
    5: "5. Do you favor or oppose laws to protect gays/lesbians against job discrimination",
    6: "6. Which comes closest to your view?",
    7: "7. Which comes closest to your view?",
    8: "8. How important do you think it is that everyone in the United States learns to speak English?",
    9: "9. What is the highest level of school you have completed or the highest degree you have received?",
    10: "10. In what state/territory did you grow up?",
    11: "11. How justified is it for people to use violence to pursue their political goals?",
    12:"12. Some people think that the way people talk needs to change with the times to be more sensitive to people from different backgrounds. Others think that this has already gone too far and many people are just too easily offended. Which is closer to your opinion?",
    13:"13. How often do you stop yourself from saying something because you think someone might call you a racist, a sexist, or otherwise a bad person?",
    14:"14. How many guns are in your house?",
    15:"15. During the past 12 months, have you joined in a protest march, rally, or demonstration, or have you not done this in the past 12 months?",
    16:"16. Rate your feelings towards transgender people from 1 to 100, 1 being feeling \"cold\" toward them and 100 feeling \"warm\" toward them.",
    17:"17. Rate your feelings towards scientists from 1 to 100, 1 being feeling \"cold\" toward them and 100 feeling \"warm\" toward them.",
    18:"18. Rate your feelings towards the Black Lives Matter movement from 1 to 100, 1 being feeling \"cold\" toward them and 100 feeling \"warm\" toward them.",
    19:"19. How important is it that more women be elected to political office?",
    20: "20. Do you favor, oppose, or neither favor nor oppose providing a path to citizenship for unauthorized immigrants who obey the law, pay a fine, and pass security checks?",
    21: "21. hat about your opinion – are you for or against preferential hiring and promotion of blacks?",
    22: "22. Next, do you favor, oppose, or neither favor nor oppose the governmenttrying to reduce the difference in incomes between the richest and poorest households?",
    23: "23. ‘Our society should do whatever is necessary to make sure that everyone has an equal opportunity to succeed.",
    24: "24. ‘This country would be better off if we worried less about how equal people are.’",
    25: "25. ‘It is not really that big a problem if some people have more of a chance in life than others.’",
    26: "26. 'If people were treated more equally in this country we would have many fewer problems.'",
    27: "27. ‘The world is always changing and we should adjust our view of moral behavior to those changes.’",
    28: "28. ‘This country would have many fewer problems if there were more emphasis on traditional family ties.’"

}

choices = {
    1: [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Washington DC", "Florida", "Georgia", "Hawaii",
    "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
    "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
    "West Virginia", "Wisconsin", "Wyoming"
],
    2: ['Favor', 'Oppose'],
    3: ['Not important at all', 'A little important', 'Moderatly important', 'Very important', 'Extremely important'],
    4: ['Have to use the bathrooms of the gender they were born as', 'Be allowed to use the bathrooms of their identified gender'],
    5: ['Favor','Oppose'],
    6: ['Gay and lesbian couples should be allowed to legally marry','Gay and lesbian couples should be allowed to form civil unions but not legally marry','There should be no legal recognition of gay or lesbian couples’ relationship'],
    7: ['Make all unauthorized immigrants felons and send them back to their home country','Have a guest worker program that allows unauthorized immigrants to remain in US to work but only for limited time','Allow unauthorized immigrants to remain in US & eventually qualify for citizenship but only if they meet requirements','Allow unauthorized immigrants to remain in US & eventually qualify for citizenship without penalties'],
    8: ['Very important','Somewhat important','Not very important','Not important at all'],
    9: ['Less than high school credential','High school graduate - High school diploma or equivalent (e.g. GED)','Some college but no degree','Associate degree in college - occupational/vocational','Associate degree in college - academic','Bachelor’s degree (e.g. BA, AB, BS)','Master’s degree (e.g. MA, MS, MEng, MEd, MSW, MBA)','Professional school degree (e.g. MD, DDS, DVM, LLB, JD)/Doctoral degree (e.g. PHD, EDD)'],
    10: [
    "Alabama", "Alaska", "Arizona", "Arkansas", "California", "Colorado",
    "Connecticut", "Delaware", "Washington DC", "Florida", "Georgia", "Hawaii",
    "Idaho", "Illinois", "Indiana", "Iowa", "Kansas", "Kentucky", "Louisiana",
    "Maine", "Maryland", "Massachusetts", "Michigan", "Minnesota", "Mississippi",
    "Missouri", "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey",
    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", "Oklahoma",
    "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", "South Dakota",
    "Tennessee", "Texas", "Utah", "Vermont", "Virginia", "Washington", 
    "West Virginia", "Wisconsin", "Wyoming"],
    11: ['Not justified at all', 'A little justified', 'Moderatly justified', 'Very justified', 'Extremely justified'],
    12: ['The way people talk needs to change a lot','The way people talk needs to change a little','People are a little too easily offended','People are much too easily offended'],
    13: ['Never','Rarely','Occasionally','Fairly often','Very often'],
    15: ['Yes','No'],
    19: ['Not important at all', 'A little important', 'Moderatly important', 'Very important', 'Extremely important'],
    20: ['Favor','Oppose'],
    21: ['For','Against'],
    22: ['Favor','Oppose'],
    23: ['Agree strongly','Agree somewhat','Neither agree nor disagree','Disagree somewhat','Disagree strongly'],
    24: ['Agree strongly','Agree somewhat','Neither agree nor disagree','Disagree somewhat','Disagree strongly'],
    25: ['Agree strongly','Agree somewhat','Neither agree nor disagree','Disagree somewhat','Disagree strongly'],
    26: ['Agree strongly','Agree somewhat','Neither agree nor disagree','Disagree somewhat','Disagree strongly'],
    27: ['Agree strongly','Agree somewhat','Neither agree nor disagree','Disagree somewhat','Disagree strongly'],
    28: ['Agree strongly','Agree somewhat','Neither agree nor disagree','Disagree somewhat','Disagree strongly']
}

choice_values = {key: list(range(1, len(value) + 1)) for key, value in choices.items()}


radio_questions = [2,3,4,5,6,7,8,9,11,12,13,15,19,20,21,22,23,24,25,26,27,28]
dropdown_questions = [1,10]
numeric_questions = [14,16,17,18]

st.title("Political Party Predictor")

st.write("Please answer the following questions:")

user_input = []
for q_id, question in questions.items():
    selected_option = None 
    if q_id in radio_questions:
        selected_option = st.radio(
            question,
            options=["Choose one of the following"] + choices.get(q_id, []),
            key=f"q{q_id}"
        )
    elif q_id in dropdown_questions:
        selected_option = st.selectbox(
            question,
            options=[""] + choices.get(q_id, []),  
            key=f"q{q_id}"
        )
    elif q_id in numeric_questions:
        input_text = st.text_input(
            question,
            key=f"q{q_id}",
            value="" 
        )
    
    if q_id in choice_values and selected_option in choices.get(q_id, []):
        user_input_value = choice_values[q_id][choices[q_id].index(selected_option)]
    else:
        user_input_value = None  

    user_input.append(user_input_value)

(var_01, var_02, var_03, var_04, var_05, var_06, var_07, var_08, var_09, var_10,
 var_11, var_12, var_13, var_14, var_15, var_16, var_17, var_18, var_19, var_20,
 var_21, var_22, var_23, var_24, var_25, var_26, var_27, var_28) = user_input

if st.button("Predict"):
    num_questions = len(questions)
    user_input_df = pd.DataFrame([user_input], columns=[f'Q{i+1}' for i in range(num_questions-1)])
    
    encoder = OneHotEncoder(handle_unknown='ignore')
    user_input_encoded = encoder.transform(user_input_df)
    model = RandomForestClassifier()
    prediction_code = model.predict(user_input_encoded)[0]
    
    party_name = party_mapping.get(prediction_code, "Unknown")

    if len(user_input) == 28:
        query = f'http://web-api:4000/m/ml_models/1/{var_01}/{var_02}/{var_03}/{var_04}/{var_05}/{var_06}/{var_07}/{var_08}/{var_09}/{var_10}/{var_11}/{var_12}/{var_13}/{var_14}/{var_15}/{var_16}/{var_17}/{var_18}/{var_19}/{var_20}/{var_21}/{var_22}/{var_23}/{var_24}/{var_25}/{var_26}/{var_27}/{var_28}'
    
results = requests.get(query).json()

st.write(f'Predicted Party: {results}')