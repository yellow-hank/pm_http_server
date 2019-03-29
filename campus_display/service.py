from datetime import datetime, timedelta
from flask import current_app
import pytz
from errors import QueryNotFound

# Get the most recent data in the given position
# pos : The ID of the sensor to be queried
# Return value : The jsonified data that is ready to be sent, 404 if any error occured
def get_recent_data(pos, upper, lower):
    try:
        from flask_server import MONGO
        # current_app.logger.info(upper)
        # current_app.logger.info(lower)
        target_data = MONGO.db.pm_data
        # Find data between lower bound time and upper bound time
        return_data = list(target_data.find({
                '$and': [
                    {
                        'position': pos
                    },
                    {
                        'date': {
                            '$gte': lower,
                            '$lte': upper
                        }
                    }
                ]
        }))
        # How many documents in this query
        data_count = len(return_data)
        current_app.logger.info(data_count)
        if data_count == 0:
            raise QueryNotFound
        sum_pm25 = 0
        sum_temp = 0
        sum_humidity = 0
        for doc in return_data:
            sum_pm25 += doc.get('pm25', 0)
            sum_temp += doc.get('temp', 0)
            sum_humidity += doc.get('humidity', 0)
        return {
            'avg_pm25': round((sum_pm25 / data_count), 2),
            'avg_temp': round((sum_temp / data_count), 2),
            'avg_humidity': round((sum_humidity / data_count), 2)
        }
    except QueryNotFound as err:
        current_app.logger.info(err)
        # return the placeholder data
        return {
            'avg_pm25': 0,
            'avg_temp': 0,
            'avg_humidity': 0
        }
def get_time_limit():
    half = timedelta(minutes=30)
    # Get the utc time which is unaware of the timezone
    cur = datetime.utcnow()
    current_app.logger.info(cur)
    # Determine which interval cur is currently in
    # 0 ~ 29 or 30 ~ 59
    if cur.minute < 30:
        time_d = timedelta(minutes=cur.minute, seconds=cur.second)
    else:
        time_d = timedelta(minutes=(cur.minute - 30), seconds=cur.second)
    upper = cur - time_d
    lower = cur - time_d - half
    return upper, lower
