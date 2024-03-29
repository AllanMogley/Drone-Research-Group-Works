import json
from landsatxplore.api import API
import datetime


# Read Username and Password from Loginss.txt
with open("Project SpaceTrack/Code/APIs/Logins.txt") as file: # type: ignore
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
    start_date='2023-05-20',
    end_date='2023-12-31'
    # max_cloud_cover=90
)


def l_sat_dates():
    # Process the result
    passes = []  # Create an empty list
    print(f"{len(scenes)} scenes found.")
    for scene in scenes:
        dates = scene['acquisition_date'].strftime('%Y-%m-%d')
        # print(dates)
        passes.append(dates)  
    last_Pass = passes[:1]
    last_Pass2 = myList = last_Pass[0].split('-')
    # print(type(last_Pass[:1]))

    global year # Make year variblae accessible globally
    year = last_Pass2[0]
    # print(year)

    montha = last_Pass2[1]
    monthb = [ele.lstrip('0') for ele in montha[1]] # Strip zero value
    global month # Make month variblae accessible globally
    month = monthb[0]
    # print(month)

    global date # Make year variblae accessible globally
    date = last_Pass2[2]
    # print(date)



l_sat_dates()
myyear = int(year)
mymonth =int(month)
mydate = int(date)

lsat = datetime.datetime(myyear, mymonth, mydate) # type: ignore
print (lsat)



    # Export scene footprints to disk
    # fname = f"{scene['landsat_product_id']}.geojson"
    # with open(fname, "w") as f:
    #     json.dump(scene['spatial_coverage'].__geo_interface__, f)
# print(passes)
api.logout()


# Parameters
# ----------
# dataset : str
#     Case-insensitive dataset alias (e.g. landsat_tm_c1).
# longitude : float, optional
#     Longitude of the point of interest.
# latitude : float, optional
#     Latitude of the point of interest.
# bbox : tuple, optional
#     (xmin, ymin, xmax, ymax) of the bounding box.
# max_cloud_cover : int, optional
#     Max. cloud cover in percent (1-100).
# start_date : str, optional
#     YYYY-MM-DD
# end_date : str, optional
#     YYYY-MM-DD. Equal to start_date if not provided.
# months : list of int, optional
#     Limit results to specific months (1-12).
# max_results : int, optional
#     Max. number of results. Defaults to 100.

# Returns
# -------
# scenes : list of dict
#     Matching scenes as a list of dict containing metadata.
# """