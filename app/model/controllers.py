import pandas as pd
import numpy as np
from sklearn.preprocessing import MinMaxScaler
from keras import models , layers, callbacks, optimizers, losses
from datetime import datetime
import math

from app import get_db
db = get_db()

Sequential, load_model = models.Sequential, models.load_model
LSTM, Dense, Dropout, Input, Reshape = layers.LSTM, layers.Dense, layers.Dropout, layers.Input, layers.Reshape
EarlyStopping, ModelCheckpoint = callbacks.EarlyStopping, callbacks.ModelCheckpoint
Adam = optimizers.Adam
MeanSquaredError = losses.MeanSquaredError

root = 'D:/Hacks/ai-driven-farm/backend/app/model'

scaler = MinMaxScaler()

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

def get_data(ZoneId = 6):
    weather_history = []
    weather_forecast = []


    # Fetch today's date
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)

    # Fetch previous weather forecasts from MongoDB
    weather_forecast_cursor = db.weather_forecast.find({
        "ZoneId": ZoneId,
        "Date": {"$lt": today}  # Only get records with Date less than today
    })
    for weather in weather_forecast_cursor:
        formatted_data = format_weather_data(weather)
        weather_forecast.append(formatted_data)


    features = ['Date', 'Min Temp', 'Max Temp', 'Humidity', 'Pressure', 'Precipitation']
    
    # Create a DataFrame for the future weather predictions
    future_weather_df = pd.DataFrame(weather_forecast, columns=features)
    future_weather_df['ZoneId'] = ZoneId
    # Reorder columns
    future_weather_df = future_weather_df[['Date', 'Min Temp', 'Max Temp', 'Humidity', 'Pressure', 'Precipitation', 'ZoneId']]

    # Initialize counters
    update_count = 0
    insert_count = 0

    # Iterate through the DataFrame and handle updates and inserts
    for index, row in future_weather_df.iterrows():
        # Create a query to find existing document by ZoneId and Date
        query = {
            'ZoneId': row['ZoneId'],
            'Date': row['Date']  # Ensure the date is considered for the update
        }
        
        # Create an update document with the new data
        update = {
            '$set': {
                'Date': row['Date'],
                'Min Temp': row['Min Temp'],
                'Max Temp': row['Max Temp'],
                'Humidity': row['Humidity'],
                'Pressure': row['Pressure'],
                'Precipitation': row['Precipitation']
            }
        }
        # Try to update the document; if not found, insert a new one
        result = db.weather_history.update_one(query, update, upsert=True)
        
        if result.matched_count > 0:
            update_count += 1  # Increment update counter
        else:
            insert_count += 1  # Increment insert counter

    # Print a summary of what was updated or inserted
    print("Data processing completed.")
    print(f"Total entries updated in history: {update_count}")
    print(f"Total entries inserted in history: {insert_count}")


    # Fetch weather_history
    weather_history_cursor = db.weather_history.find({"ZoneId" : 6})

    for weather in weather_history_cursor:
        formatted_data = format_weather_data(weather)
        weather_history.append(formatted_data)

    # Convert the lists to DataFrames
    df_history = pd.DataFrame(weather_history)
    df_forecast = pd.DataFrame(weather_forecast)

    # Return both DataFrames
    return df_history, df_forecast


def create_sequences(data, sequence_length, prediction_length):
    sequences = []
    labels = []
    for i in range(len(data) - sequence_length - prediction_length + 1):
        seq = data.iloc[i:i + sequence_length].values
        label = data.iloc[i + sequence_length: i + sequence_length + prediction_length].values
        sequences.append(seq)
        labels.append(label)
    return np.array(sequences), np.array(labels)

def dynamic_learning_rate(n):
    return max(0.00001, 0.001 * math.sqrt(100 / n))  # Scale inversely with sqrt(n)

