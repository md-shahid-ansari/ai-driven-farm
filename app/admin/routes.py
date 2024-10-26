from flask import Blueprint, jsonify
from app.admin.utils import get_crop_pattern, get_weather_forecast, match_pattern_n_save
from app.admin.controllers import get_data, forecast_n_save, fine_tune
from flask_cors import CORS

admin = Blueprint('admin', __name__)
CORS(admin)

# @admin.route('/predict', methods=['GET'])
def get_weather_data_n_predict_n_save():
    weather_history, weather_forecast = get_data()
    fine_tune(weather_forecast)
    forecast_n_save(data=weather_history)
    return jsonify("Done")


# @admin.route('/match', methods=['GET'])
def get_pattern_n_save():
    crops_dict = get_crop_pattern()
    weather_forecast = get_weather_forecast() 
    match_pattern_n_save(crops_dict, weather_forecast)
    return jsonify("Done")


@admin.route('/u', methods=['GET'])
def u():
    # Load your CSV file
    # df = pd.read_csv('D:/Hacks/ai-driven-farm/backend/app/Safflower.csv')

    # # Add the "Crop Name" column with a default value (e.g., "Wheat")
    # df['Crop Name'] = 'Safflower'  # Change 'Wheat' to the desired crop name

    # # Convert the DataFrame to a list of dictionaries
    # data_dict = df.to_dict(orient='records')
    # db = get_db()
    # db.crop_weather_pattern.insert_many(data_dict)
    
    # db = get_db()
    # db.crop_weather_pattern.update_many(
    # {},
    # {
    #     '$rename': {
    #         'Minimum Temperature (°C)': 'Min Temp',
    #         'Maximum Temperature (°C)': 'Max Temp',
    #         'Humidity (%)': 'Humidity',
    #         'Pressure (hPa)': 'Pressure',
    #         'Precipitation (mm)': 'Precipitation'
    #     }
    # })
    return jsonify("Done")