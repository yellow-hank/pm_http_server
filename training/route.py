from flask import Blueprint, request, current_app, jsonify
from .service import get_whole_data

training = Blueprint("training", __name__, url_prefix="/training")

# Getting whole data for training
@training.route("/<int:campus_id>", methods=["GET"])
def init(campus_id):
  data = get_whole_data(campus_id)
  return jsonify(data)