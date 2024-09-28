from flask import Flask, request, jsonify
from flask_cors import CORS

from weather.controllers import get_weather
from crop.controllers import get_seasonal_crops,get_recommended_crops

app = Flask(__name__)
CORS(app)


@app.route('/weather', methods=['GET'])
def get_weather_info():
    lat = request.args.get('lat')
    lon = request.args.get('lon')

    return jsonify(get_weather(lat, lon))


#for seasonal crop -------------------------------------------------------------------------------

@app.route('/seasonal_crops', methods=['GET'])
def get_seasonal():
    # Retrieve the soil type from request parameters
    soil_type_input = request.args.get('soil_type')

    return jsonify(get_seasonal_crops(soil_type_input))



#for recommendations---------------------------------------------------

@app.route('/recommended_crops', methods=['GET'])
def get_recommended():

    temperature = request.args.get('temp')
    humidity = request.args.get('humidity')

    # Retrieve the soil type from request parameters
    soil_type_input = request.args.get('soil_type')
    
    return jsonify(get_recommended_crops(temperature, humidity, soil_type_input))    
   


if __name__ == '__main__':
    app.run(debug=True)