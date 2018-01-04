from music_events import EventContainer
from postGIS_connection import PostGIS_connection
import requests
import time
import random
import json

class GeolocationResolver:
    api_key = 'GOOGLE_API_KEY'
    base_url='https://maps.googleapis.com/maps/api/geocode/json?address='
    def __init__(self, container):
        self.container = container
        self.postgisDB = PostGIS_connection()

    def resolve_location(self, location):
        url = '{}{}&key={}'.format(GeolocationResolver.base_url, 
                                   location.replace(' ','+'),
                                   GeolocationResolver.api_key)
        r = requests.get(url)
        res = json.loads(r.text)
        try:
            loc = res['results'][0]['geometry']['location']
            neighborhood = self.postgisDB.get_neighborhood_name(loc['lng'], loc['lat'])
            self.update_location(location, loc['lat'], loc['lng'], neighborhood)
        except:
            print("Cannot resolve location from name")

    def resolve_all(self):
        for location in self.container.locations:
            self.resolve_location(location)
            time.sleep(random.uniform(0,2))
    
    def update_location(self, location, lat, lng, neighborhood):
        self.container.locations[location].set_lat(lat)
        self.container.locations[location].set_lng(lng)
        self.container.locations[location].set_neighborhood(neighborhood)
        print(neighborhood)
