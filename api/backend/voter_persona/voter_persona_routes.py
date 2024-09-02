from datetime import datetime
from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

voter_persona = Blueprint('voter_persona', __name__)

# selecting voter turnout per state in a particular year
@voter_persona.route('/state-voters/<year>', methods=['GET'])
def get_voter_turnout(year):
    current_app.logger.info('voter_persona_routes.py: GET /state-voters/<year>')
    current_app.logger.info(f'year = {year}')
    cursor = db.get_db().cursor()
    # selecting voter turnout per state in a particular year
    cursor.execute('SELECT stateName, round((voterTurnout * 100),2) as voterTurnout from stateResult sR \
        JOIN election e ON sR.electionId = e.electionId \
        WHERE year = {0}'.format(year))
    the_data = cursor.fetchall()
    the_response = make_response(jsonify(the_data))
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
        COUNT(voter_id) as numVotersByEthnicity \
        FROM voter v JOIN candidate c ON v.candidate_id = c.candidate_id \
        GROUP BY politicalAffiliation, ethnicity')
    the_data = cursor.fetchall()
    the_response = make_response(jsonify(the_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@voter_persona.route('/voter-info-gender', methods=['GET'])
def get_voter_gen_info():
    current_app.logger.info('voter_persona_routes.py: GET /voter-info-gender')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT v.politicalAffiliation, \
            v.gender as voterGender, \
        COUNT(voter_id) as numVotersByGender \
        FROM voter v JOIN candidate c ON v.candidate_id = c.candidate_id \
        GROUP BY v.politicalAffiliation, v.gender')
    the_data = cursor.fetchall()
    the_response = make_response(jsonify(the_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@voter_persona.route('/voter-info-age', methods=['GET'])
def get_voter_age_info():
    current_app.logger.info('voter_persona_routes.py: GET /voter-info-age')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT v.politicalAffiliation, \
            v.age as voterAge, \
        COUNT(voter_id) as numVotersByAge \
        FROM voter v JOIN candidate c ON v.candidate_id = c.candidate_id \
        GROUP BY v.politicalAffiliation, v.age')
    the_data = cursor.fetchall()
    the_response = make_response(jsonify(the_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Insert statement into voter table
@voter_persona.route('/voter-info', methods=['POST'])
def add_voter():
    current_app.logger.info('POST /voter-info route')
    voter_info = request.json
    current_app.logger.info(voter_info)
    poli_aff = voter_info['politicalAffiliation']
    state = voter_info['state']
    county = voter_info['county']
    age = voter_info['age']
    income = voter_info['incomeLevel']
    ethnicity = voter_info['ethnicity']
    gender = voter_info['gender']
    candidate_id = voter_info['candidate_id']

    query = 'INSERT INTO voter (politicalAffiliation, state, county, age, incomeLevel, \
                ethnicity, gender, candidate_id) \
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    data = (poli_aff, state, county, age, income, ethnicity, gender, candidate_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'voter added!'

# Update voter information
@voter_persona.route('/voter-info/<voter_id>', methods=['PUT'])
def update_customer(voter_id):
    current_app.logger.info('PUT /voter-info/{0}'.format(voter_id))
    voter_info = request.json
    political_affiliation = voter_info['politicalAffiliation']
    state = voter_info['state']
    county = voter_info['county']
    age = voter_info['age']
    income = voter_info['incomeLevel']
    ethnicity = voter_info['ethnicity']
    gender = voter_info['gender']
    candidate_id = voter_info['candidate_id']
    query = 'UPDATE voter SET politicalAffiliation = %s, state = %s, county = %s, \
        age = %s, incomeLevel = %s, ethnicity = %s, gender = %s, candidate_id = %s \
        WHERE voter_id = %s'
    data = (political_affiliation, state, county, age, income, ethnicity, gender, candidate_id, voter_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'voter updated!'

# Input voter feedback
@voter_persona.route('/voter-site-survey', methods=['POST'])
def add_voter_site_survey():
    current_app.logger.info('POST /voter-site-survey route')
    site_survey = request.json
    voter_id = site_survey['voter_id']
    found_center = 1 if site_survey['foundVotingCenter'] else 0 
    is_friendly = site_survey['isUserFriendly']
    needed_info = site_survey['foundNeeded_info']
    informed = 1 if site_survey['informedAboutCandidate'] else 0
    where = site_survey['discoveredWhere']
    
    query = 'INSERT INTO voterSiteSurvey (foundVotingCenter, isUserFriendly, foundNeeded_info, \
                informedAboutCandidate, discoveredWhere, voter_id) \
            VALUES (%s, %s, %s, %s, %s, %s)'
    data = (found_center, is_friendly, needed_info, informed, where, voter_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'voter site survey response added!'

# View policies by candidate
@voter_persona.route('/policies/<candidate_id>', methods=['GET'])
def get_customer(candidate_id):
    current_app.logger.info('GET /policies/<candidate_id>')
    cursor = db.get_db().cursor()
    cursor.execute('''
            SELECT DISTINCT p.policyName, p.stance FROM policy p
            JOIN advocatesFor aF on aF.policyId = p.policyId
            JOIN candidate c on c.candidate_id = aF.candidate_id
            WHERE c.candidate_id = %s
        ''', (candidate_id))
    
    the_data = cursor.fetchall()
    the_response = make_response(jsonify(the_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Routes used to populate dropdown options
@voter_persona.route('/voter-id', methods=['GET'])
def get_campaign_ids():
    current_app.logger.info('GET /voter-id')
    query = 'SELECT voter_id FROM voter'  
    cursor = db.get_db().cursor()
    cursor.execute(query)
    voter_ids = cursor.fetchall()
    return jsonify(voter_ids)

@voter_persona.route('/candidate-names', methods=['GET'])
def get_candidate_name():
    current_app.logger.info('voter_persona_routes.py: GET /candidate-names')
    cursor = db.get_db().cursor()
    current_year = datetime.now().year
    cursor.execute('SELECT firstName, lastName, c.candidate_id \
        FROM candidate c \
        JOIN ranIn r ON c.candidate_id = r.candidate_id \
        JOIN election e ON r.electionId = e.electionId \
        WHERE year = {0}'.format(current_year))
    the_data = cursor.fetchall()
    the_response = make_response(jsonify(the_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@voter_persona.route('/all-candidate-names', methods=['GET'])
def get_all_candidate_names():
    current_app.logger.info('voter_persona_routes.py: GET /candidate-names')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT firstName, lastName, c.candidate_id \
        FROM candidate c')
    the_data = cursor.fetchall()
    the_response = make_response(jsonify(the_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@voter_persona.route('/election-years', methods=['GET'])
def get_election_year():
    current_app.logger.info('voter_persona_routes.py: GET /election-years')
    cursor = db.get_db().cursor()
    # select all election years that have a winner (a.k.a that we have result data for)
    cursor.execute('SELECT DISTINCT year\
                   FROM election e\
                   WHERE winnerId IS NOT NULL\
                   ORDER BY year DESC')
    the_data = cursor.fetchall()
    the_response = make_response(jsonify(the_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@voter_persona.route('/last-voter-id', methods=['GET'])
def get_last_voter_id():
    current_app.logger.info('GET /last-voter-id route')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT MAX(voter_id) FROM voter')
    last_id = cursor.fetchall()
    return jsonify({'lastVoter_id': last_id})

@voter_persona.route('/voting-center', methods=['GET'])
def get_voting_center():
   current_app.logger.info('voter_persona_routes.py: GET /voting-center')
   cursor = db.get_db().cursor()
   cursor.execute('SELECT c.street, \
           c.city, \
           c.state, c.zipcode \
       FROM votingCenter c')
   the_data = cursor.fetchall()
   the_response = make_response(jsonify(the_data))
   the_response.status_code = 200
   the_response.mimetype = 'application/json'
   return the_response
