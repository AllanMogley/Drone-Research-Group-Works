import datetime
import TLEs
from orbit_predictor import locations
from orbit_predictor.sources import get_predictor_from_tle_lines


# ----------------------------------------------------------------------------------
# My Location of interest
# ----------------------------------------------------------------------------------
JUJA = locations.Location("JUJA", latitude_deg=-1.1018, longitude_deg=37.0144,
                            elevation_m=1519)
# ----------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
# Satelitte Revisit Periods
# ----------------------------------------------------------------------------------
predictor2 = get_predictor_from_tle_lines(TLEs.S2A)
predictor = get_predictor_from_tle_lines(TLEs.LS8)
def satelitte():
    if predictor.sate_id == 39084:
        # print("LANDSAT 8")
        n = 16
        return n

def satelitte2():
    if predictor2.sate_id == 40697:
        # print("SENTINEL 2A")
        n = 10
        return n

landsat8 = datetime.datetime(2023, 6, 4)

sentinel2A = datetime.datetime(2023, 5, 28)
# ----------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
# Define Update Date Range
# ----------------------------------------------------------------------------------
T = datetime.datetime.today()
T2ls8 = T + datetime.timedelta(days = satelitte()*5 )
T2s2A = T + datetime.timedelta(days = satelitte2()*5 )
# ----------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
# Predict LANDSAT8 Next Pass
# ----------------------------------------------------------------------------------
x = range(0, (satelitte())*5, satelitte())
print("\n\n")
print("LANDSAT 8")
print("TODAYS DATE", T.date())
print("AFTER 5 EPOCHS END DATE", T2ls8.date())

# while True:
for i in x:
    next_pass = landsat8 + datetime.timedelta(days = i)

    if next_pass <= T2ls8:
        print("Day", i, next_pass.strftime('%A'))
        print(predictor.get_next_pass(JUJA, next_pass, max_elevation_gt=30))

# landsat8 = next_pass
# ----------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
# Predict SENTINEL2A Next Pass
# ----------------------------------------------------------------------------------
x2 = range(0, (satelitte2())*5, satelitte2())
print("\n\n")
print("SENTINEL 2A")
print("TODAYS DATE", T.date())
print("AFTER 5 EPOCHS END DATE", T2s2A.date())
for j in x2:
    next_pass2 = sentinel2A + datetime.timedelta(days = j)

    if next_pass2 <= T2s2A:
        print("Day", j, next_pass2.strftime('%A'))
        print(predictor.get_next_pass(JUJA, next_pass2, max_elevation_gt=30))
# ----------------------------------------------------------------------------------