from app import get_db
zone_data = list()
def get_zones():
    try:
        db = get_db()
        # Fetch all documents from the collection
        zones_cursor = db.weather_zones.find()
        zone_data = list(zones_cursor)
        zones = [zone['Zone'] for zone in zones_cursor]  # Extract only the 'Zone' field
        # print(zones)  # For debugging
        return zones
    except Exception as e:
        print(f"An error occurred while fetching zones: {e}")
        return []


def get_current_zone(lat, lon):
    if zone_data.count <= 0 :
        get_zones()
    print(zone_data)
    return "Zone"