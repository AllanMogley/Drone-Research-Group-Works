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



predictor = get_predictor_from_tle_lines(TLEs.LS8)

def satelitte():
    if predictor.sate_id == 39084:
        n = 16
        print("\nLANDSAT 8")
        return n

    elif predictor.sate_id == 39634:
        n = 24
        print("\nSENTINEL 1A")
        return n

    elif predictor.sate_id == 41335:
        n = 24
        print("\nSENTINEL 1B")
        return n

    elif predictor.sate_id == 40697:
        n = 10
        print("\nSENTINEL 2A")
        return n



# Predict Next Pass
# ----------------------------------------------------------------------------------
x = range(0, (satelitte())*5, satelitte())
print("\n\n")
for i in x:
    next_pass = datetime.datetime(2022, 12, 10) + datetime.timedelta(days = i)
    print("Day", i)
    print(predictor.get_next_pass(JUJA, next_pass, max_elevation_gt=30))


# print(predictor.get_position(datetime.datetime(2022, 11, 24)))
