from app import get_db
db = get_db()
import requests
import os
from flask import jsonify
from dotenv import load_dotenv
load_dotenv()
import pandas as pd
import numpy as np
from tslearn.metrics import dtw
from datetime import timedelta



def get_zones():
    try:
        # Fetch all documents from the collection
        zones_cursor = db.weather_zones.find({}, {'Zone': 1})
        zones = [zone['Zone'] for zone in zones_cursor]  # Extract only the 'Zone' field
        return zones
    except Exception as e:
        print(f"An error occurred while fetching zones: {e}")
        return []

def get_current_zone(lat, lon):
    try:
        # Convert input lat/lon to float
        lat = float(lat)
        lon = float(lon)

        # Fetch all zones with their latitude and longitude ranges
        zones_cursor = db.weather_zones.find({}, {'Zone': 1, 'Latitude Range': 1, 'Longitude Range': 1})
        
        for zone in zones_cursor:
            # Assuming Latitude Range and Longitude Range are strings like "30.0°N - 37.0°N"
            lat_range = zone['Latitude Range']
            lon_range = zone['Longitude Range']
            
            # Parse the latitude range
            lat_min, lat_max = map(float, [lat_range.split(' - ')[0][:-2], lat_range.split(' - ')[1][:-2]])  # Exclude '°N'
            lat_min = -lat_min if 'S' in lat_range else lat_min  # Convert to negative if 'S' (South)
            lat_max = -lat_max if 'S' in lat_range else lat_max
            
            # Parse the longitude range
            lon_min, lon_max = map(float, [lon_range.split(' - ')[0][:-2], lon_range.split(' - ')[1][:-2]])  # Exclude '°E'
            lon_min = -lon_min if 'W' in lon_range else lon_min  # Convert to negative if 'W' (West)
            lon_max = -lon_max if 'W' in lon_range else lon_max

            # Check if the provided lat/lon are within the range
            if lat_min <= lat <= lat_max and lon_min <= lon <= lon_max:
                return zone['Zone']  # Return the zone name
        
        return None  # Return None if no zone matches
    except Exception as e:
        print(f"An error occurred while fetching the current zone: {e}")
        return None



WEATHER_MAP_API_KEY = os.getenv('WEATHER_MAP_API_KEY', '')
WEATHER_MAP_URL = os.getenv('WEATHER_MAP_URL', 'http://api.openweathermap.org/data/2.5')

def get_weather(lat, lon):
    weather_url = f'{WEATHER_MAP_URL}/weather?lat={lat}&lon={lon}&appid={WEATHER_MAP_API_KEY}&units=metric'
    response = requests.get(weather_url)
    return response.json()


def get_crops(soil_type):
    return jsonify(soil_type)
    

def get_crop_pattern():
    crops_pattern = db.crop_weather_pattern.find()
    # Create a dictionary to store crop weather patterns
    crops_dict = {}
    
    # Iterate over the crop patterns
    for entry in crops_pattern:
        
        crop_name = entry.get('Crop Name')  # Fetch the crop name
        day = entry.get('Day')  # Fetch the day
        growth_stage = entry.get('Growth Stage')  # Fetch the growth stage
        weather_data = {
            'Day': day,
            'Growth Stage': growth_stage,
            'Humidity': entry.get('Humidity'),
            'Max Temp': entry.get('Max Temp'),
            'Min Temp': entry.get('Min Temp'),
            'Precipitation': entry.get('Precipitation'),
            'Pressure': entry.get('Pressure')
        }
        
        # Initialize the crop entry if not already present
        if crop_name not in crops_dict:
            crops_dict[crop_name] = []
        
        # Append the weather data for that day
        crops_dict[crop_name].append(weather_data)
    
    return crops_dict

def format_weather_data(weather_data):
    """Helper function to format a single weather document."""
    return {
        'Date': weather_data['Date'],  # Formatting date to YYYY-MM-DD - weather_data['Date'].strftime('%Y-%m-%d')
        'Min Temp': weather_data['Min Temp'],
        'Max Temp': weather_data['Max Temp'],
        'Humidity': weather_data['Humidity'],
        'Pressure': weather_data['Pressure'],
        'Precipitation': weather_data['Precipitation']
    }


def get_weather_forecast(ZoneId = 6):
    weather_forecast = []
    # Fetch previous weather forecasts from MongoDB
    weather_forecast_cursor = db.weather_forecast.find({
        "ZoneId": ZoneId
    })
    for weather in weather_forecast_cursor:
        formatted_data = format_weather_data(weather)
        weather_forecast.append(formatted_data)

    features = ['Date', 'Min Temp', 'Max Temp', 'Humidity', 'Pressure', 'Precipitation']
    data = pd.DataFrame(weather_forecast,columns=features)
    return data

