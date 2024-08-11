from flask import Blueprint, request, jsonify, make_response, current_app
import json
from backend.db_connection import db
from backend.ml_models.model01 import predict

# Return a realtime ratio of voters to candidates for the current election
@data_analyst.route('/voting/ratio', methods=['GET'])
def get_voter_to_candidate_ratio():
    current_app.logger.info('data_analyst_routes.py: GET /voting/ratio')
    cursor = db.get_db().cursor()

    cursor.execute('
        SELECT candidateId, COUNT(voterID)as votes
        FROM voter v JOIN candidate c ON v.candidateId=c.candidateId
            JOIN ranIn r on r.candidateId=c.candidateId
            JOIN election e on e.electionId =r.electionId
            WHERE e.year = 2024
            GROUP BY candidateID;
    ')

    row_headers = [x[0] for x in cursor.description]
    json_data = []
    theData = cursor.fetchall()
    for row in theData:
        json_data.append(dict(zip(row_headers, row)))
    the_response = make_response(jsonify(json_data))
    the_response.status_code = 200
    the_response.mimetype = 'application/json'
    return the_response

    voter_count = theData[0]
    candidate_count = theData[1]


    ratio = voter_count / candidate_count
    return jsonify({"voter_to_candidate_ratio": ratio})


# Return swing states based on the state’s popular vote ratio across a period of years (from 2.

@data_analyst.route('/swing-states', methods=['GET'])
def get_swing_states():
    current_app.logger.info('data_analyst_routes.py: GET /swing-states')
    cursor = db.get_db().cursor()

    start_year = request.args.get('start_year')
    end_year = request.args.get('end_year')

    cursor.execute('
        SELECT DISTINCT stateAbbr 
        FROM election e JOIN stateResult s ON e.electionID=s.electionId
        WHERE e.year > 2000 AND s.popularVoteRatio > 0.45 AND s.popularVoteRatio < 0.55;
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
@data_analyst.route('/campaign/<int:campaign_id>/details', methods=['GET'])
def get_campaign_details(campaign_id):
    current_app.logger.info(f'data_analyst_routes.py: GET /campaign/{campaign_id}/details')
    cursor = db.get_db().cursor()

    cursor.execute('
        SELECT SUM(a.interactions) as totalInteractions,
    
    SUM(a.cost) as advertisementsCost,
    
    SUM(r.actualAttendance) as totalAttendees,
    
    SUM(r.cost) as ralliesCost
    FROM campaign c JOIN advertisement a ON c.campaignId=a.campaignId
               JOIN rally r ON r.campaignId=c.campaignId
               WHERE c.campaignId = 1; -- user input?
    , (campaign_id, campaign_id, campaign_id))

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

@data_analyst.route('/campaign/<int:campaign_id>/feedback', methods=['POST'])
def add_campaign_feedback(campaign_id):
    current_app.logger.info(f'data_analyst_routes.py: POST /campaign/{campaign_id}/feedback')
    cursor = db.get_db().cursor()

    feedback_data = request.get_json()
    manager_name = feedback_data.get('manager_name')
    feedback_text = feedback_data.get('feedback_text')
    feedback_date = feedback_data.get('date')

    cursor.execute('
        INSERT INTO campaignManagerSiteSurvey(discoveredWhere, addAdditionalData, isDataUseful, foundNeededInfo, isUserFriendly, createdAt, updatedAt, campaignId, campaignSurveyid)
VALUES ('friend', 'more campaign cost info', TRUE, 6, 3, 5, 3, 2);

    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Feedback added successfully!"}))
    the_response.status_code = 201
    the_response.mimetype = 'application/json'
    return the_response

