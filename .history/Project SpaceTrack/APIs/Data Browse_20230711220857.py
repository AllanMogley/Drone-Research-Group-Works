import json
from landsatxplore.api import API

# Initialize a new API instance and get an access key
api = API("Allan_Mogley", "Christtheking99#")

# Search for Landsat TM scenes
scenes = api.search(
    dataset='landsat_tm_c2_l1',
    latitude=50.85,
    longitude=-4.35,
    start_date='2023-06-01',2023, 6, 20
    end_date='1995-10-01',
    max_cloud_cover=10
)

print(f"{len(scenes)} scenes found.")

# Process the result
for scene in scenes:
    print(scene['acquisition_date'].strftime('%Y-%m-%d'))
    # Write scene footprints to disk
    fname = f"{scene['landsat_product_id']}.geojson"
    with open(fname, "w") as f:
        json.dump(scene['spatial_coverage'].__geo_interface__, f)

api.logout()