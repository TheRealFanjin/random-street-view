import time
import httpx
import requests
import json
import random
import geopandas as gpd
from shapely.geometry import Polygon, Point
import os
from typing import Tuple
from pathlib import Path

class StreetViewLocation:
    def __init__(self, latitude: float = None, longitude: float = None, country_code: str = None, country_name: str = None, pano_id: str = None, street_view_metadata: dict = None):

        # If user provided incomplete location data
        if (not street_view_metadata and not latitude) or (not street_view_metadata and not longitude):
            raise TypeError('Either street_view_metadata or latitude and longitude must be provided')

        if street_view_metadata:
            self.latitude = street_view_metadata['location']['lat']
            self.longitude = street_view_metadata['location']['lng']
            self.street_view_metadata = street_view_metadata
        else:
            # street_view_metadata overrides latitude and longitude
            self.latitude = latitude
            self.longitude = longitude

        self.country_code = country_code
        self.country_name = country_name
        self.pano_id = pano_id

    def check_and_update_country(self, shape_data: gpd.GeoDataFrame):
        for i in range(len(shape_data)):
            country_polygon = shape_data.loc[i]['geometry']
            if country_polygon.contains(Point(self.longitude, self.latitude)):
                self.country_code = shape_data.loc[i]['shapeGroup']
                self.country_name = shape_data.loc[i]['shapeName']
                return self.country_name
        raise ValueError('Latitude and longitude not found in provided country shape data')

    def check_and_update_pano_id(self, google_api_key: str):
        self.pano_id = requests.get(
            f'https://maps.googleapis.com/maps/api/streetview/metadata?location={self.latitude},{self.longitude}&key={google_api_key}').json()['pano_id']

    def save_metadata(self, file_path: str = str(Path(os.getcwd()) / 'street_view_metadata.jsonl')):
        with open(file_path, 'a') as f:
            json.dump({'iso3': self.country_code, 'name': self.country_name,
                       'street_view_metadata': self.street_view_metadata}, f)
            f.write('\n')

    def save_street_view(self, google_api_key: str, size: Tuple[int, int] = (600, 400), file_path: str = str(Path(os.getcwd()) / f'{int(time.time())}.jpeg')):
        res = requests.get(
            f'https://maps.googleapis.com/maps/api/streetview?size={size[0]}x{size[1]}&location={self.latitude},{self.longitude}&key={google_api_key}')
        if res.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(res.content)

class RSV:
    def __init__(self, google_api_key: str, shape_data: gpd.GeoDataFrame = f'{os.getcwd()}'):
        self.shape_data = shape_data
        self.google_api_key = google_api_key

    def generate_valid_location(self, iso_country_code: str = None) -> StreetViewLocation:
        iso_country_index = None
        if not iso_country_code:
            iso_country_index = random.randrange(len(self.shape_data))
        else:
            for i in range(len(self.shape_data)):
                if self.shape_data.loc[i]['shapeGroup'] == iso_country_code:
                    iso_country_index = i
                    break
            if not iso_country_index:
                raise ValueError('Country not found in dataset', iso_country_code)

        country_polygon = self.shape_data.loc[iso_country_index]['geometry']
        while True:
            min_lon, min_lat, max_lon, max_lat = country_polygon.bounds
            random_lon = random.uniform(min_lon, max_lon)
            random_lat = random.uniform(min_lat, max_lat)
            if country_polygon.contains(Point(random_lon, random_lat)):
                street_view_metadata_res = requests.get(f'https://maps.googleapis.com/maps/api/streetview/metadata?location={random_lat},{random_lon}&key={self.google_api_key}&radius=50000')
                if street_view_metadata_res.status_code == 200 and street_view_metadata_res.json()['status'] == 'OK':
                    return StreetViewLocation(country_code=self.shape_data.loc[iso_country_index]['shapeGroup'], country_name=self.shape_data.loc[iso_country_index]['shapeName'], pano_id=street_view_metadata_res.json()['pano_id'], street_view_metadata=street_view_metadata_res.json())