def dynamic_batch_size(n):
    return min(64, max(2, n // 20))  # Scale batch size with n, clamped between 2 and 64

def fine_tune(data):
    n = len(data)
    
    # Convert Date columns into a single datetime column
    data['date'] = pd.to_datetime(data['Date'])
    data.set_index('date', inplace=True)
    data.drop(columns=['Date'], inplace=True)

    # Select features for prediction
    features = ['Min Temp', 'Max Temp', 'Humidity', 'Pressure', 'Precipitation']
    data = data[features]

    # Scale the data between 0 and 1
    scaled_data = scaler.fit_transform(data)
    scaled_df = pd.DataFrame(scaled_data, columns=features, index=data.index)

    # Split the data into training and testing sets (80% training, 20% testing)
    train_size = int(len(scaled_df) * 0.8)
    train_data = scaled_df[:train_size]
    test_data = scaled_df[train_size:]

    # Define sequence and prediction lengths
    sequence_length = n // 10  # Input sequence 
    prediction_length = 1  # Predict the next 

    # Create sequences for training and testing
    X_train, y_train = create_sequences(train_data, sequence_length, prediction_length)
    X_test, y_test = create_sequences(test_data, sequence_length, prediction_length)

    # Ensure the data type is float32
    X_train = X_train.astype(np.float32)
    y_train = y_train.astype(np.float32)
    X_test = X_test.astype(np.float32)
    y_test = y_test.astype(np.float32)

    # Check the shape of the generated sequences and labels
    print("X_train shape:", X_train.shape)  # Should be (samples, sequence_length, num_features)
    print("y_train shape:", y_train.shape)  # Should be (samples, prediction_length, num_features)


    # Calculate learning rate and batch size dynamically
    learning_rate = dynamic_learning_rate(n)
    batch_size = dynamic_batch_size(n)

    print("Dynamic Learning Rate:", learning_rate)
    print("Dynamic Batch Size:", batch_size)

    # Load the trained model
    model = load_model(root + '/best_model.keras')


    # Compile the model with a lower learning rate (e.g., 0.0005)
    model.compile(optimizer=Adam(learning_rate=learning_rate), loss=MeanSquaredError())

    # Set up callbacks for early stopping and model checkpointing
    early_stopping = EarlyStopping(monitor='val_loss', patience=10, restore_best_weights=True)
    model_checkpoint = ModelCheckpoint(root + '/best_model1.keras', save_best_only=True)

    # Train the model and save the history
    model.fit(X_train, y_train, epochs=100, batch_size=batch_size, validation_data=(X_test, y_test), callbacks=[early_stopping, model_checkpoint])

def forecast_n_save(data, ZoneId = 6):

    # Convert Date columns into a single datetime column
    data['date'] = pd.to_datetime(data['Date'])
    data.set_index('date', inplace=True)
    data.drop(columns=['Date'], inplace=True)

    # Select features for prediction
    features = ['Min Temp', 'Max Temp', 'Humidity', 'Pressure', 'Precipitation']
    data = data[features]

    # Scale the data using used scaler
    scaled_data = scaler.transform(data)  # Fit the scaler on the entire dataset
    scaled_df = pd.DataFrame(scaled_data, columns=features, index=data.index)

    # Define sequence length
    sequence_length = 366  # Input sequence 

    # Use the entire scaled data for prediction
    last_sequence = scaled_df.values[-sequence_length:].reshape(1, sequence_length, len(features))  # Ensure correct shape

    # Load the trained model
    model = load_model(root + '/best_model1.keras')

    # Predict future weather for the next 366 days
    future_prediction = model.predict(last_sequence)

    # Reshape the predicted data to 2D for inverse transformation
    future_prediction_reshaped = future_prediction.reshape(future_prediction.shape[1], future_prediction.shape[2])

    # Inverse transform the prediction back to the original scale
    future_weather = scaler.inverse_transform(future_prediction_reshaped)

    # Round the predicted values to 6 decimal points
    future_weather_rounded = np.round(future_weather, 6)

    # Prepare data for MongoDB
    # Get the last date from the input data
    last_date = data.index[-1]
    future_dates = pd.date_range(start=last_date + pd.Timedelta(days=1), periods=len(future_weather_rounded))
    
    # Create a DataFrame for the future weather predictions
    future_weather_df = pd.DataFrame(future_weather_rounded, columns=features)
    future_weather_df['Date'] = future_dates
    future_weather_df['ZoneId'] = ZoneId  # Set ZoneId to 6 for all entries

    # Reorder columns
    future_weather_df = future_weather_df[['Date', 'Min Temp', 'Max Temp', 'Humidity', 'Pressure', 'Precipitation', 'ZoneId']]

    # Initialize counters
    update_count = 0
    insert_count = 0

    # Iterate through the DataFrame and handle updates and inserts
    for index, row in future_weather_df.iterrows():
        # Create a query to find existing document by ZoneId and Date
        query = {
            'ZoneId': row['ZoneId'],
            'Date': row['Date']  # Ensure the date is considered for the update
        }
        
        # Create an update document with the new data
        update = {
            '$set': {
                'Date': row['Date'],
                'Min Temp': row['Min Temp'],
                'Max Temp': row['Max Temp'],
                'Humidity': row['Humidity'],
                'Pressure': row['Pressure'],
                'Precipitation': row['Precipitation']
            }
        }
        
        # Try to update the document; if not found, insert a new one
        result = db.weather_forecast.update_one(query, update, upsert=True)
        
        if result.matched_count > 0:
            update_count += 1  # Increment update counter
        else:
            insert_count += 1  # Increment insert counter

    # Print a summary of what was updated or inserted
    print("Data processing completed.")
    print(f"Total entries updated in future: {update_count}")
    print(f"Total entries inserted in future: {insert_count}")
    
    return "Success"
