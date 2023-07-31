import json
from landsatxplore.api import API
# from Logins import username, password

with open("Project SpaceTrack/APIs/Logins.txt") as file:
   lines = file.read()
   username = lines.split('\n')[0].lstrip()
   password = lines.split('\n')[1].lstrip()
   print(username)
   print(password)


# Initialize a new API instance and get an access key
api = API(username, password)



# Search for Landsat TM scenes
scenes = api.search(
    dataset='landsat_ot_c2_l1',
    latitude=-1.1018,
    longitude=37.0144,
    start_date='2023-05-19',
    end_date='2023-09-10',
    max_cloud_cover=50
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