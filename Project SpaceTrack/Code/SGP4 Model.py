import datetime
import TLEs
from orbit_predictor.sources import EtcTLESource
from orbit_predictor import locations
from orbit_predictor.sources import get_predictor_from_tle_lines



# My Location of interest
# ----------------------------------------------------------------------------------
JUJA = locations.Location("JUJA", latitude_deg=-1.1018, longitude_deg=37.0144,
                            elevation_m=1519)
# ----------------------------------------------------------------------------------



predictor = get_predictor_from_tle_lines(TLEs.S2A)

def satelitte():
    if predictor.sate_id == 39084:
        n = 16
        print("LANDSAT 8")
        return n

    elif predictor.sate_id == 39634:
        n = 24
        print("SENTINEL 1A")
        return n

    elif predictor.sate_id == 41335:
        n = 24
        print("SENTINEL 1B")
        return n

    elif predictor.sate_id == 40697:
        n = 10
        print("SENTINEL 2A")
        return n


sentinel2A = datetime.datetime(2022, 12, 9)
landsat8 = datetime.datetime(2022, 12, 10)

# Predict Next Pass
# ----------------------------------------------------------------------------------
T = datetime.datetime.now()
x = range(0, (satelitte())*5, satelitte())
# print("\n\n")
for i in x:
    next_pass = sentinel2A + datetime.timedelta(days = i)
    print("Day", i)
    print(predictor.get_next_pass(JUJA, next_pass, max_elevation_gt=30))
print("\n\n\n")
# ----------------------------------------------------------------------------------


# Update Predicted Passes at the end of loop
# ----------------------------------------------------------------------------------
if next_pass != T:

    for i in x:
        next_pass2 = next_pass + datetime.timedelta(days = i)
        print("Day", i)
        print(predictor.get_next_pass(JUJA, next_pass2, max_elevation_gt=30))
        print(next_pass2)

# ----------------------------------------------------------------------------------

# print(predictor.get_position(datetime.datetime(2022, 11, 24)))
