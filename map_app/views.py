from django.shortcuts import render
import requests
import json

# Create your views here.
def index(request):
    url = "https://api.unhcr.org/population/v1/asylum-applications/"
    year= 2019
    coo = "UKR"
    coa_countries = ["AUT","ESP","FRA","ITA"]
    
    
    
    all_data = []
    
    for coa in coa_countries:
        params = {
            "page": 1,
            "coo": coo,
            "year": year,
            "coa": coa,
            "cf_type": "iso",
        }
        response = requests.get(url, params=params)
        data = response.json()
        all_data.append(data)
    context = {
        "all_data": all_data,
      
        "coa_countries": coa_countries,
        "coo": coo,
    }
    

# The address you wish to geocode
    address = "Ukraine"

    # Encode the address for URL
    address = requests.utils.quote(address)

    print(all_data)
    items_list = [item for entry in all_data for item in entry['items']]
    print(items_list)
    coordinates_list = []
    # Create the URL for the request
    for dat in items_list:
        print(f"coa_name: {dat['coa_name']}")
        geocode_url = f"https://maps.googleapis.com/maps/api/geocode/json?address={dat['coa_name']}&key={api_key}"
        
        geocode_response = requests.get(geocode_url)

    # Check if the request was successful
        if geocode_response.status_code == 200:
            geocode_data = geocode_response.json()

            if geocode_data["status"] == "OK":
                latitude = geocode_data["results"][0]["geometry"]["location"]["lat"]
                longitude = geocode_data["results"][0]["geometry"]["location"]["lng"]
                
                coa_name = dat['coa_name']
                coordinates_list.append({
                    'coords': {'lat': latitude, 'lng': longitude},
                    'content': coa_name
                })
                print(f"Coordinates for {coa_name}: {latitude}, {longitude}")
            else:
                print(f"Geocoding failed for {coa_name}")
        else:
            print(f"Error with geocode request: {geocode_response.status_code}")
            
        
        print(coordinates_list)
        
        context = {
            "all_data": all_data,
            "coordinates_list": coordinates_list,
            "coa_countries": coa_countries,
            "coo": coo,
        }

        
        
    # coordinates_list = []

    # # Make the GET request to the Google Maps Geocoding API
    # response = requests.get(url)

    # Check if the request was successful
    # if response.status_code == 200:
    #     # Parse the JSON response
    #     geocode_data = response.json()

    #     # Pretty-print the JSON data
    #     print(json.dumps(geocode_data, indent=4))
    # else:
    #     print(f"Error: {response.status_code}")
        
    #     # map_data = [{a:1, b:2},{l}]

    # # Extracting the latitude and longitude from the response
    # if geocode_data["status"] == "OK":
    #     latitude = geocode_data["results"][0]["geometry"]["location"]["lat"]
    #     longitude = geocode_data["results"][0]["geometry"]["location"]["lng"]
    #     coordinates_list.append({
    #             'coords': {'lat': latitude, 'lng': longitude},
    #             'content': dat['coa_name']
    #         })
    #     print(coordinates_list)
        
    #     print(f"Latitude: {latitude}, Longitude: {longitude}")
    #     context = {
    #         "all_data": all_data,
    #         "latitude": latitude,
    #         "longitude": longitude,
    #         "coa_countries": coa_countries,
    #         "coo": coo,
    #     }
    # else:
    #     print("Geocoding failed with status: " + geocode_data["status"])
    
    context['coordinates_list_json'] = json.dumps(coordinates_list)
            
    return render(request, 'map/index.html', context)


#  for year in year_range:
#             page = 1
#             while True:
#                 # Define the parameters for the API request, including the page
#                 params = {
#                     "limit": 100,  # Adjust the limit per page as needed
#                     "yearFrom": year,
#                     "yearTo": year,
#                     "coo": coo,
#                     "coa": coa,
#                     "cf_type": "iso",
#                     "page": page
#                  }


#                 # Make a GET request to the API
#                 response = requests.get(url, params=params)

#                 # Check if the request was successful (status code 200)
#                 if response.status_code == 200:
#                     # Parse the JSON response
#                     data = response.json()
#                     print(data['items'])
#                     all_data.append(data.items)

#                     # Loop through the items in the response
                    

#                         # Insert data into the PostgreSQL database
                        

#                     # Check if there are more pages
#                     if data.get("maxPages", 1) <= page:
#                         break
#                     else:
#                         page += 1
                
                    
#             else:
#                 print(f"Failed to retrieve data for coa={coa}, year={year}, page={page}. Status code:",
#                       response.status_code)
#                 break
    