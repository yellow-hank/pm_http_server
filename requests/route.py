from flask import Blueprint, request, current_app, jsonify
from .service import get_prob_single_sensor, get_specific_time_data
from flask_cors import cross_origin
from .route_planning import route_planning
from campus_display.service import get_time_limit, transform_timezone, get_recent_data

requesting = Blueprint("requesting", __name__, url_prefix="/requesting")

# Get the probability of green orange red
@requesting.route("/prob/<int:campus_id>", methods=["GET"])
@cross_origin()
def init(campus_id):
    try:
        data = get_prob_single_sensor(campus_id)
        return jsonify(data)
    except AttributeError as err:
        current_app.logger.info(err)
        result = "The request may not have the header of application/json"
        return result, 400



# Get 8am 12pm 6pm pm25 data for each sensor
@requesting.route("/specific/<int:campus_id>", methods=["GET"])
@cross_origin()
def specific(campus_id):
    try:
        data = get_specific_time_data(campus_id)
        return jsonify(data)
    except AttributeError as err:
        current_app.logger.info(err)
        result = "The request may not have the header of application/json"
        return result, 400

@requesting.route("/route_cal/<float:start_lat>/<float:start_lng>/<float:end_lat>/<float:end_lng>", methods=["GET"])
@cross_origin()
def route_cal(start_lat,start_lng,end_lat,end_lng):
    try:
        # result=[]
        # result.append(start_lat)
        # result.append(start_lng)
        # result.append(end_lat)
        # result.append(end_lng)
        #pm25_list = [46, 45.5, 42, 42, 42.5, 42, 40, 38.5]
        pm25_list=[]
        upper, lower = get_time_limit()
        taiwan_aware = transform_timezone(upper)
     # Unpack the dict to pass it to the function
        for i in range(8):
            data = get_recent_data(i, upper, lower)
            #pm25_list.append(int(data.get('avg_pm25')))


        result = route_planning(start_lat,start_lng,end_lat,end_lng,pm25_list)
        format_result=[]
        for i in result:
            format_result.append({'lng':i[1], 'lat':i[0]})
        return jsonify(format_result)
    except AttributeError as err:
        current_app.logger.info(err)
        result = "The request may not have the header of application/json"
        return result, 400
  
