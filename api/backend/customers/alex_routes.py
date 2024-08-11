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
        SELECT 
            (SELECT COUNT(*) FROM voter WHERE election_id = e.id) AS voter_count, 
            (SELECT COUNT(*) FROM candidate WHERE election_id = e.id) AS candidate_count 
        FROM election e 
        WHERE e.active = TRUE 
        LIMIT 1
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
        SELECT 
            s.name, 
            AVG(er.popular_vote_ratio) as avg_ratio 
        FROM state s 
        JOIN election_result er ON er.state_id = s.id 
        WHERE er.year BETWEEN %s AND %s 
        GROUP BY s.name 
        HAVING AVG(er.popular_vote_ratio) BETWEEN 0.45 AND 0.55
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
        SELECT 
            c.name as campaign_name, 
            c.description as campaign_description, 
            COALESCE(ct.cost_details, '[]') as costs, 
            COALESCE(it.interaction_details, '[]') as interactions 
        FROM campaign c
        LEFT JOIN (
            SELECT campaign_id, 
            JSON_AGG(JSON_BUILD_OBJECT('description', description, 'amount', amount)) as cost_details 
            FROM cost 
            WHERE campaign_id = %s 
            GROUP BY campaign_id
        ) ct ON ct.campaign_id = c.id
        LEFT JOIN (
            SELECT campaign_id, 
            JSON_AGG(JSON_BUILD_OBJECT('type', type, 'date', date)) as interaction_details 
            FROM interaction 
            WHERE campaign_id = %s 
            GROUP BY campaign_id
        ) it ON it.campaign_id = c.id
        WHERE c.id = %s
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
        INSERT INTO feedback (campaign_id, manager_name, feedback_text, date) 
        VALUES (%s, %s, %s, %s)
    , (campaign_id, manager_name, feedback_text, feedback_date))

    db.get_db().commit()

    the_response = make_response(jsonify({"message": "Feedback added successfully!"}))
    the_response.status_code = 201
    the_response.mimetype = 'application/json'
    return the_response

