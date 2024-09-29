import pandas as pd
from datetime import datetime
import joblib
import os
from dotenv import load_dotenv
load_dotenv()
from app import get_db

URL = os.getenv('PATH_TO_CROP', '/')

#for seasonal crop -------------------------------------------------------------------------------

# Load data from the CSV files and convert to dictionaries
soil_type_df = pd.read_csv(f'{URL}soil_type.csv')
crops_data_df = pd.read_csv(f'{URL}crops_data.csv')
# Convert to dictionaries
soil_type_dict = soil_type_df.to_dict(orient='records')
crops_data_dict = crops_data_df.to_dict(orient='records')


def get_seasonal_crops(soil_type_input):
    
    # Step 1: Find crops that match the given soil type
    matched_crops = []
    for entry in soil_type_dict:
        soil_types = entry['Soil Type'].split(',')
        for soil in soil_types :
            if soil.strip().lower() == soil_type_input.strip().lower():
                matched_crops.append(entry['Crops'])
            
    
    
    # Step 2: Filter crops data based on the matched crops and current season
    current_month = datetime.now().month
    recommendations = []

    for crop in crops_data_dict:
        if crop['Crop Name'] in matched_crops:
            # Check if the crop can be planted in the current season
            planting_dates = crop['Planting Dates'].split('-')
            harvesting_dates = crop['Harvesting Dates'].split('-')
            months = {
                "January": 1, "February": 2, "March": 3, "April": 4,
                "May": 5, "June": 6, "July": 7, "August": 8,
                "September": 9, "October": 10, "November": 11, "December": 12
            }
            start_month = months[planting_dates[0]]
            end_month = months[harvesting_dates[1]]
            
            if start_month <= end_month:
                in_season = start_month <= current_month <= end_month
            else:
                in_season = current_month >= start_month or current_month <= end_month
            
            if in_season:
                recommendations.append(crop)
    
    # Return the recommendations as a JSON response
    return recommendations  

#for recommendations---------------------------------------------------

# Load the trained model
model = joblib.load(f'{URL}crop_recommendation_model.pkl')

# Function to recommend crops based on temperature and humidity
def recommend_crops(temperature, humidity, top_n=3):
    # Create a DataFrame with the input features
    input_data = pd.DataFrame({'Temperature_y': [temperature], 'Humidity_y': [humidity]})
    
    # Get the prediction probabilities for each class
    probabilities = model.predict_proba(input_data)[0]
    
    # Get the class labels
    class_labels = model.classes_
    
    # Create a DataFrame with the class labels and their corresponding probabilities
    prob_df = pd.DataFrame({'Crop': class_labels, 'Probability': probabilities})
    
    # Sort the DataFrame by probability in descending order and get the top N recommendations
    top_recommendations = prob_df.sort_values(by='Probability', ascending=False).head(top_n)
    
    return top_recommendations

def get_recommended_crops(temperature, humidity, soil_type_input):
    
    # Step 1: Find crops that match the given soil type
    matched_crops = []
    for entry in soil_type_dict:
        soil_types = entry['Soil Type'].split(',')
        for soil in soil_types :
            if soil.strip().lower() == soil_type_input.strip().lower():
                matched_crops.append(entry['Crops'])
            
    
    
    # Step 2: Filter crops data based on the matched crops and current season
    current_month = datetime.now().month
    recommendations = []
    recommended_crops = recommend_crops(temperature, humidity, top_n=20)
    recommended_crop_names = recommended_crops['Crop'].tolist()
    for crop in crops_data_dict:
        if crop['Crop Name'] in matched_crops:
            # Check if the crop can be planted in the current season
            planting_dates = crop['Planting Dates'].split('-')
            harvesting_dates = crop['Harvesting Dates'].split('-')
            months = {
                "January": 1, "February": 2, "March": 3, "April": 4,
                "May": 5, "June": 6, "July": 7, "August": 8,
                "September": 9, "October": 10, "November": 11, "December": 12
            }
            start_month = months[planting_dates[0]]
            end_month = months[harvesting_dates[1]]
            
            if start_month <= end_month:
                in_season = start_month <= current_month <= end_month
            else:
                in_season = current_month >= start_month or current_month <= end_month
            
            if in_season and crop['Crop Name'] in recommended_crop_names:
                recommendations.append(crop)

    # Return the recommendations as a JSON response
    return recommendations 

