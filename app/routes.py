from flask import Blueprint, jsonify
from app.utils import get_crop_pattern, get_weather_forecast, match_pattern_n_save
from app.controllers import get_data, forecast_n_save, fine_tune
from flask_cors import CORS
from app import get_db
from bson.json_util import dumps
import pandas as pd

admin = Blueprint('admin', __name__)
CORS(admin)

@admin.route('/', methods=['GET'])
def _():
    return jsonify("Admin")

# @admin.route('/predict', methods=['GET'])
def get_weather_data_n_predict_n_save():
    weather_history, weather_forecast = get_data()
    fine_tune(weather_forecast)
    forecast_n_save(data=weather_history)
    return jsonify("Done")


# @admin.route('/match', methods=['GET'])
def get_pattern_n_save():
    crops = get_crop_pattern()
    weather_forecast = get_weather_forecast() 
    match_pattern_n_save(crops, weather_forecast)
    return jsonify("Done")


@admin.route('/u', methods=['GET'])
def u():
    db = get_db()
    data = get_weather_forecast()
    return dumps(data)