def calculate_vo2max_6min(distance_km):
    return round(distance_km * 33, 2)

# Function to calculate VO2Max for the Cooper Test
def calculate_vo2max_cooper(distance_km):
    distance_meters = distance_km * 1000
    return round((distance_meters - 504.9) / 44.73, 2)



def calculate_performance_decrease(time_800m, time_200m):
    if time_800m > 0 and time_200m > 0:
        decrease = (time_800m / 4) - time_200m
        return round(decrease, 2)
    return None

# Function to calculate RAST power
def calculate_power(body_mass, distance, time):
    if time > 0:
        return round((body_mass * (distance**2)) / (time**3), 2)
    return 0

# Function to calculate fatigue index for RAST
def rast_fatigue_index(peak_power, lowest_power, sprint_times):
    if peak_power > 0:
        return round(((peak_power - lowest_power) / sum(sprint_times)) , 2)
    return 0

def wingate_fatigue_index(peak_power, lowest_power):
    if peak_power > 0:
        return round(((peak_power - lowest_power) / peak_power) * 100 , 2)
    return 0
def performance_decrease_perc(time_800m, time_200m):
    if time_800m > 0 and time_200m > 0:
        decrease = ((time_800m - (time_200m * 4)) / time_800m)
        return round(decrease, 2) * 100
  