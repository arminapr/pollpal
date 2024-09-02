from flask import Blueprint, jsonify, make_response, current_app
from backend.db_connection import db

data_analyst = Blueprint('data_analyst', __name__)

# view campaign site survey results
@data_analyst.route('/campaign-site-survey', methods=['GET'])
def get_campaign_site_survey():
    current_app.logger.info('data_analyst_routes.py: GET /campaign-site-survey')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM campaignManagerSiteSurvey')
    the_data = cursor.fetchall()
    the_response = make_response(jsonify(the_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# view voter site survey results
@data_analyst.route('/voter-site-survey', methods=['GET'])
def get_voter_site_survey():
    current_app.logger.info('data_analyst_routes.py: GET /voter-site-survey')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM voterSiteSurvey')
    the_data = cursor.fetchall()
    the_response = make_response(jsonify(the_data))
    current_app.logger.info(the_data)
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# view voter demographics
@data_analyst.route('/voter-info-ethnicity', methods=['GET'])
def get_voter_ethnicity():
    current_app.logger.info('data_analyst_routes.py: GET /voter-info')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT ethnicity, COUNT(voterId) as userCount\
    FROM voter v GROUP BY ethnicity ORDER BY userCount ASC')
    the_data = cursor.fetchall()
    the_response = make_response(jsonify(the_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@data_analyst.route('/voter-info-age', methods=['GET'])
def get_voter_age():
    current_app.logger.info('data_analyst_routes.py: GET /voter-info')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT age, COUNT(voterId) as userCount\
    FROM voter v GROUP BY age ORDER BY userCount ASC')
    the_data = cursor.fetchall()
    the_response = make_response(jsonify(the_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@data_analyst.route('/voter-info-gender', methods=['GET'])
def get_voter_gender():
    current_app.logger.info('data_analyst_routes.py: GET /voter-info')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT gender, COUNT(voterId) as userCount\
    FROM voter v GROUP BY gender ORDER BY userCount ASC')
    the_data = cursor.fetchall()
    the_response = make_response(jsonify(the_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

@data_analyst.route('/voter-info', methods=['GET'])
def get_invalid_data():
    current_app.logger.info('data_analyst_persona_routes.py: GET /voter-info')
    cursor = db.get_db().cursor()
    cursor.execute('SELECT * FROM voter ORDER BY age')
    the_data = cursor.fetchall()
    the_response = make_response(jsonify(the_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

# Deleting invalid user data, voter ages below 18
@data_analyst.route('/voter-info', methods=['DELETE'])
def delete_invalid_data():
    current_app.logger.info('data_analyst_persona_routes.py: DELETE /voter-info')
    cursor = db.get_db().cursor()
    cursor.execute('DELETE FROM voter v WHERE v.age < 18')
    db.get_db().commit()
    the_response = make_response(jsonify({"message": "Data deleted"}))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response
