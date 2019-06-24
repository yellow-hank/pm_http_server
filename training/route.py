from flask import Blueprint, request, current_app, jsonify
from .service import get_whole_data

training = Blueprint("training", __name__, url_prefix="/training")

# Getting whole data for training
@training.route("", methods=["GET"])
def init():
  try:
    data = get_whole_data()
    return jsonify(data)
  except AttributeError as err:
    current_app.logger.info(err)
    result = "The request may not have the header of application/json"
    return result, 400
