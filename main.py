import requests
import json

# Your API key (keep it secret!)
api_key = 'AIzaSyCofEHIsoFbtmxqUvDMQgbHTRIfJ1yrARI'

# The address you wish to geocode
address = "Ukraine"

# Encode the address for URL
address = requests.utils.quote(address)

# Create the URL for the request
url = f"https://maps.googleapis.com/maps/api/geocode/json?address={address}&key={api_key}"

# Make the GET request to the Google Maps Geocoding API
response = requests.get(url)

# Check if the request was successful
if response.status_code == 200:
    # Parse the JSON response
    geocode_data = response.json()

    # Pretty-print the JSON data
    print(json.dumps(geocode_data, indent=4))
else:
    print(f"Error: {response.status_code}")

# Extracting the latitude and longitude from the response
if geocode_data["status"] == "OK":
    latitude = geocode_data["results"][0]["geometry"]["location"]["lat"]
    longitude = geocode_data["results"][0]["geometry"]["location"]["lng"]
    print(f"Latitude: {latitude}, Longitude: {longitude}")
else:
    print("Geocoding failed with status: " + geocode_data["status"])