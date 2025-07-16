import json
import time
import os
import random
from rsv import StreetViewLocation

headers = {
    "accept": "image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8",
    "accept-encoding": "gzip, deflate, br, zstd",
    "accept-language": "en-US,en;q=0.9",
    "dnt": "1",
    "origin": "https://www.google.com",
    "priority": "i",
    "referer": "https://www.google.com/",
    "sec-ch-ua": '"Not)A;Brand";v="8", "Chromium";v="138", "Google Chrome";v="138"',
    "sec-ch-ua-mobile": "?0",
    "sec-ch-ua-platform": '"macOS"',
    "sec-fetch-dest": "image",
    "sec-fetch-mode": "cors",
    "sec-fetch-site": "cross-site",
    "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36",
    "x-browser-copyright": "Copyright 2025 Google LLC. All rights reserved.",
    "x-browser-validation": "qvLgIVtG4U8GgiRPSI9IJ22mUlI=",
    "x-browser-year": "2025",
    "x-client-data": "CJC2yQEIpLbJAQipncoBCOfrygEIk6HLAQijo8sBCIagzQEIpfLOAQiS9s4BCJn3zgEI9vnOAQjf+84BGMr6zgE="
}

with open('data/street_view_data/batch1.jsonl', 'r') as f:
    for line in f.readlines():
        data = json.loads(line)
        lat = data['street_view_metadata']['location']['lat']
        lng = data['street_view_metadata']['location']['lng']
        location = StreetViewLocation(latitude=lat, longitude=lng, pano_id=data['street_view_metadata']['pano_id'], country_code=data['name'])
        path = f'data/street_view_data/street_view_images/{data['iso3']}_{lat}_{lng}'
        if os.path.exists(path):
            continue
        os.mkdir(path)
        location.save_street_view_unofficial(request_headers=headers, zoom_level=3, folder_path=path)
        time.sleep(random.uniform(.5, 10))
