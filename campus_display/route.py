from datetime import datetime, timedelta
from flask import Blueprint, request, current_app, jsonify
import pytz
from .service import get_recent_data, get_time_limit

campus_display = Blueprint("campus_display", __name__, url_prefix="/campus")

@campus_display.route("/<int:campus_id>", methods=["GET"])
def get_partial_data(campus_id):
    try:
        convert_to_taiwan = timedelta(hours=8)
        upper, lower = get_time_limit()
        current_app.logger.info(campus_id)
        # Unpack the dict to pass it to the function
        data = get_recent_data(campus_id, upper, lower)
        # Append time on each data
        avg_pm25 = {
            'data': data.get('avg_pm25'),
            'time': upper + convert_to_taiwan
        }
        avg_temp = {
            'data': data.get('avg_temp'),
            'time': upper + convert_to_taiwan
        }
        avg_humidity = {
            'data': data.get('avg_humidity'),
            'time': upper + convert_to_taiwan
        }
        return jsonify(avg_pm25=avg_pm25, avg_temp=avg_temp, avg_humidity=avg_humidity)
    except AttributeError as err:
        current_app.logger.info(err)
        result = "The request may not have the header of application/json"
        return result, 400

@campus_display.route('/init/<int:campus_id>', methods=["GET"])
def init(campus_id):
    try:
        taiwan_timezone = 'Asia/Taipei'
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
            # Make the datetime object aware of the timezone
            # tzinfo=None can be specified to create a naive datetime
            # from an aware datetime with no conversion of date and time data.
            utc_aware = utc_unaware.replace(tzinfo=pytz.utc)
            # Convert this utc time to taiwan local time
            taiwan_aware = utc_aware.astimezone(pytz.timezone(taiwan_timezone))
            current_app.logger.info(f'utc_unaware: {utc_unaware}')
            current_app.logger.info(f'utc_aware: {utc_aware}')
            current_app.logger.info(f'taiwan_aware: {taiwan_aware}')
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
