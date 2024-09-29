from flask import Blueprint, jsonify, request
from weather.controllers import get_weather
from crop.controllers import get_seasonal_crops, get_recommended_crops

main_routes = Blueprint('main', __name__)

# For weather information -------------------------------------------------------------------------------

@main_routes.route('/weather', methods=['GET'])
def get_weather_info():
    lat = request.args.get('lat')
    lon = request.args.get('lon')
    return jsonify(get_weather(lat, lon))

# For seasonal crops -------------------------------------------------------------------------------

@main_routes.route('/seasonal_crops', methods=['GET'])  # Corrected route definition
def get_seasonal():
    # Retrieve the soil type from request parameters
    soil_type_input = request.args.get('soil_type')
    return jsonify(get_seasonal_crops(soil_type_input))

# For crop recommendations ---------------------------------------------------

@main_routes.route('/recommended_crops', methods=['GET'])  # Corrected route definition
def get_recommended():
    temperature = request.args.get('temp')
    humidity = request.args.get('humidity')

    # Retrieve the soil type from request parameters
    soil_type_input = request.args.get('soil_type')
    
    return jsonify(get_recommended_crops(temperature, humidity, soil_type_input))
