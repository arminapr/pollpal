########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
from datetime import datetime
from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

voter_persona = Blueprint('voter_persona', __name__)

@voter_persona.route('/state-voters/<year>', methods=['GET'])
def get_voter_turnout(year):
    current_app.logger.info('voter_persona_routes.py: GET /state-voters/<year>')
    current_app.logger.info(f'year = {year}')
    cursor = db.get_db().cursor()
    # selecting voter turnout per state in a particular year (for heatmap)
    cursor.execute('SELECT stateName, round((voterTurnout * 100),2) as voterTurnout from stateResult sR \
        JOIN election e ON sR.electionId = e.electionId \
        WHERE year = {0}'.format(year))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Get voter info by demographics
@voter_persona.route('/voter-info-ethnicity', methods=['GET'])
def get_voter_ethnicity_info():
    current_app.logger.info('voter_persona_routes.py: GET /voter-info-ethnicity')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT v.politicalAffiliation, \
            v.ethnicity as voterEthnicity, \
        COUNT(voterId) as numVotersByEthnicity \
        FROM voter v JOIN candidate c ON v.candidateId = c.candidateId \
        GROUP BY politicalAffiliation, ethnicity')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@voter_persona.route('/voter-info-gender', methods=['GET'])
def get_voter_gen_info():
    current_app.logger.info('voter_persona_routes.py: GET /voter-info-gender')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT v.politicalAffiliation, \
            v.gender as voterGender, \
        COUNT(voterId) as numVotersByGender \
        FROM voter v JOIN candidate c ON v.candidateId = c.candidateId \
        GROUP BY v.politicalAffiliation, v.gender')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@voter_persona.route('/voter-info-age', methods=['GET'])
def get_voter_age_info():
    current_app.logger.info('voter_persona_routes.py: GET /voter-info-age')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT v.politicalAffiliation, \
            v.age as voterAge, \
        COUNT(voterId) as numVotersByAge \
        FROM voter v JOIN candidate c ON v.candidateId = c.candidateId \
        GROUP BY v.politicalAffiliation, v.age')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@voter_persona.route('/voter-info', methods=['POST'])
def add_voter():
    current_app.logger.info('POST /voter-info route')
    voter_info = request.json
    # current_app.logger.info(cust_info)
    current_app.logger.info(voter_info)
    poliAff = voter_info['politicalAffiliation']
    state = voter_info['state']
    county = voter_info['county']
    age = voter_info['age']
    income = voter_info['incomeLevel']
    ethnicity = voter_info['ethnicity']
    gender = voter_info['gender']
    candidateId = voter_info['candidateId']

    query = 'INSERT INTO voter (politicalAffiliation, state, county, age, incomeLevel, \
                ethnicity, gender, candidateId) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    data = (poliAff, state, county, age, income, ethnicity, gender, candidateId)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'voter added!'

@voter_persona.route('/voter-info/<voterId>', methods=['PUT'])
def update_customer(voterId):
    current_app.logger.info('PUT /voter-info/{0}'.format(voterId))
    voter_info = request.json
    political_affiliation = voter_info['politicalAffiliation']
    state = voter_info['state']
    county = voter_info['county']
    age = voter_info['age']
    income = voter_info['incomeLevel']
    ethnicity = voter_info['ethnicity']
    gender = voter_info['gender']
    candidateId = voter_info['candidateId']
    query = 'UPDATE voter SET politicalAffiliation = %s, state = %s, county = %s, \
        age = %s, incomeLevel = %s, ethnicity = %s, gender = %s, candidateId = %s \
        WHERE voterId = %s'
    data = (political_affiliation, state, county, age, income, ethnicity, gender, candidateId, voterId)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'voter updated!'

@voter_persona.route('/voter-site-survey', methods=['POST'])
def add_voter_site_survey():
    current_app.logger.info('POST /voter-site-survey route')
    site_survey = request.json
    voterId = site_survey['voterId']
    foundCenter = 1 if site_survey['foundVotingCenter'] else 0 
    isFriendly = site_survey['isUserFriendly']
    neededInfo = site_survey['foundNeededInfo']
    informed = 1 if site_survey['informedAboutCandidate'] else 0
    where = site_survey['discoveredWhere']
    
    query = 'INSERT INTO voterSiteSurvey (foundVotingCenter, isUserFriendly, foundNeededInfo, informedAboutCandidate, discoveredWhere, voterId) VALUES (%s, %s, %s, %s, %s, %s)'
    data = (foundCenter, isFriendly, neededInfo, informed, where, voterId)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'voter site survey response added!'

@voter_persona.route('/policies/<candidateId>', methods=['GET'])
def get_customer(candidateId):
    current_app.logger.info('GET /policies/<candidateId>')
    cursor = db.get_db().cursor()
    cursor.execute('''
            SELECT DISTINCT p.policyName, p.stance FROM policy p
            JOIN advocatesFor aF on aF.policyId = p.policyId
            JOIN candidate c on c.candidateId = aF.candidateId
            WHERE c.candidateId = %s
        ''', (candidateId))
    
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# TODO: ask about including this in the api matrix
@voter_persona.route('/voter-id', methods=['GET'])
def get_campaign_ids():
    current_app.logger.info('GET /voter-id')
    query = 'SELECT voterId FROM voter'  
    cursor = db.get_db().cursor()
    cursor.execute(query)
    voter_ids = cursor.fetchall()
    return jsonify(voter_ids)

@voter_persona.route('/candidate-names', methods=['GET'])
def get_candidate_name():
    current_app.logger.info('voter_persona_routes.py: GET /candidate-names')
    cursor = db.get_db().cursor()
    current_year = datetime.now().year
    cursor.execute('SELECT firstName, lastName, c.candidateId \
        FROM candidate c \
        JOIN ranIn r ON c.candidateId = r.candidateId \
        JOIN election e ON r.electionId = e.electionId \
        WHERE year = {0}'.format(current_year))
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@voter_persona.route('/all-candidate-names', methods=['GET'])
def get_all_candidate_names():
    current_app.logger.info('voter_persona_routes.py: GET /candidate-names')
    cursor = db.get_db().cursor()
    current_year = datetime.now().year
    cursor.execute('SELECT firstName, lastName, c.candidateId \
        FROM candidate c')
    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@voter_persona.route('/election-years', methods=['GET'])
def get_election_year():
    current_app.logger.info('voter_persona_routes.py: GET /election-years')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT DISTINCT year\
                   FROM election e\
                   ORDER BY year DESC')
    theData = cursor.fetchall()
    current_app.logger.info(f'Retrieved data: {theData}')
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@voter_persona.route('/last-voter-id', methods=['GET'])
def get_last_voter_id():
    current_app.logger.info('GET /last-voter-id route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT MAX(voterId) FROM voter')
    last_id = cursor.fetchall()
    return jsonify({'lastVoterId': last_id})

@voter_persona.route('/voting-center', methods=['GET'])
def get_voting_center():
   current_app.logger.info('voter_persona_routes.py: GET /voting-center')
   cursor = db.get_db().cursor()
   cursor.execute('SELECT c.street, \
           c.city, \
           c.state, c.zipcode \
       FROM votingCenter c')
   theData = cursor.fetchall()
   the_response = make_response(jsonify(theData))
   the_response.status_code = 200
   the_response.mimetype = 'application/json'
   return the_response