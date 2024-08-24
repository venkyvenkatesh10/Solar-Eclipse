import pandas as pd
import folium
import json
import os
import random
from faker import Faker
import hashlib

fake = Faker()

# Define the cities and their approximate latitude and longitude
city_lat_long = {
    "Austin": (30.2672, -97.7431),
    "Dallas": (32.7767, -96.7970),
    "Waco": (31.5493, -97.1467),
    "Little Rock": (34.7465, -92.2896),
    "Hot Springs": (34.5037, -93.0552),
    "Cape Girardeau": (37.3059, -89.5181),
    "Carbondale": (37.7273, -89.2168),
    "Evansville": (37.9716, -87.5711),
    "Indianapolis": (39.7684, -86.1581),
    "Dayton": (39.7589, -84.1916),
    "Toledo": (41.6528, -83.5379),
    "Cleveland": (41.4993, -81.6944),
    "Buffalo": (42.8864, -78.8784),
    "Rochester": (43.1566, -77.6088)
}

# Expanded device specifications (make and model)
device_data = {
    "Apple": ["iPhone 13", "iPhone 13 Pro", "iPhone 12", "iPhone 12 Pro", "iPhone 11", "iPhone SE", "iPad Pro", "iPad Air"],
    "Samsung": ["Galaxy S21", "Galaxy S21 Ultra", "Galaxy S20", "Galaxy Note 20", "Galaxy A52", "Galaxy Tab S7", "Galaxy Z Fold3", "Galaxy Z Flip3"],
    "Google": ["Pixel 6", "Pixel 6 Pro", "Pixel 5", "Pixel 4a", "Pixel 4", "Pixel Slate", "Pixelbook Go"],
    "OnePlus": ["OnePlus 9", "OnePlus 9 Pro", "OnePlus 8T", "OnePlus Nord", "OnePlus 7T", "OnePlus 7 Pro", "OnePlus Watch"],
    "Xiaomi": ["Mi 11", "Mi 11 Ultra", "Redmi Note 10", "Poco X3", "Mi 10T", "Mi Mix Fold", "Mi Pad 5"],
    "Huawei": ["P40 Pro", "P40 Lite", "Mate 40 Pro", "Nova 7i", "Y9s", "MatePad Pro", "Mate X2"],
    "Sony": ["Xperia 1 III", "Xperia 5 III", "Xperia 10 III", "Xperia Pro", "Xperia L4", "Xperia Tablet Z", "Xperia Z5"],
    "LG": ["Wing 5G", "V60 ThinQ", "G8X ThinQ", "Velvet", "K92 5G", "G7 ThinQ", "Stylo 6"],
    "Motorola": ["Moto G100", "Moto G Power", "Edge 20 Pro", "Razr 5G", "Moto G Stylus", "One 5G Ace", "Moto E7"],
    "Nokia": ["Nokia 8.3 5G", "Nokia 5.4", "Nokia 7.2", "Nokia 6.2", "Nokia G50", "Nokia 2720 Flip", "Nokia C3"]
}

# Points of Interest for each city
poi_data = {
    "Austin": ["Texas State Capitol", "Zilker Park", "Barton Springs Pool", "Mount Bonnell", "Lady Bird Lake"],
    "Dallas": ["The Sixth Floor Museum", "Dallas Arboretum", "Reunion Tower", "Dallas Zoo", "Klyde Warren Park"],
    "Waco": ["Waco Mammoth National Monument", "Dr Pepper Museum", "Cameron Park Zoo", "Texas Ranger Hall of Fame", "Magnolia Market"],
    "Little Rock": ["Little Rock Central High School", "William J. Clinton Library", "Pinnacle Mountain State Park", "River Market District", "Big Dam Bridge"],
    "Hot Springs": ["Hot Springs National Park", "Garvan Woodland Gardens", "Bathhouse Row", "Magic Springs Theme Park", "Lake Catherine State Park"],
    "Cape Girardeau": ["Mississippi River", "Cape Rock Park", "Trail of Tears State Park", "Lazy L Safari Park", "Cape Girardeau Conservation Nature Center"],
    "Carbondale": ["Giant City State Park", "Southern Illinois University", "Crab Orchard National Wildlife Refuge", "Cedar Lake", "Boo Rochman Memorial Park"],
    "Evansville": ["Mesker Park Zoo", "Evansville Museum", "Angel Mounds", "Children's Museum of Evansville", "Wesselman Woods Nature Preserve"],
    "Indianapolis": ["Indianapolis Motor Speedway", "Children's Museum of Indianapolis", "Indianapolis Zoo", "White River State Park", "Monument Circle"],
    "Dayton": ["National Museum of the USAF", "Carillon Historical Park", "Dayton Aviation Heritage Park", "Boonshoft Museum", "Wegerzyn Gardens"],
    "Toledo": ["Toledo Zoo", "Toledo Museum of Art", "Oak Openings Preserve", "Imagination Station", "Wildwood Preserve Metropark"],
    "Cleveland": ["Rock & Roll Hall of Fame", "Cleveland Museum of Art", "Cleveland Metroparks Zoo", "West Side Market", "Cleveland Botanical Garden"],
    "Buffalo": ["Niagara Falls", "Buffalo Zoo", "Albright-Knox Art Gallery", "Frank Lloyd Wright's Martin House", "Canalside"],
    "Rochester": ["The Strong National Museum", "Highland Park", "Seneca Park Zoo", "George Eastman Museum", "Seabreeze Amusement Park"]
}

