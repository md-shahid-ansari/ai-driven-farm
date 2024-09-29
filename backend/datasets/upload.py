from app import get_db

# Step 1: Define the weather zones data directly
zones_data = [
    {
        "Zone": "Western Himalayas",
        "Districts": 44,
        "States": "Jammu & Kashmir, Himachal Pradesh, Uttarakhand",
        "Climate": "Cold, temperate, alpine",
        "Temperature Range": [5, 15],
        "Precipitation Range": [1000, 2000],
        "Latitude Range": "30.0°N - 37.0°N",
        "Longitude Range": "74.0°E - 82.0°E"
    },
    {
        "Zone": "Eastern Himalayas",
        "Districts": 33,
        "States": "Arunachal Pradesh, Sikkim, Darjeeling",
        "Climate": "Temperate, subtropical",
        "Temperature Range": [10, 20],
        "Precipitation Range": [1500, 3000],
        "Latitude Range": "26.0°N - 30.0°N",
        "Longitude Range": "88.0°E - 96.0°E"
    },
    {
        "Zone": "Indo-Gangetic Plains",
        "Districts": 156,
        "States": "Punjab, Haryana, Uttar Pradesh, Bihar",
        "Climate": "Semi-arid, humid subtropical",
        "Temperature Range": [20, 30],
        "Precipitation Range": [500, 1000],
        "Latitude Range": "24.0°N - 30.0°N",
        "Longitude Range": "74.0°E - 88.0°E"
    },
    {
        "Zone": "Thar Desert",
        "Districts": 23,
        "States": "Rajasthan, Gujarat",
        "Climate": "Arid, hot desert",
        "Temperature Range": [25, 35],
        "Precipitation Range": [0, 500],  # Assuming '<500' means up to 500
        "Latitude Range": "23.0°N - 29.0°N",
        "Longitude Range": "69.0°E - 76.0°E"
    },
    {
        "Zone": "Deccan Plateau",
        "Districts": 101,
        "States": "Maharashtra, Karnataka, Telangana",
        "Climate": "Semi-arid, tropical",
        "Temperature Range": [20, 30],
        "Precipitation Range": [500, 1000],
        "Latitude Range": "15.0°N - 22.0°N",
        "Longitude Range": "74.0°E - 82.0°E"
    },
    {
        "Zone": "Eastern Coastal Plains",
        "Districts": 74,
        "States": "West Bengal, Odisha, Andhra Pradesh",
        "Climate": "Humid subtropical, tropical",
        "Temperature Range": [20, 30],
        "Precipitation Range": [1000, 2000],
        "Latitude Range": "10.0°N - 20.0°N",
        "Longitude Range": "80.0°E - 90.0°E"
    },
    {
        "Zone": "Western Coastal Plains",
        "Districts": 51,
        "States": "Kerala, Tamil Nadu",
        "Climate": "Tropical, humid",
        "Temperature Range": [22, 32],
        "Precipitation Range": [2000, 3000],
        "Latitude Range": "8.0°N - 15.0°N",
        "Longitude Range": "72.0°E - 78.0°E"
    },
    {
        "Zone": "Northeastern Hills",
        "Districts": 35,
        "States": "Meghalaya, Manipur, Mizoram, Nagaland",
        "Climate": "Subtropical, temperate",
        "Temperature Range": [15, 25],
        "Precipitation Range": [1500, 3000],
        "Latitude Range": "22.0°N - 28.0°N",
        "Longitude Range": "90.0°E - 98.0°E"
    },
    {
        "Zone": "Islands",
        "Districts": 9,
        "States": "Andaman & Nicobar, Lakshadweep",
        "Climate": "Tropical, humid",
        "Temperature Range": [22, 32],
        "Precipitation Range": [2000, 3000],
        "Latitude Range": "6.0°N - 14.0°N",
        "Longitude Range": "92.0°E - 94.0°E"
    },
    {
        "Zone": "Central India",
        "Districts": 54,
        "States": "Madhya Pradesh, Chhattisgarh",
        "Climate": "Semi-arid, tropical",
        "Temperature Range": [20, 30],
        "Precipitation Range": [500, 1000],
        "Latitude Range": "20.0°N - 25.0°N",
        "Longitude Range": "75.0°E - 85.0°E"
    },
    {
        "Zone": "Southwestern India",
        "Districts": 22,
        "States": "Goa, Konkan region",
        "Climate": "Tropical, humid",
        "Temperature Range": [22, 32],
        "Precipitation Range": [2000, 3000],
        "Latitude Range": "14.0°N - 18.0°N",
        "Longitude Range": "72.0°E - 78.0°E"
    },
    {
        "Zone": "Northwestern India",
        "Districts": 30,
        "States": "Delhi, NCR, parts of Haryana",
        "Climate": "Semi-arid, humid subtropical",
        "Temperature Range": [20, 30],
        "Precipitation Range": [500, 1000],
        "Latitude Range": "25.0°N - 30.0°N",
        "Longitude Range": "70.0°E - 78.0°E"
    },
    {
        "Zone": "Ladakh and Jammu",
        "Districts": 14,
        "States": "Ladakh, Jammu & Kashmir",
        "Climate": "Cold, temperate",
        "Temperature Range": [5, 15],
        "Precipitation Range": [500, 1000],
        "Latitude Range": "32.0°N - 37.0°N",
        "Longitude Range": "74.0°E - 80.0°E"
    },
    {
        "Zone": "Tripura and Mizoram",
        "Districts": 10,
        "States": "Tripura, Mizoram",
        "Climate": "Subtropical, temperate",
        "Temperature Range": [15, 25],
        "Precipitation Range": [1500, 3000],
        "Latitude Range": "23.0°N - 26.0°N",
        "Longitude Range": "91.0°E - 93.5°E"
    },
    {
        "Zone": "Puducherry and Andaman",
        "Districts": 5,
        "States": "Puducherry, Andaman & Nicobar",
        "Climate": "Tropical, humid",
        "Temperature Range": [22, 32],
        "Precipitation Range": [2000, 3000],
        "Latitude Range": "10.0°N - 14.0°N",
        "Longitude Range": "92.0°E - 94.0°E"
    },
]

def upload():
    db = get_db()
    
    # Step 4: Insert the processed data into the 'weather_zones' collection
    result = db.weather_zones.insert_many(zones_data)
    
    print(f"Inserted {len(result.inserted_ids)} zone records into the weather_zones collection.")
