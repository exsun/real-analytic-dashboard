def calculate_vo2max_6min(distance_km):
    return round(distance_km * 33, 2)

# Function to calculate VO2Max for the Cooper Test
def calculate_vo2max_cooper(distance_km):
    distance_meters = distance_km * 1000
    return round((distance_meters - 504.9) / 44.73, 2)


