import requests
import time
import datetime
import csv

# Constants
API_KEY = '8ae233758d7844fbad56b365a8a1e4ac'
BASE_URL = 'https://api.weatherbit.io/v2.0/history/subhourly'
LAT = '35.78'
LON = '-78.64'
CSV_FILE = 'weather_data.csv'

# Date range
start_year = 2020
end_year = 2024

# Initialize CSV file
with open(CSV_FILE, mode='w', newline='') as file:
    writer = csv.writer(file)
    # Write header
    writer.writerow(['Timestamp', 'Temperature', 'Precipitation', 'Wind Speed', 'Pressure', 'Humidity'])

    for year in range(start_year, end_year + 1):
        for day in range(1, 366):
            try:
                date = datetime.datetime(year, 1, 1) + datetime.timedelta(days=day - 1)
                start_date = date.strftime('%Y-%m-%d')
                end_date = (date + datetime.timedelta(days=1)).strftime('%Y-%m-%d')
                url = f"{BASE_URL}?lat={LAT}&lon={LON}&start_date={start_date}&end_date={end_date}&key={API_KEY}"
                
                # Make the API request
                response = requests.get(url)
                if response.status_code == 200:
                    json_data = response.json()
                    for entry in json_data.get('data', []):
                        timestamp = entry.get('timestamp_local')
                        temp = entry.get('temp')
                        precip = entry.get('precip')
                        wind_speed = entry.get('wind_spd')
                        pressure = entry.get('pres')
                        humidity = entry.get('rh')
                        # Write data row
                        writer.writerow([timestamp, temp, precip, wind_speed, pressure, humidity])
                else:
                    print(f"Failed to retrieve data for {start_date}")
                
                # Pause to respect rate limits
                # time.sleep(1)
            
            except Exception as e:
                print(f"Error on {start_date}: {e}")


# import pandas as pd
# import joblib

# # Load the trained model
# model = joblib.load('crop_recommendation_model.pkl')

# # Function to recommend crops based on temperature and humidity
# def recommend_crops(temperature, humidity, top_n=3):
#     # Create a DataFrame with the input features
#     input_data = pd.DataFrame({'Temperature_y': [temperature], 'Humidity_y': [humidity]})
    
#     # Get the prediction probabilities for each class
#     probabilities = model.predict_proba(input_data)[0]
    
#     # Get the class labels
#     class_labels = model.classes_
    
#     # Create a DataFrame with the class labels and their corresponding probabilities
#     prob_df = pd.DataFrame({'Crop': class_labels, 'Probability': probabilities})
    
#     # Sort the DataFrame by probability in descending order and get the top N recommendations
#     top_recommendations = prob_df.sort_values(by='Probability', ascending=False).head(top_n)
    
#     return top_recommendations

# # Example usage
# temperature = 35.6
# humidity = 80
# recommended_crops = recommend_crops(temperature, humidity, top_n=20)
# print(f"Recommended crops for temperature {temperature}°C and humidity {humidity}%:\n{recommended_crops}")