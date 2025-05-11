from app import get_db
db = get_db()
import pandas as pd
import numpy as np
from tslearn.metrics import dtw
from datetime import timedelta

def get_crop_pattern():
    crops = db.crops.find({"Stages": {"$exists": True}})
    result = []
    for crop in crops:
        crop.pop("_id", None)  # remove _id
        result.append(crop)
    return result


def format_weather_data(weather_data):
    """Helper function to format a single weather document."""
    return {
        'Date': weather_data['Date'],  # Formatting date to YYYY-MM-DD - weather_data['Date'].strftime('%Y-%m-%d')
        'Min Temp': weather_data['Min Temp'],
        'Max Temp': weather_data['Max Temp'],
        'Humidity': weather_data['Humidity'],
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

    features = ['Date', 'Min Temp', 'Max Temp', 'Humidity', 'Precipitation']
    data = pd.DataFrame(weather_forecast,columns=features)
    return data


def match_pattern_n_save(crops, weather_forecast):
    forecast = np.round(weather_forecast, 1)
    
    for crop in crops:
        best_start, min_distance = match_pattern(forecast,crop)
        
        # take data to stre
        best_start_date = weather_forecast['Date'].iloc[best_start]

        current_date = best_start_date
        growth_stage = []
        for stage in crop["Stages"]:
            stage_start_date = current_date
            
            # Append the stage, start date, end date, and count with date in "DD-MM-YYYY" format
            growth_stage.append([
                stage["Stage"],
                stage_start_date.strftime('%d-%m-%Y'),  # Format date as "DD-MM-YYYY"
                stage["Days"]
            ])
            # Move the current_date to the next day after the current stage's end date
            current_date = current_date + timedelta(days=stage["Days"])
        
        # Add the additional fields to the crop data
        crop_predicted = crop.copy()  # Make a copy of the original crop document

        # Drop specified fields
        fields_to_drop = [
            '_id', 
            'Stages', 
        ]

        for field in fields_to_drop:
            crop_predicted.pop(field, None)  # Remove the field if it exists


        # Convert the growth stage data into a more usable format (e.g., a list of dictionaries)
        formatted_growth_stage = []
        for stage in growth_stage:
            stage_data = {
                'Stage': stage[0],
                'Start Date': stage[1],
                'Duration': stage[2]
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
        result = db.crops_prediction.update_one(
            filter_condition,
            {'$set': crop_predicted},  # Update with new data
            upsert=True  # If the document doesn't exist, insert a new one
        )

        if result.matched_count > 0:
            print(f"{crop_predicted['Crop Name']} - Data updated successfully in crops_prediction collection.")
        else:
            print(f"{crop_predicted['Crop Name']} - Data inserted successfully into crops_prediction collection.")
    return

# Function to match crop weather with weather data
def match_pattern(weather_features, crop_data):
    # Compute DTW distance for each subsequence in weather data (window size = length of crop_data)
    min_distance = float('inf')
    best_start = None

    for i in range(len(weather_features)):
        length = 0
        for stages in crop_data["Stages"]:
            length += stages["Days"]

        subsequence = circular_df_slice(weather_features, i, length)

        # Calculate DTW distance between crop requirements and subsequence of weather data
        window = 0
        distance = 0
        try:
            for stages in crop_data["Stages"]:
                days = stages["Days"]
                min_temp = stages["Min Temp"]
                max_temp = stages["Max Temp"]
                humidity = stages["Humidity"]
                precipitation = stages["Precipitation"]

                window += days
                min_temps = subsequence['Min Temp'].loc[window - days:window].sum()
                max_temps = subsequence['Max Temp'].loc[window - days:window].sum()
                humiditys = subsequence['Humidity'].loc[window - days:window].sum()
                precipitations = subsequence['Precipitation'].loc[window - days:window].sum()

                diff_min_temp = abs(min_temp - min_temps/days)
                diff_max_temp = abs(max_temp - max_temps/days)
                diff_humidity = abs(humidity - humiditys/days)
                diff_precipitation = abs(precipitation - precipitations/days)

                sum = diff_min_temp + diff_max_temp + diff_humidity + diff_precipitation
                distance += sum / 4
        except Exception as e:
            print(f"Error calculating DTW for start index: {i}")
            continue
        # print(f"Distance: {distance} for start index: {i}")

        # Find the subsequence with the minimum distance
        if distance < min_distance:
            min_distance = distance
            best_start = i
    return best_start, min_distance

# Function to create circular subsequences from weather data
def circular_df_slice(df, start, length):
    """
    Circularly slices a DataFrame from 'start' index for 'length' rows.
    """
    n = len(df)
    end = (start + length) % n
    if start < end:
        return df.iloc[start:end]
    else:
        # Wrap around: take from start to end
        return pd.concat([df.iloc[start:], df.iloc[:end]], axis=0).reset_index(drop=True)
