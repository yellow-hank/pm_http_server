from datetime import datetime, timedelta
from flask import Blueprint, request, current_app, jsonify
import pytz
from .service import get_recent_data, get_time_limit, get_two_weeks_data, get_two_weeks_time_limit, transform_timezone

campus_display = Blueprint("campus_display", __name__, url_prefix="/campus")

@campus_display.route("/<int:campus_id>", methods=["GET"])
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

@campus_display.route('/display/<int:position>', methods=['GET'])
def display(position):
    upper, lower = get_two_weeks_time_limit()
    # taiwan_aware = transform_timezone(upper)
    data = get_two_weeks_data(position, upper, lower)
    current_app.logger.info(f"position: { position }")
    return jsonify(data)

