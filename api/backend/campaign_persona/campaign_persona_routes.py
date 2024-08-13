from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db

campaign_manager = Blueprint('campaign_manager', __name__)

# Return a realtime ratio of voters to candidates for the current election g
@campaign_manager.route('/polling-data', methods=['GET'])
def get_voter_to_candidate_ratio():
    current_app.logger.info('data_analyst_routes.py: GET /polling-data')
    cursor = db.get_db().cursor()

    cursor.execute(' \
        SELECT candidateId, COUNT(voterID)as votes \
        FROM voter v JOIN candidate c ON v.candidateId=c.candidateId \
            JOIN ranIn r on r.candidateId=c.candidateId \
            JOIN election e on e.electionId =r.electionId \
            WHERE e.year = 2024 \
            GROUP BY candidateID')

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response



# Return swing states based on the state’s popular vote ratio across a period of years (from 2.

@campaign_manager.route('/swing-state', methods=['GET'])
def get_swing_states():
    current_app.logger.info('data_analyst_routes.py: GET /swing-states')
    cursor = db.get_db().cursor()

    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')

    cursor.execute(' \
        SELECT DISTINCT stateAbbr \
        FROM election e JOIN stateResult s ON e.electionID=s.electionId \
        WHERE e.year > 2000 AND s.popularVoteRatio > 0.45 AND s.popularVoteRatio < 0.55'
    , (start_year, end_year))

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Return detailed info about cost and interactions for the specific campaign. 
@campaign_manager.route('/campaign-data/<campaignId>', methods=['GET'])
def get_campaign_details(campaign_id):
    current_app.logger.info(f'data_analyst_routes.py: GET /campaign/{campaign_id}/details')
    cursor = db.get_db().cursor()

    cursor.execute(' \
        SELECT SUM(a.interactions) as totalInteractions, \
    SUM(a.cost) as advertisementsCost, \
    SUM(r.actualAttendance) as totalAttendees, \
    SUM(r.cost) as ralliesCost \
    FROM campaign c JOIN advertisement a ON c.campaignId=a.campaignId \
               JOIN rally r ON r.campaignId=c.campaignId \
               WHERE c.campaignId = {0}'.format(campaign_id))

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Adding campaign manager feedback onto the website.

@campaign_manager.route('/campaign-site-survey', methods=['POST'])
def add_campaign_feedback(campaign_id):
    current_app.logger.info('POST /campaign-site-survey')
    campaign_survey = request.json
    discoveredWhere = campaign_survey['discoveredWhere']
    addAdditionalData = campaign_survey['addAdditionalData']
    isDataUseful = campaign_survey['isDataUseful']
    foundNeededInfo = campaign_survey['foundNeededInfo']
    isUserFriendly = campaign_survey['isUserFriendly']
    
    query = ' INSERT INTO campaignManagerSiteSurvey(discoveredWhere, addAdditionalData, isDataUseful, foundNeededInfo, \
                   isUserFriendly, campaignId) \
                    VALUES (%s, %s, %d, %d, %d, %d, %d, %d)'
    data = (discoveredWhere, addAdditionalData, isDataUseful, foundNeededInfo, isUserFriendly, campaign_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'campaign survey response submitted!'