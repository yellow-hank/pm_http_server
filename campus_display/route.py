from datetime import datetime, timedelta
from flask import Blueprint, request, current_app, jsonify, send_file
import pytz
from .service import get_recent_data, get_time_limit, get_one_position_data, transform_timezone
from flask_cors import cross_origin
from .map import create_picture 

campus_display = Blueprint("campus_display", __name__, url_prefix="/campus")

@campus_display.route("/<int:campus_id>", methods=["GET"])
@cross_origin()
def get_partial_data(campus_id):
    try:
        upper, lower = get_time_limit()
        taiwan_aware = transform_timezone(upper)
        # Unpack the dict to pass it to the function
        data = get_recent_data(campus_id, upper, lower)
        # Append time on each data
        avg_pm25 = {
            'pm25': data.get('avg_pm25'),
            'time': taiwan_aware
        }
        avg_temp = {
            'temp': data.get('avg_temp'),
            'time': taiwan_aware
        }
        avg_humidity = {
            'humidity': data.get('avg_humidity'),
            'time': taiwan_aware
        }
        return jsonify(avg_pm25=avg_pm25, avg_temp=avg_temp, avg_humidity=avg_humidity)
    except AttributeError as err:
        current_app.logger.info(err)
        result = "The request may not have the header of application/json"
        return result, 400

@campus_display.route('/init/<int:campus_id>', methods=["GET"])
def init(campus_id):
    try:
        half = timedelta(minutes=30)
        upper, lower = get_time_limit()
        current_app.logger.info(campus_id)
        pm25 = []
        temp = []
        humidity = []
        # Get the data within 6 hours
        for i in range(12):
            utc_unaware = upper - (half * i)
            data = get_recent_data(campus_id, upper - (half * i), lower - (half * i))
            taiwan_aware = transform_timezone(utc_unaware)
            pm25.append({
                'pm25': data.get('avg_pm25'),
                'time': taiwan_aware
            })
            temp.append({
                'temp': data.get('avg_temp'),
                'time': taiwan_aware
            })
            humidity.append({
                'humidity': data.get('avg_humidity'),
                'time': taiwan_aware
            })
        return jsonify(pm25List=pm25, tempList=temp, humidityList=humidity)
    except AttributeError as err:
        current_app.logger.info(err)
        result = "The request may not have the header of application/json"
        return result, 400

@campus_display.route('/hour/<int:campus_id>', methods=["GET"])
def hour(campus_id):
    try:
        half = timedelta(minutes=60)
        upper, lower = get_time_limit()
        current_app.logger.info(campus_id)
        pm10 = []
        pm25 = []
        pm100 = []
        temp = []
        humidity = []
        # Get the data within 24 hours
        for i in range(24):
            utc_unaware = upper - (half * i)
            data = get_recent_data(campus_id, upper - (half * i), lower - (half * i))
            taiwan_aware = transform_timezone(utc_unaware)
	    #Change time format to "Year-Month-day Hour:minute:second"
	    taiwan_aware = taiwan_aware.strftime("%Y-%m-%d %H:%M:%S")
            pm10.append({
                'pm10': data.get('avg_pm10'),
                'time': taiwan_aware
            })
            pm25.append({
                'pm25': data.get('avg_pm25'),
                'time': taiwan_aware
            })
            pm100.append({
                'pm100': data.get('avg_pm100'),
                'time': taiwan_aware
            })
            temp.append({
                'temp': data.get('avg_temp'),
                'time': taiwan_aware
            })
            humidity.append({
                'humidity': data.get('avg_humidity'),
                'time': taiwan_aware
            })
        return jsonify(pm10List=pm10, pm25List=pm25, pm100List=pm100, tempList=temp, humidityList=humidity)
    except AttributeError as err:
        current_app.logger.info(err)
        result = "The request may not have the header of application/json"
        return result, 400

@campus_display.route('/day/<int:campus_id>', methods=["GET"])
def day(campus_id):
    try:
        half = timedelta(days=1)
        upper, lower = get_time_limit()
        current_app.logger.info(campus_id)
        pm10 = []
        pm25 = []
        pm100 = []
        temp = []
        humidity = []
        # Get the data within 1 week
        for i in range(7):
            utc_unaware = upper - (half * i)
            data = get_recent_data(campus_id, upper - (half * i), lower - (half * i))
            taiwan_aware = transform_timezone(utc_unaware)
            pm10.append({
                'pm10': data.get('avg_pm10'),
                'time': taiwan_aware
            })
            pm25.append({
                'pm25': data.get('avg_pm25'),
                'time': taiwan_aware
            })
            pm100.append({
                'pm100': data.get('avg_pm100'),
                'time': taiwan_aware
            })
            temp.append({
                'temp': data.get('avg_temp'),
                'time': taiwan_aware
            })
            humidity.append({
                'humidity': data.get('avg_humidity'),
                'time': taiwan_aware
            })
        return jsonify(pm10List=pm10, pm25List=pm25, pm100List=pm100, tempList=temp, humidityList=humidity)
    except AttributeError as err:
        current_app.logger.info(err)
        result = "The request may not have the header of application/json"
        return result, 400

@campus_display.route('/display/<int:position>', methods=['GET'])
def display(position):
    # upper, lower = get_two_weeks_time_limit()
    # taiwan_aware = transform_timezone(upper)
    data = get_one_position_data(position)
    current_app.logger.info(f"position: { position }")
    return jsonify(data)


@campus_display.route('/picture' , methods=['GET'])
def show_picture():
    pm25_list=[]
    upper, lower = get_time_limit()
    taiwan_aware = transform_timezone(upper)
    # Unpack the dict to pass it to the function
    for i in range(8):
        data = get_recent_data(i, upper, lower)
        pm25_list.append(data.get('avg_pm25'))
    create_picture(pm25_list)
    
    return send_file("../result.png", mimetype='image/png')

@campus_display.route('/get_file' , methods=['GET'])
@cross_origin()
def sendfile():
    return send_file("../yes.json", mimetype='application/json')
