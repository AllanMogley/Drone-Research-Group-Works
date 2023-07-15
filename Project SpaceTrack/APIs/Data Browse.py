import json
from landsatxplore.api import API


# Read Username and Password from Loginss.txt
with open("Project SpaceTrack/APIs/Logins.txt") as file:
   lines = file.read()
   username = lines.split('\n')[0].lstrip()
   password = lines.split('\n')[1].lstrip()

# print(username)
# print(password)


# Initialize a new API instance and get an access key
api = API(username, password)


# Search for Landsat TM scenes
scenes = api.search(
    dataset='landsat_ot_c2_l1',
    latitude=-1.1018,
    longitude=37.0144,
    start_date='2023-06-20',
    end_date='2023-12'
    # max_cloud_cover=90
)

print(f"{len(scenes)} scenes found.")

# Process the result
passes = []  # Create an empty list
for scene in scenes:
    print(scene['acquisition_date'].strftime('%Y-%m-%d'))
    # passes.append(scene)  Fill List with LS8/9 PassDates


    # Export scene footprints to disk
    # fname = f"{scene['landsat_product_id']}.geojson"
    # with open(fname, "w") as f:
    #     json.dump(scene['spatial_coverage'].__geo_interface__, f)
# print(passes)
api.logout()
