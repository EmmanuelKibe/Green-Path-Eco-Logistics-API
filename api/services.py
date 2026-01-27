from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def calculate_distance(origin_name, dest_name):
    """
    Takes two city names and returns distance in kilometers.
    """
    geolocator = Nominatim(user_agent="green_path_logistics")
    
    # Get coordinates for origin
    loc1 = geolocator.geocode(origin_name)
    # Get coordinates for destination
    loc2 = geolocator.geocode(dest_name)
    
    if loc1 and loc2:
        # Returns distance in km
        return geodesic((loc1.latitude, loc1.longitude), (loc2.latitude, loc2.longitude)).km
    return None