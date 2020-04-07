from flask import current_app
from errors import QueryNotFound

def get_prob_single_sensor(campus_id):
  try:
      # prevent circular import
      from flask_server import MONGO
      target_data = MONGO.db.pm_data
      recentData = list(target_data.find({'position': campus_id}))
      # No data is found
      if len(recentData) == 0:
          raise QueryNotFound
      return len(recentData)
  except QueryNotFound as err:
      current_app.logger.info(err)
      # return the an empty arr
      return []