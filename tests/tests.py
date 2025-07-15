from rsv import RSV, StreetViewLocation
import geopandas as gpd
from dotenv import load_dotenv
import os

load_dotenv()
random_street_view = RSV(os.getenv('GOOGLE_API_KEY'), gpd.read_file(
    "../data/geo_boundaries/geoBoundariesCGAZ_ADM0.shp"))
location = random_street_view.generate_valid_location('USA')
location.save_metadata('results/test.jsonl')
location.save_street_view(os.getenv('GOOGLE_API_KEY'), file_path="results/test_pic.jpeg")