import urllib
import json
import pandas as pd
import numpy as np
import apiKey
import googlemaps

'''
gmaps = googlemaps.Client(key=mykey2)

response = gmaps.geocode(address = 'West+34,+9+Avenue,+NY')
print response

'''
intersection_latlon = []
behind = ['st', 'nd', 'rd', 'th', 'th', 'th', 'th', 'th', 'th', 'th', 'th']
fourthAve = ['Lexington', 'Park', 'Madison']


def get_intersection(url):
    response_url = urllib.urlopen(url).read()
    intersection = json.loads(response_url)
    if (intersection['results']):
        lat = intersection['results'][0]['geometry']['location']['lat']
        lon = intersection['results'][0]['geometry']['location']['lng']
        intersection_latlon.append([lat, lon])
        print((lat,lon))
    else:
        print('Error zero_results')



for st in range(14, 60):
    for ave in range(1, 12):
        if (ave == 4):
            for item in fourthAve:
                url = 'https://maps.googleapis.com/maps/api/geocode/json?address=East+' + str(st) + ',+' + \
                      item + '+Avenue,+NY&key='+apiKey.mykey3
                get_intersection(url)
        else:
            if (ave >= 5):
                url = 'https://maps.googleapis.com/maps/api/geocode/json?address=West+' + str(st) + ',+' + \
                      str(ave) + behind[ave - 1] + '+Avenue,+NY&key='+apiKey.mykey3
                get_intersection(url)
            else:
                url = 'https://maps.googleapis.com/maps/api/geocode/json?address=East+' + str(st) + ',+' + \
                      str(ave) + behind[ave - 1] + '+Avenue,+NY&key='+apiKey.mykey3
                get_intersection(url)

intersection_array = np.array(intersection_latlon)
dataframe = pd.DataFrame({'lat': intersection_array[:, 0], 'lon': intersection_array[:, 1]})
dataframe.to_csv("intersection2.csv", index=False, header=False)


