import datetime
from Satellite_Orbital_Parameters import TLEs #type: ignore
from orbit_predictor import locations
from orbit_predictor.sources import get_predictor_from_tle_lines
from APIs.DataBrowse import *


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
        n = 8
        return n

def satelitte2():
    if predictor2.sate_id == 40697:
        # print("SENTINEL 2A")
        n = 10
        return n


# ----------------------------------------------------------------------------------
# Define Update Date Range
# ----------------------------------------------------------------------------------
T = datetime.datetime.today()
T2ls8 = T + datetime.timedelta(days = satelitte()*15 ) # type: ignore
T2s2A = T + datetime.timedelta(days = satelitte2()*15 ) # type: ignore
# ----------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
# Predict LANDSAT8 Next Pass
# ----------------------------------------------------------------------------------
x = range(0, (satelitte())*11, satelitte()) # type: ignore
print("\n\n")
print("LANDSAT 8")
print("TODAYS DATE", T.date())
print("AFTER 15 EPOCHS END DATE", T2ls8.date())

passes = []  #Create an empty list
for i in x:
    landsat8 = datetime.datetime(myyear, mymonth, mydate)
    next_pass = landsat8 + datetime.timedelta( days= -i)
    passes.append(next_pass) # Stores the passes to the list

    if next_pass <= T2ls8:
        print("Day", i, next_pass.strftime('%A, %b %d'))

# ----------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
# Predict SENTINEL2A Next Pass
# ----------------------------------------------------------------------------------
x2 = range(0, (satelitte2())*11, satelitte2()) # type: ignore
print("\n\n")
print("SENTINEL 2A")
print("TODAYS DATE", T.date())
print("AFTER 11 EPOCHS END DATE", T2s2A.date())


passes2 = []  #Create an empty list
for j in x2:
    sentinel2A = datetime.datetime(2023, 7, 27)
    next_pass2 = sentinel2A + datetime.timedelta(days = j)
    passes2.append(next_pass) # type: ignore

    if next_pass2 <= T2s2A:
        print("Day", j, next_pass2.strftime('%A, %b %d'))

