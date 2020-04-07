from flask import Blueprint, request, current_app, jsonify
from .service import get_prob_single_sensor

requesting = Blueprint("requesting", __name__, url_prefix="/requesting")

# Get the probability of green orange red
@requesting.route("/prob/<int:campus_id>", methods=["GET"])
def init(campus_id):
  try:
    data = get_prob_single_sensor(campus_id)
    return jsonify(data)
  except AttributeError as err:
    current_app.logger.info(err)
    result = "The request may not have the header of application/json"
    return result, 400
