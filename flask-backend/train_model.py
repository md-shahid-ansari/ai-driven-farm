import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from imblearn.over_sampling import SMOTE
import joblib

# Load the datasets
crops_data = pd.read_csv('crops_data.csv')
weather_data = pd.read_csv('weather_data_cleen.csv')

# Convert the 'Timestamp' column in weather_data to datetime
weather_data['Timestamp'] = pd.to_datetime(weather_data['Timestamp'])

# Convert numerical columns in crops_data to appropriate data types
crops_data['Water Requirements'] = crops_data['Water Requirements'].str.extract('(\d+)-(\d+)').astype(float).mean(axis=1)
crops_data['Temperature'] = crops_data['Temperature'].str.extract('(\d+)-(\d+)').astype(float).mean(axis=1)
crops_data['Humidity'] = crops_data['Humidity'].str.extract('(\d+)-(\d+)').astype(float).mean(axis=1)
crops_data['Sunshine Hours'] = crops_data['Sunshine Hours'].str.extract('(\d+)-(\d+)').astype(float).mean(axis=1)
crops_data['Wind Speed'] = crops_data['Wind Speed'].str.extract('(\d+)-(\d+)').astype(float).mean(axis=1)
crops_data['Soil pH Level'] = crops_data['Soil pH Level'].str.extract('(\d+\.\d+)-(\d+\.\d+)').astype(float).mean(axis=1)

# Extract the month from the 'Planting Dates' column in crops_data
def extract_month(date_str):
    match = re.search(r'\b(January|February|March|April|May|June|July|August|September|October|November|December)\b', date_str, re.IGNORECASE)
    if match:
        return match.group(0)
    return None

crops_data['Month'] = crops_data['Planting Dates'].apply(extract_month)
month_to_period = {
    'January': '2020-01', 'February': '2020-02', 'March': '2020-03', 'April': '2020-04',
    'May': '2020-05', 'June': '2020-06', 'July': '2020-07', 'August': '2020-08',
    'September': '2020-09', 'October': '2020-10', 'November': '2020-11', 'December': '2020-12'
}
crops_data['Month'] = crops_data['Month'].map(month_to_period)

# Aggregate weather data to monthly averages
weather_data['Month'] = weather_data['Timestamp'].dt.to_period('M').astype(str)
monthly_weather_data = weather_data.groupby('Month').mean().reset_index()

# Align the datasets based on the 'Month' column
aligned_data = pd.merge(crops_data, monthly_weather_data, on='Month', how='inner')

# Create the feature set and target variable using only temperature and humidity
X = aligned_data[['Temperature_y', 'Humidity_y']]
y = aligned_data['Crop Name']

# Apply SMOTE to balance the classes
smote = SMOTE(random_state=42)
X_resampled, y_resampled = smote.fit_resample(X, y)

# Split the resampled data into training and testing sets
X_train_resampled, X_test_resampled, y_train_resampled, y_test_resampled = train_test_split(X_resampled, y_resampled, test_size=0.2, random_state=42)

# Train a Random Forest classifier on the resampled data
rf_clf_resampled = RandomForestClassifier(random_state=42)
rf_clf_resampled.fit(X_train_resampled, y_train_resampled)

# Make predictions on the test set
y_pred_resampled = rf_clf_resampled.predict(X_test_resampled)

# Evaluate the model
report_resampled = classification_report(y_test_resampled, y_pred_resampled)
print(report_resampled)

# Save the trained model to a file
joblib.dump(rf_clf_resampled, 'crop_recommendation_model.pkl')