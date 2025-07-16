import random
from rsv import RSV, StreetViewLocation
import geopandas as gpd
from dotenv import load_dotenv
import os
street_view_countries_iso3 = [
        "ALB",  # Albania
        "AND",  # Andorra
        "ARG",  # Argentina
        "AUS",  # Australia
        "AUT",  # Austria
        "BGD",  # Bangladesh
        "BEL",  # Belgium
        "BTN",  # Bhutan
        "BOL",  # Bolivia
        "BWA",  # Botswana
        "BRA",  # Brazil
        "BGR",  # Bulgaria
        "KHM",  # Cambodia
        "CAN",  # Canada
        "CHL",  # Chile
        "COL",  # Colombia
        "HRV",  # Croatia
        "CZE",  # Czechia
        "DNK",  # Denmark
        "DOM",  # Dominican Republic
        "ECU",  # Ecuador
        "EST",  # Estonia
        "SWZ",  # Eswatini (Swaziland)
        "FIN",  # Finland
        "FRA",  # France
        "DEU",  # Germany
        "GRC",  # Greece
        "GRL",  # Greenland
        "GTM",  # Guatemala
        "HUN",  # Hungary
        "ISL",  # Iceland
        "IND",  # India
        "IDN",  # Indonesia
        "IRL",  # Ireland
        "ISR",  # Israel
        "ITA",  # Italy
        "JPN",  # Japan
        "JOR",  # Jordan
        "KAZ",  # Kazakhstan
        "KEN",  # Kenya
        "KGZ",  # Kyrgyzstan
        "LAO",  # Laos
        "LVA",  # Latvia
        "LSO",  # Lesotho
        "LTU",  # Lithuania
        "LUX",  # Luxembourg
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
        "NOR",  # Norway
        "PAN",  # Panama
        "PER",  # Peru
        "PHL",  # Philippines
        "POL",  # Poland
        "PRT",  # Portugal
        "QAT",  # Qatar
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
        "URY",  # Uruguay
    ]
load_dotenv()

while True:
    random_street_view = RSV(os.getenv('GOOGLE_API_KEY'), gpd.read_file("./data/geo_boundaries/geoBoundariesCGAZ_ADM0.shp"))
    rnd = random.choice(street_view_countries_iso3)
    location = random_street_view.generate_valid_location(rnd)
    location.save_metadata('data/street_view_data/batch2.jsonl')
