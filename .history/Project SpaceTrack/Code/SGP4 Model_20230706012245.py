import datetime
import TLEs
from orbit_predictor import locations
from orbit_predictor.sources import get_predictor_from_tle_lines


# ----------------------------------------------------------------------------------
# My Location of interest
# ----------------------------------------------------------------------------------
JUJA = locations.Location("JUJA", latitude_deg=-0.6507289449113348,
                          longitude_deg=37.38098941349445, elevation_m=1150)
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


# ----------------------------------------------------------------------------------
# Define Update Date Range
# ----------------------------------------------------------------------------------
T = datetime.datetime.today()
T2ls8 = T + datetime.timedelta(days = satelitte()*6 )
T2s2A = T + datetime.timedelta(days = satelitte2()*6 )
# ----------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
# Predict LANDSAT8 Next Pass
# ----------------------------------------------------------------------------------
x = range(0, (satelitte())*6, satelitte())
print("\n\n")
print("LANDSAT 8")
print("TODAYS DATE", T.date())
print("AFTER 5 EPOCHS END DATE", T2ls8.date())

passes = []  #Create an empty list
for i in x:
    landsat8 = datetime.datetime(2023, 1, 4)
    next_pass = landsat8 + datetime.timedelta(days = i)
    passes.append(next_pass) # Stores the passes to the passes[] list

    if next_pass <= T2ls8:
        print("Day", i, next_pass.strftime('%A'))
        print(predictor.get_next_pass(JUJA, next_pass, max_elevation_gt=30))


print("\n\n")
print(len(passes))
print("Initial Pass = ", landsat8) # type: ignore
print("Last Pass = ", passes[5])
landsat8 = passes[5]
print("Updated Initial Pass = ", landsat8)
# ----------------------------------------------------------------------------------



# ----------------------------------------------------------------------------------
# Predict SENTINEL2A Next Pass
# ----------------------------------------------------------------------------------
# x2 = range(0, (satelitte2())*6, satelitte2())
# print("\n\n")
# print("SENTINEL 2A")
# print("TODAYS DATE", T.date())
# print("AFTER 5 EPOCHS END DATE", T2s2A.date())
# for j in x2:
    # sentinel2A = datetime.datetime(2023, 5, 28)
#     next_pass2 = sentinel2A + datetime.timedelta(days = j)

#     if next_pass2 <= T2s2A:
#         print("Day", j, next_pass2.strftime('%A'))
#         print(predictor.get_next_pass(JUJA, next_pass2, max_elevation_gt=30))
# ----------------------------------------------------------------------------------