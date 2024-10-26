from flask import Blueprint, jsonify, request
from app.controllers import get_zones, get_current_zone, get_crops , get_soils


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

