import time

import requests
import json
import random
import geopandas as gpd
from shapely.geometry import Polygon, Point
from dotenv import load_dotenv
import os

class RandomStreetView:
    def __init__(self, shape_data_path='data/geo_boundaries/geoBoundariesCGAZ_ADM0.shp', valid_street_view_path='data/street_view_data/valid_street_views.jsonl'):
        """
        Example data:
        shapeGroup AFG
        shapeType ADM0
        shapeName Afghanistan
        geometry POLYGON ((74.889862 37.23409, 74.889616 37.233...
        Name: 0, dtype: object
        """
        # print(self.shape_data.loc[0]['shapeName'])
        self.shape_data = gpd.read_file(shape_data_path)
        load_dotenv()
        self.google_api_key = os.getenv("GOOGLE_API_KEY")
        self.valid_street_view_path = valid_street_view_path
    def generate_random_coordinates(self, iso_country_code=None):
        iso_country_index = None
        if not iso_country_code:
            iso_country_index = random.randrange(len(self.shape_data))
        else:
            for i in range(len(self.shape_data)):
                if self.shape_data.loc[i]['shapeGroup'] == iso_country_code:
                    iso_country_index = i
            if not iso_country_index:
                raise ValueError('Invalid iso country code')

        country_polygon = self.shape_data.loc[iso_country_index]['geometry']
        while True:
            min_lon, min_lat, max_lon, max_lat = country_polygon.bounds
            random_lon = random.uniform(min_lon, max_lon)
            random_lat = random.uniform(min_lat, max_lat)
            if country_polygon.contains(Point(random_lon, random_lat)):
                return random_lon, random_lat, self.shape_data.loc[iso_country_index]

    def check_valid_streetview(self, coords):

        # Note: Google deems it valid if the coordinate is < 50 m from a street view
        # Therefore, response lat & lon could differ from input
        res = requests.get(f'https://maps.googleapis.com/maps/api/streetview/metadata?location={coords[1]},{coords[0]}&key={self.google_api_key}')
        if res.json()['status'] != 'OK':
            return False
        return True

    def check_and_save_valid_streetview(self, coords, country_data=None, verbose=False):
        res = requests.get(f'https://maps.googleapis.com/maps/api/streetview/metadata?location={coords[1]},{coords[0]}&key={self.google_api_key}')
        if verbose:
            print(res.json())
        if res.json()['status'] == 'OK':
            with open(self.valid_street_view_path, 'a') as f:
                if country_data is None:
                    json.dump(res.json(), f)
                    f.write('\n')
                else:
                    json.dump({'iso3': country_data['shapeGroup'], 'name': country_data['shapeName'], 'street_view_metadata': res.json()}, f)
                    f.write('\n')
            return True
        return False

    def save_street_view_from_official_api(self, coords):

        res = requests.get(f'https://maps.googleapis.com/maps/api/streetview?size=600x400&location={coords[1]},{coords[0]}&key={self.google_api_key}')
        if res.json()['status'] == 'OK':
            with open('data/street_view_data/pic.jpg', 'w') as f:
                f.write(res.content)
                return True
        return False

if __name__ == '__main__':
    random_street_view = RandomStreetView('data/geo_boundaries/geoBoundariesCGAZ_ADM0.shp', 'data/street_view_data/valid_street_views_with_country.jsonl')
    while True:
        lon, lat, country = random_street_view.generate_random_coordinates()
        random_street_view.check_and_save_valid_streetview((lon, lat), country, True)
        time.sleep(.001)
