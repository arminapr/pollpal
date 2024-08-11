########################################################
# Sample customers blueprint of endpoints
# Remove this file if you are not using it in your project
########################################################
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
    cursor.execute('SELECT year, stateName, voterTurnout from stateResult sR \
        JOIN election e ON sR.electionId = e.electionId \
        WHERE year = {0}'.format(year))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Get voter info by demographics
@voter_persona.route('/voter-info-ethnicity/<year>', methods=['GET'])
def get_voter_ethnicity_info(year):
    current_app.logger.info('voter_persona_routes.py: GET /voter-info-ethnicity/{0}'.format(year))
    cursor = db.get_db().cursor()
    cursor.execute('SELECT c.firstName, \
            c.lastName, \
            v.ethnicity as voterEthnicity, \
        COUNT(voterId) as numVotersByEthnicity \
        FROM voter v JOIN candidate c ON v.candidateId = c.candidateId \
        WHERE year = {0}} \
        GROUP BY firstName, lastName,  ethnicity'.format(year))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@voter_persona.route('/voter-info-gender/<year>', methods=['GET'])
def get_voter_gen_info(year):
    current_app.logger.info('voter_persona_routes.py: GET /voter-info-gender/{0}'.format(year))
    cursor = db.get_db().cursor()
    cursor.execute('SELECT c.firstName, \
            c.lastName, \
            v.gender as voterGender, \
        COUNT(voterId) as numVotersByGender \
        FROM voter v JOIN candidate c ON v.candidateId = c.candidateId \
        WHERE year = {0} \
        GROUP BY firstName, lastName, gender'.format(year))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@voter_persona.route('/voter-info-age/<year>', methods=['GET'])
def get_voter_age_info(year):
    current_app.logger.info('voter_persona_routes.py: GET /voter-info-age/{0}'.format(year))
    cursor = db.get_db().cursor()
    cursor.execute('SELECT c.firstName, \
            c.lastName, \
            v.age as voterAge, \
        COUNT(voterId) as numVotersByAge \
        FROM voter v JOIN candidate c ON v.candidateId = c.candidateId \
        WHERE year = {0} \
        GROUP BY firstName, lastName,  age'.format(year))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@voter_persona.route('/voter-info', methods=['POST'])
def add_voter():
    current_app.logger.info('POST /voter-info route')
    voter_info = request.json
    # current_app.logger.info(cust_info)
    # voter_id = voter_info['id'] ???
    poliAff = voter_info['politicalAffiliation']
    state = voter_info['state']
    county = voter_info['county']
    age = voter_info['age']
    income = voter_info['incomeLevel']
    ethnicity = voter_info['ethnicity']
    gender = voter_info['gender']
    candidateId = voter_info['candidateId']

    query = 'INSERT INTO voter VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
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
    query = 'UPDATE voter SET politicalAffiliation = %s, state = %s, county = %s \
        age = %s, incomeLevel = %s, ethnicity = %s, gender = %s, candidateId = %s \
        WHERE voterId = %s'
    data = (political_affiliation, state, county, age, income, ethnicity, gender, candidateId, voterId)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'voter updated!'

@voter_persona.route('/voter-site-survey/<voterId>', methods=['POST'])
def add_voter_site_survey(voterId):
    current_app.logger.info('POST /voter-site-survey route')
    site_survey = request.json
    # current_app.logger.info(cust_info)
    # foundVotingCenter, isUserFriendly, foundNeededInfo, informedAboutCandidate, discoveredWhere, voterId)
    foundCenter = site_survey['foundVotingCenter']
    isFriendly = site_survey['isUserFriendly']
    neededInfo = site_survey['foundNeededInfo']
    informed = site_survey['informedAboutCandidate']
    where = site_survey['discoveredWhere']
    
    query = 'INSERT INTO voter VALUES (%s, %s, %s, %s, %s, %s)'
    data = (foundCenter, isFriendly, neededInfo, informed, where, voterId)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'voter site survey response added!'

@voter_persona.route('/policies/<candidateId>', methods=['GET'])
def get_customer(candidateId):
    current_app.logger.info('GET /policies/<candidateId>')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT policyName, stance FROM candidate c \
                   JOIN advocatesFor aF on c.candidateId = aF.candidateId \
                   JOIN policy p on aF.policyId = p.policyId \
                   WHERE c.candidateId = {0}'.format(candidateId))
    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response