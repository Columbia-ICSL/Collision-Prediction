#!/usr/bin/python
#coding:utf-8
######save the 'trip_save_nyc_taxi_2014.csv' from raw dataset######
###format: [pickup_lat,pickup_lon,dropoff_lat,dropoff_lon,points]###
import numpy as np
import pandas as pd
import apiKey
import googlemaps

gmaps_1 = googlemaps.Client(key=apiKey.mykey1)
trip=[]# all trips from nyc_taxi_data
###format: [pickup_latitude,pickup_longtitude,dropoff_latitude,dropoff_longtitude]###
trip_filtered = [] # trips in midtown Manhattan
###format: [pickup_latitude,pickup_longtitude,dropoff_latitude,dropoff_longtitude]###
trip_traject = [] #add points from google map direction api to trip_filtered
###format: [pickup_latitude,pickup_longtitude,dropoff_latitude,dropoff_longtitude,points]###

#---------Midtown Manhattan Bound--------
lat_low = 40.739045
lat_high = 40.763321
lon_left = -74.0066
lon_right = -73.962742
#---------Midtown Manhattan Bound--------

#----------------Load Trip-------------

taxiFile = pd.read_csv('nyc_taxi_data_2014.csv',nrows = 100000,usecols=['pickup_longitude', 'pickup_latitude', 'dropoff_longitude','dropoff_latitude'])
for i in range(len(taxiFile)):
    line = taxiFile.ix[i]
    trip.append(line)

print len(trip)

#----------------Filter Trip-------------

for item in trip:
    if(item[1]>lat_low and item[1]<lat_high and item[3]>lat_low and item[3]<lat_high and item[0]> lon_left and item[0]< lon_right and item[2]> lon_left and item[2]< lon_right ):
        trip_filtered.append([item[1],item[0],item[3],item[2]])
    else:
        continue

print len(trip_filtered) # 17,448 in first 100,000

# -----------------Get Trajectory Points---------------

for i in range(len(trip_filtered)):
    trip_traject.append([])
    direction_result = gmaps_1.directions(origin=(trip_filtered[i][0], trip_filtered[i][1]), destination=(trip_filtered[i][2], trip_filtered[i][3]),
                                        mode="driving")
    points = direction_result[0]['overview_polyline']['points']
    print points
    trip_filtered[i].append(points)
    trip_traject[i].append(trip_filtered[i][0])
    trip_traject[i].append(trip_filtered[i][1])
    trip_traject[i].append(trip_filtered[i][2])
    trip_traject[i].append(trip_filtered[i][3])
    trip_traject[i].append(points)
trip_save = np.array(trip_traject)
print np.shape(trip_save)
dataframe = pd.DataFrame({'pickup_lat': trip_save[:, 0], 'pickup_lon': trip_save[:, 1],'dropoff_lat':trip_save[:,2],'dropoff_lon':trip_save[:,3],'points':trip_save[:,4]})
dataframe.to_csv("trip_save_nyc_taxi_2014.csv", index=False, header=False)
print "Ok"


