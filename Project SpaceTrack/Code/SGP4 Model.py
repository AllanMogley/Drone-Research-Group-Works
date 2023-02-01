import datetime
import TLEs
from orbit_predictor.sources import EtcTLESource
from orbit_predictor import locations
from orbit_predictor.sources import get_predictor_from_tle_lines


# Satelitte TLE values (Landsat 8)
# ----------------------------------------------------------------------------------
TLE_LINES = (
            "1 39084U 13008A   23029.41611366  .00000452  00000+0  11041-3 0  9990",
            "2 39084  98.1979 101.5520 0001124  81.3714 278.7612 14.57109848529900")


# print(dir(TLEs))
predictor = get_predictor_from_tle_lines(TLEs.S2A)


# My Location of interest
# ----------------------------------------------------------------------------------
JUJA = locations.Location("JUJA", latitude_deg=-1.1018, longitude_deg=37.0144,
                            elevation_m=1519)


# Predict Next Pass
# ----------------------------------------------------------------------------------
next_pass = datetime.datetime.utcnow() + datetime.timedelta(days=0)
print(predictor.get_next_pass(JUJA, next_pass, max_elevation_gt=30))
# print(predictor.get_position(datetime.datetime(2019, 1, 1))).