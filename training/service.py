from flask import current_app
from errors import QueryNotFound

def get_whole_data(pos):
  try:
      # prevent circular import
      from flask_server import MONGO
      target_data = MONGO.db.pm_data
      recentData = list(target_data.find({}))
      # No data is found
      if len(recentData) == 0:
          raise QueryNotFound
      return recentData
  except QueryNotFound as err:
      current_app.logger.info(err)
      # return the an empty arr
      return []