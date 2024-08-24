import pandas as pd
import numpy as np
from random import randint, choice
from faker import Faker
import datetime
import os

fake = Faker()

# Define the eclipse cities, their airports, the time of totality, and time zones
eclipse_cities = {
    "Austin": {"airport": "AUS", "eclipse_time": "2024-04-08T13:36:00", "time_zone": "CST"},
    "Dallas": {"airport": "DFW", "eclipse_time": "2024-04-08T13:42:00", "time_zone": "CST"},
    "Waco": {"airport": "ACT", "eclipse_time": "2024-04-08T13:38:00", "time_zone": "CST"},
    "Little Rock": {"airport": "LIT", "eclipse_time": "2024-04-08T13:52:00", "time_zone": "CST"},
    "Hot Springs": {"airport": "HOT", "eclipse_time": "2024-04-08T13:50:00", "time_zone": "CST"},
    "Cape Girardeau": {"airport": "CGI", "eclipse_time": "2024-04-08T14:00:00", "time_zone": "CST"},
    "Carbondale": {"airport": "MWA", "eclipse_time": "2024-04-08T14:02:00", "time_zone": "CST"},
    "Evansville": {"airport": "EVV", "eclipse_time": "2024-04-08T14:04:00", "time_zone": "CST"},
    "Indianapolis": {"airport": "IND", "eclipse_time": "2024-04-08T15:06:00", "time_zone": "EST"},
    "Dayton": {"airport": "DAY", "eclipse_time": "2024-04-08T15:10:00", "time_zone": "EST"},
    "Toledo": {"airport": "TOL", "eclipse_time": "2024-04-08T15:12:00", "time_zone": "EST"},
    "Cleveland": {"airport": "CLE", "eclipse_time": "2024-04-08T15:15:00", "time_zone": "EST"},
    "Buffalo": {"airport": "BUF", "eclipse_time": "2024-04-08T15:18:00", "time_zone": "EST"},
    "Rochester": {"airport": "ROC", "eclipse_time": "2024-04-08T15:20:00", "time_zone": "EST"}
}

# Define additional cities outside the eclipse path and their airports
other_cities = {
    "Houston": "IAH",
    "San Antonio": "SAT",
    "Memphis": "MEM",
    "Chicago": "ORD",
    "Detroit": "DTW",
    "Atlanta": "ATL",
    "Miami": "MIA",
    "New York": "JFK",
    "Los Angeles": "LAX",
    "Phoenix": "PHX",
    "Denver": "DEN",
    "Seattle": "SEA",
    "Boston": "BOS",
    "Philadelphia": "PHL",
    "Washington D.C.": "DCA"
}

# Example hotel and motel names
hotel_names = [
    "Hilton Garden Inn",
    "Marriott",
    "Hyatt Regency",
    "Holiday Inn Express",
    "Courtyard by Marriott",
    "Best Western",
    "Comfort Inn",
    "Hampton Inn",
    "Days Inn",
    "Super 8",
    "Motel 6",
    "La Quinta Inn",
    "Econo Lodge",
    "Quality Inn",
    "Red Roof Inn"
]

# Generate random subscriber data
num_subscribers = 1000
data = []

for _ in range(num_subscribers):
    subscriber_id = fake.uuid4()
    origin_city = choice(list(other_cities.keys()))  # Select origin city from outside the eclipse path
    origin_airport = other_cities[origin_city]
    destination_city = choice(list(eclipse_cities.keys()))  # Select destination city from eclipse cities
    destination_airport = eclipse_cities[destination_city]["airport"]
    eclipse_time = eclipse_cities[destination_city]["eclipse_time"]
    time_zone = eclipse_cities[destination_city]["time_zone"]
    travel_mode = choice(["Flight", "Road"])
    start_time = fake.date_time_between(start_date="-2d", end_date="-1d")  # A day before the eclipse
    arrival_time = start_time + datetime.timedelta(hours=randint(1, 10))
    
    # Simulate hotel check-in if applicable
    if travel_mode == "Flight":
        hotel_check_in = choice(hotel_names)
    else:
        hotel_check_in = None

    data.append({
        "subscriber_id": subscriber_id,
        "origin_city": origin_city,
        "origin_airport": origin_airport,
        "destination_city": destination_city,
        "destination_airport": destination_airport,
        "travel_mode": travel_mode,
        "start_time": start_time.isoformat(),
        "arrival_time": arrival_time.isoformat(),
        "eclipse_time": eclipse_time,
        "time_zone": time_zone,
        "hotel_check_in": hotel_check_in,
        "data_usage_upstream": randint(100, 1000),  # in MB
        "data_usage_downstream": randint(500, 5000),  # in MB
    })

df = pd.DataFrame(data)

# Specify the path where the file will be saved
output_path = r"C:\Users\venka\Desktop\Solar Eclipse"

# Ensure the directory exists
os.makedirs(output_path, exist_ok=True)

# Save the DataFrame as a JSON file
output_file = os.path.join(output_path, "eclipse_subscriber_data_with_times.json")
df.to_json(output_file, orient="records", lines=True)

print(f"Data saved to {output_file}")
