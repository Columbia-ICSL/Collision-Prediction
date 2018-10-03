#!/usr/bin/python
#coding:utf-8
#########save the 'trajectoryLatLon_nyc_taxi_2014.csv' from 'trip_save_nyc_taxi_2014.csv'##########
###format example: [40.75866,-73.97168,40.759,-73.97251,40.75964,-73.97206,40.7585,-73.96933]###
import csv
import polyline

pointsLatLon = [] #read points from 'trip_save_nyc_taxi_2014.csv'
###format example: @87aefheHLHAE7EJFhfe7a&^bfai ###
pointsLatLon2 = []#decode result from points
###format example: [40.75866,-73.97168,40.759,-73.97251,40.75964,-73.97206,40.7585,-73.96933]###

#----------------Save LatLonTrip-------------

tripFile = open('trip_save_nyc_taxi_2014.csv','r')
reader = csv.reader(tripFile)

ii = 0
for item in reader:
    points = item[4]
    try:
        points = polyline.decode(points)
        pointsLatLon.append(points)
    except:
        print ('cannot be decoded: ', ii)
        ii += 1

count = 0
for trip in pointsLatLon:
    pointsLatLon2.append([])
    for item in trip:
        pointsLatLon2[count].append(item[0])
        pointsLatLon2[count].append(item[1])
    count += 1

with open('trajectoryLatLon_nyc_taxi_2014.csv','w') as f:
    writer=csv.writer(f)
    for trip in pointsLatLon2:
        writer.writerow(trip)

