# PollPal

## Creators
Armina Parvaresh Rizi, Nalika Palayoor, Niki Anand, Celia Burrington & Sriya Vuppala

## About

As election season comes upon us, many voters face the difficult decision of choosing a presidential candidate who will best represent their values and address the pressing issues faced by our nation. Campaign offices also face the challenge of understanding opponents’ strategies and accessing detailed voter demographics. Data analysts struggle with sifting through vast amounts of information and finding unbiased sources to inform their analyses. 

Given the needs of these entities, the intended users include campaign managers, civic-minded citizens, and data analysts. For dedicated voters, our app, PollPal, offers an intuitive and user-friendly platform that organizes historical voter data, presents clear visualizations of voting patterns, and provides summaries of key trends. This empowers voters to stay informed and engage in meaningful discussions within their communities. Additionally, our app features a survey to track real-time updates of voter opinion and a map feature for visualizing data geographically, ensuring both voters and campaign managers have the information they need at their fingertips. For the lead marketing and data analyst at PollPal, the information offered by our product will allow them to pinpoint areas of limited data to improve data acquisition strategies. 

Note: All data used in this app relies on mock data. 

## Demo
Watch the demo [here](https://youtu.be/1poJbeGhcqM)

## Features

- User-friendly platform for voters to stay informed on many things election-related
- Historical voter data and clear visualizations of voting patterns
- Real-time updates of voter opinion through surveys
- Geographical data visualization through map features
- Role-based access control for different user roles, including voter, campaign manager, and data analyst.
- Machine Learning model to predict someone's political affiliation (PENDING... IN PROGRESS)

## Running the Project
To run the project the user should first make a copy of the ```.env.template``` file and call it ```.env```. The user should change the ```DB_NAME``` to ```fontevote```. If you are planning to connect to our project's database docker container, make sure to set the ```MYSQL_ROOT_PASSWORD``` to your password of choice since that will be used to connect to the database through DataGrip. 

After setting up your ```.env```, the project can be run using the following command:
- ```docker compose up -d```

Run  ```docker compose down```  to stop the containers.

If there are any issues while running, run the following command:
- ```docker compose build --no-cache```

Run  ```docker compose up -d```  bring the containers back up.

The Streamlit app will then run on http://localhost:8501/.

## Project Directory

- Streamlit App (in the `./app` directory)
- Flask REST api (in the `./api` directory)
- MySQL setup files (in the `./database-files` directory)

## Role-Based Access Control (RBAC)

Our app demonstrates a simple RBAC system in Streamlit, where different user roles have access to specific features and functionalities. The code is organized to accommodate three roles:

- Campaign Manager
- Voter
- Data Analyst

## Disclosure

This application was made as a part of our final project for Introduction to Databases (CS 3200) at Northeastern University.
