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
    api_key = ''
    print(all_data)
    items_list = [item for entry in all_data for item in entry['items']]
    print(items_list)
    coordinates_list = []
    # Create the URL for the request
    for dat in items_list:
        print(f"coa_name: {dat['coa_name']}")
        card_data= {
            'year': dat['year'],
            'coo_name': dat['coo_name'],
            'coa_name': dat['coa_name'],
            'applications': dat['applied'],
            'decision_level': dat['dec_level'],
        }
        print(f"card_data: {card_data}")
        
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
                    'content': coa_name,
                    'card_data': card_data
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

        
        
  
    
    context['coordinates_list_json'] = json.dumps(coordinates_list)
            
    return render(request, 'map/index.html', context)