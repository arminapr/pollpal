# PollPal

## Creators
Armina Parvaresh Rizi, Nalika Palayoor, Niki Anand, Celia Burrington & Sriya Vuppala

## About

As election season comes upon us, many voters face the difficult decision of choosing a presidential candidate who will best represent their values and address the pressing issues faced by our nation. Campaign offices also face the challenge of understanding opponents’ strategies and accessing detailed voter demographics. Data analysts struggle with sifting through vast amounts of information and finding unbiased sources to inform their analyses. 

Given the needs of these entities, the intended users include campaign managers, civic-minded citizens, and data analysts. For dedicated voters, our app, PollPal, offers an intuitive and user-friendly platform that organizes historical voter data, presents clear visualizations of voting patterns, and provides summaries of key trends. This empowers voters to stay informed and engage in meaningful discussions within their communities. Additionally, our app features a survey to track real-time updates of voter opinion and a map feature for visualizing data geographically, ensuring both voters and campaign managers have the information they need at their fingertips. For the lead marketing and data analyst at PollPal, the information offered by our product will allow them to pinpoint areas of limited data to improve data acquisition strategies. 

Note: All data used in this app relies on mock data. 

## Features

- User-friendly platform for voters to stay informed on many things election-related
- Historical voter data and clear visualizations of voting patterns
- Real-time updates of voter opinion through surveys
- Geographical data visualization through map features
- Role-based access control for different user roles, including voter, campaign manager, and data analyst.

## Running the Project
To run the project or run it after completing any changes the two following actions should be run in the terminal:
- ```docker compose down ```
- ```docker compose up -d ```

  
If there any issues while running this action should be run:
- ```docker compose build --no-cache ```
and after that ``` docker compose up - d ``` to run the project again

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
