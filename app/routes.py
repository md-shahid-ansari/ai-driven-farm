from flask import Blueprint, jsonify
from app.utils import get_crop_pattern, get_weather_forecast, match_pattern_n_save
from app.controllers import get_data, forecast_n_save, fine_tune
from flask_cors import CORS
from app import get_db
from bson.json_util import dumps

admin = Blueprint('admin', __name__)
CORS(admin)

@admin.route('/', methods=['GET'])
def _():
    return jsonify("Admin")

@admin.route('/predict', methods=['GET'])
def get_weather_data_n_predict_n_save():
    weather_history, weather_forecast = get_data()
    fine_tune(weather_forecast)
    forecast_n_save(data=weather_history)
    return jsonify("Done")


@admin.route('/match', methods=['GET'])
def get_pattern_n_save():
    crops = get_crop_pattern()
    weather_forecast = get_weather_forecast() 
    match_pattern_n_save(crops, weather_forecast)
    return jsonify("Done")


# sample route to perform some basic operations
@admin.route('/u', methods=['GET'])
def u():
    db = get_db()
    
    stages_data = [
        {
            "Stage": "Germination",
            "Days": 7,
            "Min Temp": 20,
            "Max Temp": 30,
            "Humidity": 70,
            "Precipitation": 7,
            "Stage Rank": 1
        },
        {
            "Stage": "Vegetative Growth",
            "Days": 60,
            "Min Temp": 18,
            "Max Temp": 30,
            "Humidity": 70,
            "Precipitation": 8.4,
            "Stage Rank": 2
        },
        {
            "Stage": "Flowering/Fruiting",
            "Days": 50,
            "Min Temp": 20,
            "Max Temp": 30,
            "Humidity": 70,
            "Precipitation": 4,
            "Stage Rank": 3
        },
        {
            "Stage": "Maturity/Harvest",
            "Days": 15,
            "Min Temp": 18,
            "Max Temp": 30,
            "Humidity": 60,
            "Precipitation": 3.4,
            "Stage Rank": 4
        }
    ]

    # Update the crop document by name
    result = db.crops.update_one(
        {"Crop Name": "Chili Pepper"},
        {"$set": {"Stages": stages_data}}
    )

    # Optional logging
    if result.matched_count:
        print(f"Updated stages for 'Chili Pepper'.")
    else:
        print(f"No document found for 'Chili Pepper'.")
    return dumps("done")