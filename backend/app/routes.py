from flask import Blueprint, jsonify, request
from weather.controllers import get_weather
from crop.controllers import get_seasonal_crops, get_recommended_crops
from app.controllers import get_zones, get_current_zone

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