def match_pattern_n_save(crops_dict, weather_forecast):
    features = ['Min Temp', 'Max Temp', 'Humidity', 'Pressure', 'Precipitation']
    growth_column = ['Day','Growth Stage']
    forecast = pd.DataFrame(weather_forecast,columns=features)
    df_forecast = np.round(forecast, 1)
    
    for name , pattern in crops_dict.items():
        df_pattern = pd.DataFrame(pattern, columns=features)

        best_start, min_distance = match_pattern(df_forecast,df_pattern)

        # take data to stre
        best_start_date = weather_forecast['Date'].iloc[best_start]

        pattern_stages = pd.DataFrame(pattern, columns=growth_column) 
        growth_stage_counts = pattern_stages['Growth Stage'].value_counts()
        current_date = best_start_date
        growth_stage = []
        for stage, count in growth_stage_counts.items():
            stage_start_date = current_date
            stage_end_date = current_date + timedelta(days=count - 1)  # Count - 1 because we include the start day
            
            # Append the stage, start date, end date, and count with date in "DD-MM-YYYY" format
            growth_stage.append([
                stage,
                stage_start_date.strftime('%d-%m-%Y'),  # Format date as "DD-MM-YYYY"
                stage_end_date.strftime('%d-%m-%Y'),    # Format date as "DD-MM-YYYY"
                count
            ])
            # Move the current_date to the next day after the current stage's end date
            current_date = stage_end_date + timedelta(days=1)

        crop = db.crops.find_one({'Crop Name' : name})
        # Add the additional fields to the crop data
        crop_predicted = crop.copy()  # Make a copy of the original crop document

        # Drop specified fields
        fields_to_drop = [
            '_id', 
            'Temperature', 
            'Soil Type', 
            'Humidity', 
            'Wind Speed', 
            'Planting Dates', 
            'Harvesting Dates'
        ]

        for field in fields_to_drop:
            crop_predicted.pop(field, None)  # Remove the field if it exists


        # Convert the growth stage data into a more usable format (e.g., a list of dictionaries)
        formatted_growth_stage = []
        for stage in growth_stage:
            stage_data = {
                'Stage': stage[0],
                'Start Date': stage[1],
                'End Date': stage[2],
                'Duration': stage[3]
            }
            formatted_growth_stage.append(stage_data)

        # Add new fields
        crop_predicted['ZoneId'] = 6
        crop_predicted['Growth Stage'] = formatted_growth_stage  # Add the formatted growth stages
        crop_predicted['Season'] = best_start_date.strftime('%Y')  # Convert current date to year (full)
        crop_predicted['DTW'] = round(min_distance)

        # Prepare the filter for checking existence
        filter_condition = {
            'Crop Name': crop_predicted['Crop Name'],
            'ZoneId': crop_predicted['ZoneId'],
            'Season': crop_predicted['Season']
        }

        # Attempt to update the document if it exists, otherwise insert a new one
        result = db.crops_predicted.update_one(
            filter_condition,
            {'$set': crop_predicted},  # Update with new data
            upsert=True  # If the document doesn't exist, insert a new one
        )

        if result.matched_count > 0:
            print(f"{name} - Data updated successfully in crops_predicted collection.")
        else:
            print(f"{name} - Data inserted successfully into crops_predicted collection.")
    return
    
# Function to match crop weather with weather data
def match_pattern(weather_features, crop_data):
    # Compute DTW distance for each subsequence in weather data (window size = length of crop_data)
    min_distance = float('inf')
    best_start = None

    for i in range(len(weather_features)):
        subsequence = circular_slice(weather_features, i, len(crop_data))
        
        # Calculate DTW distance between crop requirements and subsequence of weather data
        distance = dtw(subsequence, crop_data)
        
        # Find the subsequence with the minimum distance
        if distance < min_distance:
            min_distance = distance
            best_start = i
    return best_start, min_distance

# Function to create circular subsequences from weather data
def circular_slice(array, start, length):
    """ Slices array circularly from 'start' for 'length' elements. """
    n = len(array)
    end = (start + length) % n  # Circular end position
    if start < end:
        return array[start:end]
    else:
        # If it wraps around, concatenate two slices (end wraps around to the start)
        return np.concatenate((array[start:], array[:end]), axis=0)