# Function to generate random latitude and longitude within a city's approximate range
def generate_lat_long(city):
    lat, long = city_lat_long.get(city, (0, 0))
    return lat + random.uniform(-0.05, 0.05), long + random.uniform(-0.05, 0.05)

# Function to generate random app usage including social media, video streaming, and food delivery apps
def generate_app_usage(city, state, zipcode):
    apps = [
        {"app": "Instagram", "category": "Social Media"},
        {"app": "Facebook", "category": "Social Media"},
        {"app": "Twitter", "category": "Social Media"},
        {"app": "YouTube", "category": "Video Streaming"},
        {"app": "Netflix", "category": "Video Streaming"},
        {"app": "Google Maps", "category": "Navigation"},
        {"app": "Spotify", "category": "Music Streaming"},
        {"app": "WhatsApp", "category": "Messaging"},
        {"app": "Gmail", "category": "Email"},
        {"app": "Zoom", "category": "Video Conferencing"},
        {"app": "Snapchat", "category": "Social Media"},
        {"app": "Uber Eats", "category": "Food Delivery", "url": f"https://www.ubereats.com/{state.lower()}/{city.lower()}-{zipcode}"},
        {"app": "DoorDash", "category": "Food Delivery", "url": f"https://www.doordash.com/{state.lower()}/{city.lower()}/d/{zipcode}"},
        {"app": "Grubhub", "category": "Food Delivery", "url": f"https://www.grubhub.com/{state.lower()}/{city.lower()}/{zipcode}"},
        {"app": "Postmates", "category": "Food Delivery", "url": f"https://postmates.com/delivery/{state.lower()}/{city.lower()}-{zipcode}"},
        {"app": "Seamless", "category": "Food Delivery", "url": f"https://www.seamless.com/{state.lower()}/{city.lower()}/{zipcode}"}
    ]
    return random.choice(apps)

# Function to generate a random MDN hash
def generate_mdn_hash():
    mdn = fake.phone_number()
    mdn_hash = hashlib.sha256(mdn.encode()).hexdigest()
    return mdn_hash

# Load the JSON data (to extract only subscriber_id and eclipse_time)
input_file = r"C:\Users\venka\Desktop\Solar Eclipse\eclipse_subscriber_data_with_times.json"
with open(input_file, 'r') as file:
    data = [json.loads(line) for line in file]

# Create a list to store processed data
processed_data = []

# Path to save the individual maps
map_folder = r"C:\Users\venka\Desktop\Solar Eclipse\maps"
os.makedirs(map_folder, exist_ok=True)

# Process each entry in the data
for entry in data:
    subscriber_id = entry['subscriber_id']
    eclipse_time = entry['eclipse_time']
    
    # Select a random destination city
    destination_city = random.choice(list(city_lat_long.keys()))
    
    # Generate latitude and longitude for the selected city
    latitude, longitude = generate_lat_long(destination_city)
    
    origin_city = fake.city()
    eclipse_upstream_data = random.randint(50, 300)  # MB
    eclipse_downstream_data = random.randint(200, 1500)  # MB
    app_usage = generate_app_usage(destination_city, "TX", "75201")
    time_zone = "CST" if destination_city in ["Austin", "Dallas", "Waco", "Little Rock", "Hot Springs", "Cape Girardeau", "Carbondale", "Evansville"] else "EST"
    
    # Generate random device make and model
    make = random.choice(list(device_data.keys()))
    model = random.choice(device_data[make])
    
    # Generate MDN hash
    mdn_hash = generate_mdn_hash()
    
    # Select all Points of Interest for the destination city
    poi = poi_data[destination_city]
    poi_str = ', '.join(poi)

    # Create a map centered on the subscriber's location
    m = folium.Map(location=[latitude, longitude], zoom_start=12)
    
    # Add the subscriber location marker
    folium.Marker(
        location=[latitude, longitude],
        popup=f"Subscriber ID: {subscriber_id}",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    
    # Add POI markers on the map
    for p in poi:
        poi_lat, poi_long = generate_lat_long(destination_city)
        folium.Marker(
            location=[poi_lat, poi_long],
            popup=f"POI: {p}",
            icon=folium.Icon(color='green', icon='cloud')
        ).add_to(m)
    
    # Save the map as an HTML file
    map_filename = f"map_{subscriber_id}.html"
    map_filepath = os.path.join(map_folder, map_filename)
    m.save(map_filepath)
    
    # Add a hyperlink to the map in the CSV data
    location_link = f'=HYPERLINK("{map_filepath}", "See Location")'
    
    # Add the entry to the processed data list
    processed_data.append({
        "subscriber_id": subscriber_id,
        "origin_city": origin_city,
        "destination_city": destination_city,
        "eclipse_time": eclipse_time,
        "time_zone": time_zone,
        "latitude": latitude,
        "longitude": longitude,
        "eclipse_upstream_data": eclipse_upstream_data,
        "eclipse_downstream_data": eclipse_downstream_data,
        "app_used": app_usage['app'],
        "app_category": app_usage['category'],
        "app_url": app_usage.get('url', 'N/A'),  # Some apps won't have URLs
        "make": make,
        "model": model,
        "mdn_hash": mdn_hash,
        "points_of_interest": poi_str,
        "see_location": location_link
    })

# Convert processed data to a DataFrame
df = pd.DataFrame(processed_data)

# Specify the path where the CSV file will be saved
output_csv_file = r"C:\Users\venka\Desktop\Solar Eclipse\eclipse_subscriber_data_with_links.csv"

# Save the DataFrame to a CSV file
df.to_csv(output_csv_file, index=False)

print(f"CSV file saved to {output_csv_file}")
