from app import get_db
db = get_db()



def get_zones():
    try:
        # Fetch all documents from the collection
        zones_cursor = db.weather_zones.find({}, {'Zone': 1 , 'ZoneId' : 1})
        # Create a list of dictionaries containing both 'Zone' and 'ZoneId'
        zones = [{'ZoneId': zone['ZoneId'], 'Name': zone['Zone']} for zone in zones_cursor]
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

def get_soils():
    try:
        # Fetch all documents from the collection
        soils_cursor = db.crops.find({}, {'Soil Type': 1})
        soil_list = set()

        # Extract and flatten the soil types
        soils = [soil['Soil Type'] for soil in soils_cursor]  # Extract only the 'Soil Type' field
        
        for s in soils:
            soil_list.update(s.split(', '))

        return list(soil_list)  # Convert set back to list for return
    except Exception as e:
        print(f"An error occurred while fetching soils: {e}")
        return []

def get_crops(zoneId):
    
    # Find all crops based on ZoneId
    result = db.crops_predicted.find({"ZoneId": int(zoneId)})
    crops = []
    
    for crop in result:
        
        # Get soil type using the crop name
        soil_info = db.crops.find_one({"Crop Name": crop['Crop Name']})
        
        # Create a dictionary with all fields except '_id'
        crop_data = {key: value for key, value in crop.items() if key != '_id'}
        
        # Add soil type information if available
        if soil_info and "Soil Type" in soil_info:
            soil = soil_info["Soil Type"]
            # If soil type is a string, wrap it in a list as a single soil type
            if isinstance(soil, str):
                crop_data['Soil Type'] = [soil]
            elif isinstance(soil, list):
                # If the list contains only one element and it's a comma-separated string, split it
                if len(soil) == 1 and isinstance(soil[0], str):
                    crop_data['Soil Type'] = [s.strip() for s in soil[0].split(',')]
                else:
                    crop_data['Soil Type'] = soil  # Keep the list as is if it's already correct
        
        
        # Append the crop data with soil type
        crops.append(crop_data)

    return crops

