import streamlit as st
import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.ensemble import RandomForestClassifier
import requests
import pickle

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
    1: "2. Do you favor or oppose the death penalty for persons convicted of murder?",
    2: "4. Should transgender people - that is, people who identify themselves as the sex or gender different from the one they were born as - have to use the bathrooms of the gender they were born as, or should they be allowed to use the bathrooms of their identified gender?",
    3: "7. Which comes closest to your view?",
    4: "8. How important do you think it is that everyone in the United States learns to speak English?",
    5: "9. What is the highest level of school you have completed or the highest degree you have received?",
    6: "11. How justified is it for people to use violence to pursue their political goals?",
    7:"19. How important is it that more women be elected to political office?",
    8: "21. What about your opinion – are you for or against preferential hiring and promotion of blacks?",
    9: "22. Next, do you favor, oppose, or neither favor nor oppose the governmenttrying to reduce the difference in incomes between the richest and poorest households?",
    10: "23. ‘Our society should do whatever is necessary to make sure that everyone has an equal opportunity to succeed.",
    11: "24. ‘This country would be better off if we worried less about how equal people are.’",
    12: "25. ‘It is not really that big a problem if some people have more of a chance in life than others.’",
    13: "26. 'If people were treated more equally in this country we would have many fewer problems.'",
    14: "28. ‘This country would have many fewer problems if there were more emphasis on traditional family ties.’"

}

choices = {
    1: ['Favor', 'Oppose'],
    2: ['Have to use the bathrooms of the gender they were born as', 'Be allowed to use the bathrooms of their identified gender'],
    3: ['Make all unauthorized immigrants felons and send them back to their home country','Have a guest worker program that allows unauthorized immigrants to remain in US to work but only for limited time','Allow unauthorized immigrants to remain in US & eventually qualify for citizenship but only if they meet requirements','Allow unauthorized immigrants to remain in US & eventually qualify for citizenship without penalties'],
    4: ['Very important','Somewhat important','Not very important','Not important at all'],
    5: ['Less than high school credential','High school graduate - High school diploma or equivalent (e.g. GED)','Some college but no degree','Associate degree in college - occupational/vocational','Associate degree in college - academic','Bachelor’s degree (e.g. BA, AB, BS)','Master’s degree (e.g. MA, MS, MEng, MEd, MSW, MBA)','Professional school degree (e.g. MD, DDS, DVM, LLB, JD)/Doctoral degree (e.g. PHD, EDD)'],
    6: ['Not justified at all', 'A little justified', 'Moderatly justified', 'Very justified', 'Extremely justified'],
    7: ['Not important at all', 'A little important', 'Moderatly important', 'Very important', 'Extremely important'],
    8: ['For','Against'],
    9: ['Favor','Oppose'],
    10: ['Agree strongly','Agree somewhat','Neither agree nor disagree','Disagree somewhat','Disagree strongly'],
    11: ['Agree strongly','Agree somewhat','Neither agree nor disagree','Disagree somewhat','Disagree strongly'],
    12: ['Agree strongly','Agree somewhat','Neither agree nor disagree','Disagree somewhat','Disagree strongly'],
    13: ['Agree strongly','Agree somewhat','Neither agree nor disagree','Disagree somewhat','Disagree strongly'],
    14: ['Agree strongly','Agree somewhat','Neither agree nor disagree','Disagree somewhat','Disagree strongly']
}

choice_values = {key: list(range(1, len(value) + 1)) for key, value in choices.items()}

radio_questions = [2,3,4,5,6,7,8,9,11,12,13,15,19,20,21,22,23,24,25,26,27,28]
dropdown_questions = [1,10]
numeric_questions = [14,16,17,18]


st.title("Political Party Predictor")

st.write("Please answer the following questions:")

user_input = []
for q_id, question in questions.items():
    selected_option = st.radio(
        question,
        options=choices.get(q_id, []),
        key=f"q{q_id}"
    )
    user_input_value = choice_values[q_id][choices[q_id].index(selected_option)]
    user_input.append(user_input_value)


(var_01, var_02, var_03, var_04, var_05, var_06, var_07, var_08, var_09, var_10,
 var_11, var_12, var_13, var_14) = user_input

if st.button("Predict"):
    num_questions = len(questions)
    user_input_df = pd.DataFrame([user_input], columns=[f'Q{i+1}' for i in range(num_questions)])

    if len(user_input) == 14:
        st.write(user_input)
        query = f'http://web-api:4000/m/ml_model/' + '/'.join(map(str, user_input))

        response = requests.get(query)

        results = response.json()
        st.write(f'Predicted Party: {results.get("result","Unknown")}')

    else:
        st.error("All questions must be answered.")