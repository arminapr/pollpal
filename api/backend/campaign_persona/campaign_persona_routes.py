from flask import Blueprint, request, jsonify, make_response, current_app
from backend.db_connection import db

campaign_manager = Blueprint('campaign_manager', __name__)

# Return a realtime ratio of voters to candidates for the current election 
@campaign_manager.route('/polling-data/<year>', methods=['GET'])
def get_voter_to_candidate_ratio(year):
    current_app.logger.info(f'campaign_persona_routes.py: GET /polling-data/{year}')
    cursor = db.get_db().cursor()

    cursor.execute(' \
        SELECT c.candidateId, c. firstName, c.lastName, c.politicalAffiliation, COUNT(voterID)as votes \
        FROM voter v JOIN candidate c ON v.candidateId=c.candidateId \
            JOIN ranIn r on r.candidateId=c.candidateId \
            JOIN election e on e.electionId =r.electionId \
            WHERE e.year = {0} \
            GROUP BY candidateID'.format(year))

    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Return swing states based on the state’s popular vote ratio across a period of years 
@campaign_manager.route('/swing-state', methods=['GET'])
def get_swing_states():
    current_app.logger.info('campaign_persona_routes.py: GET /swing-states')
    cursor = db.get_db().cursor()

    cursor.execute(' \
        SELECT DISTINCT stateAbbr, stateName, popularVoteRatio, partyRepresentative, numElectoralVotes, year \
        FROM election e JOIN stateResult s ON e.electionID=s.electionId \
        WHERE e.year > 1984 AND s.popularVoteRatio > 0.49 AND s.popularVoteRatio < 0.52')

    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Return detailed info about cost and interactions for the specific campaign. 
@campaign_manager.route('/campaign-data/<campaignId>', methods=['GET'])
def get_campaign_details(campaignId):
    current_app.logger.info(f'campaign_persona_routes.py: GET /campaign/{campaignId}/details')
    cursor = db.get_db().cursor()

    cursor.execute(' \
        SELECT SUM(a.interactions) as totalInteractions, \
            SUM(a.cost) as advertisementsCost, \
            SUM(r.actualAttendance) as totalAttendees, \
            SUM(r.cost) as ralliesCost \
            FROM campaign c JOIN advertisement a ON c.campaignId=a.campaignId \
               JOIN rally r ON r.campaignId=c.campaignId \
               WHERE c.campaignId = {0}'.format(campaignId))

    theData = cursor.fetchall()
    the_response = make_response(jsonify(theData))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response


# Adding campaign manager feedback onto the website.
@campaign_manager.route('/campaign-site-survey', methods=['POST'])
def add_campaign_feedback():
    current_app.logger.info('POST /campaign-site-survey')
    campaign_survey = request.json
    campaign_id = campaign_survey['campaignId']
    discoveredWhere = campaign_survey['discoveredWhere']
    addAdditionalData = campaign_survey['addAdditionalData']
    isDataUseful = 1 if campaign_survey['isDataUseful'] == 'True' else 0    
    foundNeededInfo = campaign_survey['foundNeededInfo']
    isUserFriendly = campaign_survey['isUserFriendly']
    
    query = ' INSERT INTO campaignManagerSiteSurvey(discoveredWhere, addAdditionalData, isDataUseful, foundNeededInfo, \
                   isUserFriendly, campaignId) \
                    VALUES (%s, %s, %s, %s, %s, %s)'
    data = (discoveredWhere, addAdditionalData, isDataUseful, foundNeededInfo, isUserFriendly, campaign_id)
    cursor = db.get_db().cursor()
    r = cursor.execute(query, data)
    db.get_db().commit()
    return 'campaign survey response submitted!'

# Routes to populate dropdown options
@campaign_manager.route('/campaign-ids', methods=['GET'])
def get_campaign_ids():
    current_app.logger.info('GET /campaign-ids')
    query = 'SELECT campaignId FROM campaign'  
    cursor = db.get_db().cursor()
    cursor.execute(query)
    campaign_ids = cursor.fetchall()
    return jsonify(campaign_ids)


@campaign_manager.route('/election-years', methods=['GET'])
def get_election_years():
    current_app.logger.info('GET /election-years')
    query = 'SELECT year FROM election ORDER BY year DESC'  
    cursor = db.get_db().cursor()
    cursor.execute(query)
    election_years = cursor.fetchall()
    return jsonify(election_years)
