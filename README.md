# Random Street View

Generate random valid Google Street View locations inside country boundaries, save their Street View metadata as JSONL, and optionally download the corresponding Street View image.

The project samples random latitude/longitude points inside country polygons from a geoBoundaries shapefile, checks the Google Street View metadata endpoint for nearby imagery, and records successful panorama matches.

## Features

- Sample random points within country boundaries.
- Restrict sampling to a specific ISO 3166-1 alpha-3 country code.
- Validate that Google Street View imagery exists near the sampled point.
- Save valid Street View metadata to JSONL.
- Download Street View images for valid locations.

## Project Structure

```text
.
├── rsv.py                                  # Core Street View sampling classes
├── run.py                                  # Long-running metadata collection script
├── requirements.txt                        # Python dependencies
├── example.env                             # Environment variable template
├── valid_street_views_with_country.jsonl   # Example collected metadata
├── data/
│   ├── geo_boundaries/                     # Local geoBoundaries shapefile files
│   └── street_view_data/                   # Generated JSONL output
└── tests/
    └── tests.py                            # API-backed smoke test
```

## Requirements

- Python 3.10+
- A Google Maps API key with access to the Street View Static API
- geoBoundaries country shapefile files for ADM0 boundaries

The code expects this shapefile path:

```text
data/geo_boundaries/geoBoundariesCGAZ_ADM0.shp
```

The shapefile sidecar files, such as `.dbf`, `.shx`, and `.prj`, must be present in the same directory.

## Setup

Create and activate a virtual environment:

```bash
python -m venv .venv
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create a local `.env` file from the template:

```bash
cp example.env .env
```

Then edit `.env`:

```env
GOOGLE_API_KEY=your_google_maps_api_key
```

## Usage

Run the collector script:

```bash
python run.py
```

`run.py` continuously chooses a random country from its configured list, searches for valid Street View imagery, and appends successful metadata records to:

```text
data/street_view_data/valid_street_views_with_country_fixed.jsonl
```

Stop the script with `Ctrl+C`.

## Library Example

```python
import os
import geopandas as gpd
from dotenv import load_dotenv
from rsv import RSV

load_dotenv()

shape_data = gpd.read_file("data/geo_boundaries/geoBoundariesCGAZ_ADM0.shp")
random_street_view = RSV(os.getenv("GOOGLE_API_KEY"), shape_data)

location = random_street_view.generate_valid_location("USA")
location.save_metadata("data/street_view_data/usa_locations.jsonl")
location.save_street_view(
    os.getenv("GOOGLE_API_KEY"),
    size=(600, 400),
    file_path="data/street_view_data/usa_location.jpeg",
)
```

## Output Format

Metadata is saved as one JSON object per line:

```json
{
  "iso3": "USA",
  "name": "United States",
  "street_view_metadata": {
    "copyright": "© Google",
    "date": "2024-07",
    "location": {
      "lat": 40.0,
      "lng": -75.0
    },
    "pano_id": "example_panorama_id",
    "status": "OK"
  }
}
```

## Tests

The test script calls the Google Street View API and writes output under `tests/results/`, so it requires a valid `.env` file and local shapefile data.

From the `tests` directory:

```bash
cd tests
python tests.py
```

## Notes

- The collector can run for a long time because it repeatedly samples random points until it finds Street View imagery.
- Google API usage may incur costs depending on your Google Cloud billing setup and quota configuration.
- Generated Street View data and downloaded images should be treated according to the Google Maps Platform terms that apply to your API key.
