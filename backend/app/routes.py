from flask import Blueprint, jsonify, request
from app.controllers import get_zones, get_current_zone, get_crops , get_crop_pattern, get_weather_forecast, match_pattern_n_save, get_soils
from app.model.controllers import get_data, forecast_n_save, fine_tune

main_routes = Blueprint('main', __name__)

# For zone information -------------------------------------------------------------------------------

@main_routes.route('/current_zone', methods=['GET'])
def get_zones_curr():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    zone = get_current_zone(lat, lon)
    return jsonify(zone)

@main_routes.route('/zones', methods=['GET'])
def get_zones_all():
    return jsonify(get_zones())

@main_routes.route('/soils', methods=['GET'])
def get_soil_all():
    return jsonify(get_soils())


# For crops -------------------------------------------------------------------------------

@main_routes.route('/crops', methods=['GET'])  # Corrected route definition
def get_seasonal():
    # Retrieve the soil type from request parameters
    zoneId = request.args.get('zone_id')
    return jsonify(get_crops(zoneId))


# @main_routes.route('/predict', methods=['GET'])
def get_weather_data_n_predict_n_save():
    weather_history, weather_forecast = get_data()
    fine_tune(weather_forecast)
    forecast_n_save(data=weather_history)
    return jsonify("Done")


# @main_routes.route('/match', methods=['GET'])
def get_pattern_n_save():
    crops_dict = get_crop_pattern()
    weather_forecast = get_weather_forecast() 
    match_pattern_n_save(crops_dict, weather_forecast)
    return jsonify("Done")


# @main_routes.route('/u', methods=['GET'])
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
