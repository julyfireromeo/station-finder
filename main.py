import math
import csv
import pgeocode

def distancefinder(lon1, lat1, lon2, lat2):
    circ = 24901.461 

    #conversions
    deltaLon = math.radians(lon2 - lon1)
    lat1 = math.radians(lat1)
    lat2 = math.radians(lat2)

    #spherical law of cosines aghhh
    cos_pAng = math.sin(lat1)*math.sin(lat2)+math.cos(lat1)*math.cos(lat2)*math.cos(deltaLon)
    cos_pAng = max(-1.0, min(1.0, cos_pAng)) #NOT error maxxing

    pAng_r = math.acos(cos_pAng)
    pAng_d = math.degrees(pAng_r)
    
    arcl = (pAng_d/360)*circ #arc length
    return arcl

def zipcodetolat(zipcode): #uses pgeo
    nomi = pgeocode.Nominatim('us')
    r0 = nomi.query_postal_code(zipcode)
    return r0.latitude


def zipcodetolon(zipcode): #uses pgeo
    nomi = pgeocode.Nominatim('us')
    r1 = nomi.query_postal_code(zipcode)
    return r1.longitude

def zipcodetotownish(zipcode): #uses pgeo
    nomi = pgeocode.Nominatim('us')
    r2 = nomi.query_postal_code(zipcode)
    return r2.place_name

def stationfinder(user_lat, user_lon):
    nearest_station = None;
    dist = 0.0;
    min_distance = float('inf')

    #f stands for file!! the more you know...
    with open("NTAD_Amtrak_Stations_-8378338137364472090.csv", "r", ) as f:
        reader = csv.DictReader(f)

        for row in reader:
            station_lon = float(row['lon'])
            station_lat = float(row['lat'])

            dist = distancefinder(station_lon, station_lat, user_lon, user_lat)

            if dist < min_distance:
                min_distance = dist
                nearest_station = row

    if nearest_station:
        n = ""
        if nearest_station.get('StationName'):
            n = nearest_station.get('StationName')
        else:
            n = "This station has no official name"

        min_distance = round(min_distance, 3)
        
        return {
            'Name': n,
            'Location' : nearest_station.get('Name'),
            'Address': nearest_station.get('Address1'), # type: ignore
            'Minimum Distance to You': min_distance  # type: ignore
        }
        
    return None

zip = input('Please input your zipcode here: ')

print("You live in " + zipcodetotownish(zip) + " and your nearest Amtrak station is... ")
print(stationfinder(zipcodetolat(zip), zipcodetolon(zip)))


