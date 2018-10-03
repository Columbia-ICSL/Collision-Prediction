#!/usr/bin/python
#coding:utf-8
#lat --- 40
import numpy as np
import matplotlib.pyplot as plt
import json
import csv
from functools import reduce
import polyline
import random
import pandas as pd

#---------google map parameters-------------
scale = 14
pixelS = 1
size = 640
point = 0.07
#---------google map parameters-------------

center_la,center_lo = 40.753522, -73.985100 #the center of Mid-town Manhattan

#----------------[One Point(lat,lon)] Convert Latitude,Longitude to Pixel X Y-------------
def latLonToPixelXY(lat, lon, zoomS):
    mapW = 256 * 2 ** zoomS + 0.0
    mapH = 256 * 2 ** zoomS + 0.0
    x = (lon + 180) * (mapW / 360)  # get x value
    latRad = lat * np.pi / 180  # convert from degrees to radians
    mercN = np.log(np.tan((np.pi / 4) + (latRad / 2)))  # get y value
    y = (mapH / 2) - (mapW * mercN / (2 * np.pi))
    return x, y

#-------[Array:[(lat,lon),(lat,lon),(lat,lon),...]] Convert Latitude,Longitude to displayable Coorninates--------
def latLonToPixelArray(latLonArray,centerLat = center_la,centerLon = center_lo,scale = 14, pixelS = 1, size = 640, point = 0.07):
    M = []
    count = 0
    centX, centY = latLonToPixelXY(centerLat, centerLon, scale)
    for item in latLonArray:
        M.append([])
        lat = item[0]
        lon = item[1]
        x,y = latLonToPixelXY(float(lat), float(lon), scale)
        x,y = size * pixelS /2 + x - centX, size * pixelS/2   - (y - centY) #after this step, the x,y can be displayed correctly
        M[count].append(x)
        M[count].append(y)
        count += 1
    return M

def str2float(s):
    factor = 1.0
    if (s[0]=='-'):
        factor = -1.0
        s = s[1:]
    def str2num(s):
        return {'0': 0, '1': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}[s]
    def fnMuti(x, y):
        return x * 10 + y
    def fnDivid(x, y):
        return x / 10.0 + y
    if (s.find('.')!=-1):
        dotIndex = s.index('.')
        return (reduce(fnMuti, map(str2num, s[:dotIndex])) + reduce(fnDivid, list(map(str2num, s[dotIndex + 1:]))[
                                                                             ::-1]) / 10) * factor
    else:
        return reduce(fnMuti, map(str2num, s)) * factor

def randomcolor():
    colorArr = ['1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F']
    color = ""
    for i in range(6):
        color += colorArr[random.randint(0, 14)]
    return "#" + color

def randomcolor2():
    colortype =['blue','red','black','indigo','darkcyan','firebrick','saddlebrown']
    colortype2 = ['tomato','yellowgreen','orangered','lightcoral','seagreen','lightseagreen','slateblue','palevioletred']
    return colortype2[random.randint(0,len(colortype2)-1)]

#----------------Show Map -------------
def showMap(latLonArray,color):
    fig = plt.figure(figsize=(6, 6))
    M = latLonToPixelArray(latLonArray,centerLat=center_la, centerLon=center_lo)
    im = np.flipud(plt.imread('/Users/liangao/Desktop/summer18/predict_turn/nyc_taxi_trip.png')) #background
    ax = plt.subplot(111)
    ax.imshow(im)
    for item in M:
        ax.scatter(item[0], item[1], s=100 * point, facecolor=color, lw=1, alpha=0.7)
    ax.set_xlim(0,size*pixelS)
    ax.set_ylim(0,size*pixelS)
    plt.axis('on')
    plt.show()

def showTrajectory(latLonArray):
    fig = plt.figure(figsize=(6, 6))
    im = np.flipud(plt.imread('/Users/liangao/Desktop/summer18/predict_turn/nyc_taxi_trip.png')) #background
    ax = plt.subplot(111)
    ax.imshow(im)
    for trip in latLonArray:
        M = latLonToPixelArray(trip,centerLat=center_la, centerLon=center_lo)
        count = 0
        color = randomcolor2()
        for item in M:
            if (count == 0):
                prelat = item[0]
                prelon =item[1]
                count = 1
                ax.scatter(prelat, prelon, color='red', lw=2, alpha=0.7)
                continue
            else:
                ax.plot((prelat,item[0]), (prelon,item[1]), color=color, lw=3, alpha=0.7)
                prelat = item[0]
                prelon = item[1]
        ax.scatter(prelat, prelon, color='blue', lw=2, alpha=0.7)
    ax.set_xlim(0,size*pixelS)
    ax.set_ylim(0,size*pixelS)
    plt.axis('on')
    plt.show()
#------------Test-------------


#------------Generate Pic1-------------
'''
intersectionLatLon = []

intersectionFile = open('intersectionFinal.csv','r')
reader = csv.reader(intersectionFile)
for item in reader:
    intersectionLatLon.append((str2float(item[0]),str2float(item[1])))
intersectionFile.close()

showMap(intersectionLatLon,'yellow')

'''

'''
#------------Generate Pic2-------------
pointsLatLon = []
pointsfloat = []
tripFile = open('trip_save.csv','r')
reader = csv.reader(tripFile)
for item in reader:
    points = item[4]
    points = polyline.decode(points)
    pointsLatLon.append(points)

# showTrajectory(pointsLatLon[10:30])
# showMap(pointsLatLon[20],'blue')

'''

'''
trajectoryLatLonFile = open('trajectoryLatLon.csv','r')
reader = csv.reader(trajectoryLatLonFile)
trajectoryLatLon_raw = []
trajectoryLatLon_raw2 = []
count = 0
for trip in reader:
    if (len(trip)<=4):
        continue
    else:
        trajectoryLatLon_raw.append([])
        for item in trip:
            trajectoryLatLon_raw[count].append(str2float(item))
        count += 1

count = 0
for trip in trajectoryLatLon_raw:
    trajectoryLatLon_raw2.append([])
    for ii in range(len(trip)/2):
        list = []
        list.append(trip[2*ii])
        list.append(trip[2*ii+1])
        trajectoryLatLon_raw2[count].append(list)
    count +=1

print len(trajectoryLatLon_raw2[13])
showMap(trajectoryLatLon_raw2[13],'blue')


'''



