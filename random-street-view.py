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

    def check_and_save_valid_streetview(self, coords, country_data, verbose=False):
        res = requests.get(f'https://maps.googleapis.com/maps/api/streetview/metadata?location={coords[1]},{coords[0]}&key={self.google_api_key}&radius=50000&source=outdoor')
        if verbose:
            print(res.json())
        if res.json()['status'] == 'OK':
            if country_data['geometry'].contains(Point(res.json()['location']['lng'], res.json()['location']['lat'])):
                with open(self.valid_street_view_path, 'a') as f:
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
    random_street_view = RandomStreetView('data/geo_boundaries/geoBoundariesCGAZ_ADM0.shp', 'data/street_view_data/valid_street_views_with_country_fixed.jsonl')
    street_view_countries_iso3 = [
        "ALB",  # Albania
        "AND",  # Andorra
        "ARG",  # Argentina
        "ASM",  # American Samoa
        "AUS",  # Australia
        "AUT",  # Austria
        "BGD",  # Bangladesh
        "BEL",  # Belgium
        "BMU",  # Bermuda
        "BTN",  # Bhutan
        "BOL",  # Bolivia
        "BWA",  # Botswana
        "BRA",  # Brazil
        "BGR",  # Bulgaria
        "KHM",  # Cambodia
        "CAN",  # Canada
        "CHL",  # Chile
        "CXR",  # Christmas Island
        "COL",  # Colombia
        "HRV",  # Croatia
        "CUW",  # Curaçao
        "CZE",  # Czechia
        "DNK",  # Denmark
        "DOM",  # Dominican Republic
        "ECU",  # Ecuador
        "EST",  # Estonia
        "SWZ",  # Eswatini (Swaziland)
        "FRO",  # Faroe Islands
        "FIN",  # Finland
        "FRA",  # France
        "DEU",  # Germany
        "GIB",  # Gibraltar
        "GRC",  # Greece
        "GRL",  # Greenland
        "GUM",  # Guam
        "GTM",  # Guatemala
        "GGY",  # Guernsey
        "HKG",  # Hong Kong
        "HUN",  # Hungary
        "ISL",  # Iceland
        "IND",  # India
        "IDN",  # Indonesia
        "IRL",  # Ireland
        "IMN",  # Isle of Man
        "ISR",  # Israel
        "ITA",  # Italy
        "JPN",  # Japan
        "JEY",  # Jersey
        "JOR",  # Jordan
        "KAZ",  # Kazakhstan
        "KEN",  # Kenya
        "KGZ",  # Kyrgyzstan
        "LAO",  # Laos
        "LVA",  # Latvia
        "LSO",  # Lesotho
        "LTU",  # Lithuania
        "LUX",  # Luxembourg
        "MAC",  # Macao
        "MYS",  # Malaysia
        "MLT",  # Malta
        "MEX",  # Mexico
        "MCO",  # Monaco
        "MNG",  # Mongolia
        "MNE",  # Montenegro
        "NLD",  # Netherlands
        "NZL",  # New Zealand
        "NGA",  # Nigeria
        "MKD",  # North Macedonia
        "MNP",  # Northern Mariana Islands
        "NOR",  # Norway
        "PSE",  # Palestine
        "PAN",  # Panama
        "PER",  # Peru
        "PHL",  # Philippines
        "PCN",  # Pitcairn Islands
        "POL",  # Poland
        "PRT",  # Portugal
        "PRI",  # Puerto Rico
        "QAT",  # Qatar
        "REU",  # Réunion
        "ROU",  # Romania
        "RUS",  # Russia
        "RWA",  # Rwanda
        "SMR",  # San Marino
        "SEN",  # Senegal
        "SRB",  # Serbia
        "SGP",  # Singapore
        "SVK",  # Slovakia
        "SVN",  # Slovenia
        "ZAF",  # South Africa
        "KOR",  # South Korea
        "ESP",  # Spain
        "LKA",  # Sri Lanka
        "SWE",  # Sweden
        "CHE",  # Switzerland
        "TWN",  # Taiwan
        "TZA",  # Tanzania
        "THA",  # Thailand
        "TUN",  # Tunisia
        "TUR",  # Turkey
        "UGA",  # Uganda
        "UKR",  # Ukraine
        "ARE",  # United Arab Emirates
        "GBR",  # United Kingdom
        "USA",  # United States
        "VIR",  # United States Virgin Islands
        "URY",  # Uruguay
    ]
    while True:
        lon, lat, country = random_street_view.generate_random_coordinates()
        while True:
            if country['shapeGroup'] not in street_view_countries_iso3 or random_street_view.check_and_save_valid_streetview((lon, lat), country):
                break
            else:
                lon, lat, country = random_street_view.generate_random_coordinates(country['shapeGroup'])

        time.sleep(.001)
