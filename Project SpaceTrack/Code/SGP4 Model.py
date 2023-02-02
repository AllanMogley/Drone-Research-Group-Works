import datetime
import TLEs
from orbit_predictor.sources import EtcTLESource
from orbit_predictor import locations
from orbit_predictor.sources import get_predictor_from_tle_lines


predictor = get_predictor_from_tle_lines(TLEs.LS8)


# My Location of interest
# ----------------------------------------------------------------------------------
JUJA = locations.Location("JUJA", latitude_deg=-1.1018, longitude_deg=37.0144,
                            elevation_m=1519)


# Predict Next Pass
# ----------------------------------------------------------------------------------
next_pass = datetime.datetime.utcnow() + datetime.timedelta(days=-8)
print(predictor.get_next_pass(JUJA, next_pass, max_elevation_gt=30))
# print(predictor.get_position(datetime.datetime(2019, 1, 1))).
