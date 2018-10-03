#!/usr/bin/python
#coding:utf-8
#--------------------------------Standard Intersection Trip-----------------------------
#    each trip:
#   [ ...,(street_num_of_intersection_i,ave_num_of_intersection_i),...]
#
#--------------------------------Standard Intersection Trip-----------------------------
import showMap
import csv
from functools import reduce

B = [] # y = kx+b ; the b of each street and avenue; first row : street 14 to 59 ; second row : avenue 1 to 11
intersectionLatLon = [] # GPS location of each intersections in midtown Manhattan; from ave1 street14 to ave 11 street 59
###format: [(40.731314,-73.982587),(..),..]###
trajectoryLatLon_raw = [] # read trajectoryLatLon and exclude trips with less than 3 points
###format: [[40.725374,-73.902687,...]...]###
trajectoryLatLon_raw2 = [] #change format of trajectoryLatLon_raw
###format: [[[40.725374,-73.902687],[...]...]...]###
roadSegmentTrip = [] #convert trajectory to road segments
###format example: [[('S',18),('S',18),('A',7),('A',7),('A',7),('S',14),...],[...]]###
intersectionTrip = [] #all the turning intersections are extracted and start and end point are added at the end
###format example: [[[('S',18),('A',7)] [('A',7),('S',16)]..],[...],('A',5),('S',14)]###
trajectoryCoorninates = []# convert GPS location in trajectoryLatLon_raw2 to coordinates
finalIntersectionTrip = [] # origin intersection + middle intersections + destination intersection
###format example: [[[('A',3),('S',18)][('S',18),('A',7)] [('A',7),('S',16)]..],[...]]###
finalTrip = []

Label_three_classes = []
Label_two_classes = []

#-------------google map parameters-----------------
scale = 14
pixelS = 1
size = 640
point = 0.07
#-------------google map parameters-----------------

#-----linear parameters of streets and avenues-----
strK = -0.556192
aveK = 1.820408
strKV = 0.000972+0.1
aveKV = 0.031355+0.1
strStep = 12.622230
aveStep3 = 63.696216
strSF = 173.75501357
aveSF = -654.78045449
aveB6 = -348.36596704
aveB2 = -527.26116951
#-----linear parameters of streets and avenues-----

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

def getRoadSegment(trajectoryLatLonArray):
    testTra = showMap.latLonToPixelArray(trajectoryLatLonArray)
    # print testTra
    xPre = testTra[0][0]
    yPre = testTra[0][1]
    roadArray = []
    for ii in range(1, len(testTra)):
        xNow = testTra[ii][0]
        yNow = testTra[ii][1]
        k = (yNow - yPre) / (xNow - xPre) * 1.0
        # print k
        # decide whether street or avenue
        if (k > strK - strKV and k < strK + strKV):
            bNow = yNow - strK * xNow
            bPre = yPre - strK * xPre
            b = (bNow + bPre) / 2.0
            # print b
            bNum = int((b - strSF) / strStep)
            if (b - B[bNum] < B[bNum + 1] - b):
                roadArray.append(('S', bNum))
            else:
                roadArray.append(('S', bNum + 1))
        else:
            bNow = yNow - aveK * xNow
            bPre = yPre - aveK * xPre
            b = (bNow + bPre) / 2.0
            # print b
            if(b>-369):
                bNum = int((b-aveB6)/80)
                if ((52 + bNum + 1) <= 58):
                    if (abs(b - B[52 + bNum]) < abs(B[52 + bNum + 1] - b)):
                        roadArray.append(('A', bNum + 6))
                    else:
                        roadArray.append(('A', bNum + 7))
                else:
                    roadArray.append(('A', 12))

            if(b<=-369 and b>=-504):
                bNum = int((b-aveB2)/42)
                if (abs(b - B[48 + bNum]) < abs(B[48 + bNum + 1] - b)):
                    roadArray.append(('A', bNum+2))
                else:
                    roadArray.append(('A', bNum + 3))
            if (b<=-504):
                bNum = int((b-aveSF)/63)
                if (abs(b - B[46 + bNum]) < abs(B[46 + bNum + 1] - b)):
                    roadArray.append(('A', bNum))
                else:
                     roadArray.append(('A', bNum + 1))
        xPre = testTra[ii][0]
        yPre = testTra[ii][1]

    return roadArray

def getLabel(now,before,after):
    # result : up: 0 ; down: 1; left: 2; right: 3;
    # label_three_classes: go straight : 0 ; turn left : 1 ; turn right: 2
    # label_two_classes: go straigth :0 ;turn :1
    flag1 = 0
    flag2 = 0
    flag3 = 0
    if (now[0]<before[0]):
        l = 1
        flag1 =1
    if (now[0]>before[0]):
        l = 0
        flag1 =1
    if(now[1]<before[1]):
        l = 3
        flag1 =1
    if (now[1] > before[1]):
        l = 2
        flag1 =1
    if (after[0]<now[0]):
        L = 1
        flag2 =1
    if (after[0]>now[0]):
        L = 0
        flag2 =1
    if(after[1]<now[1]):
        L = 3
        flag2 =1
    if (after[1] > now[1]):
        L = 2
        flag2 =1
    if(flag1==0 or flag2 ==0):
        l = 0
        L = 0
    label = [l,L]
    if (label[0]==label[1]):
        label_three_classes = 0
        label_two_classes = 0
        flag3 = 1
    if(label == [0,2] or label == [1,3] or label == [2,1] or label == [3,0]):
        label_three_classes = 1
        label_two_classes = 1
        flag3 = 1
    if (label == [0,3] or label == [1,2] or label == [2,0] or label == [3,1]):
        label_three_classes = 2
        label_two_classes = 1
        flag3 = 1
    if(flag3 == 0):
        label_three_classes = 0
        label_two_classes = 0
    return label_three_classes,label_two_classes,flag3

#----------------Load Intersection-------------

intersectionFile = open('intersectionFinal.csv','r')
reader = csv.reader(intersectionFile)
for item in reader:
    intersectionLatLon.append((str2float(item[0]),str2float(item[1])))
intersectionFile.close()

#------------------Load fileB--------------------

linearbFile = open('LinearB.csv','r')
reader = csv.reader(linearbFile)
for item in reader:
    for ii in item:
        B.append(str2float(ii))
linearbFile.close()

#------------------Load trajectoryLatLon--------------------

trajectoryLatLonFile = open('trajectoryLatLon_nyc_taxi_2014.csv','r')
reader = csv.reader(trajectoryLatLonFile)

#######filter trips with less than 3 points########
#######REDUCE NUMBER OF TRIP#########
count = 0
for trip in reader:
    if (len(trip)<=4):
        continue
    else:
        # at least 3 points
        trajectoryLatLon_raw.append([])
        for item in trip:
            trajectoryLatLon_raw[count].append(str2float(item))
        count += 1
# print ('Length of trips with at least 3 points: /trajectoryLatLon_raw ',len(trajectoryLatLon_raw))

####change the format from [lat,lon,lat,lon,...]###
###########to [[lat,lon],[lat,lon],...]###########
count = 0
for trip in trajectoryLatLon_raw:
    trajectoryLatLon_raw2.append([])
    for ii in range(len(trip)/2):
        list = []
        list.append(trip[2*ii])
        list.append(trip[2*ii+1])
        trajectoryLatLon_raw2[count].append(list)
    count +=1

#------------------Convert trajectoryLatLon To road segments-------------------

for ii in range(len(trajectoryLatLon_raw2)):
    roadSegmentTrip.append([])
    trajectoryCoorninates.append([])
    roadSegmentTrip[ii].append(getRoadSegment(trajectoryLatLon_raw2[ii]))
    trajectoryCoorninates[ii].append(showMap.latLonToPixelArray(trajectoryLatLon_raw2[ii]))

#------------------Extract Turning Intersections In A Trip-------------------

count = 0
for trip in roadSegmentTrip:
    intersectionTrip.append([])
    pre = trip[0][0]
    for ii in range(len(trip[0])-1):
        if(pre != trip[0][ii+1]):
            if(ii+2<(len(trip[0])-1)):
                if (pre != trip[0][ii + 2]): # exclude some bad points like ('S',18),('A',7),('S',18)
                    intersectionTrip[count].append([pre,trip[0][ii+1]])
            else:
                intersectionTrip[count].append([pre,trip[0][ii+1]])
        pre = trip[0][ii+1]
    count +=1

#------------------Add Start And End Point Info At The End of intersectionTrip-------------------

#start point
for ii in range(len(trajectoryCoorninates)):
    if(intersectionTrip[ii]):
        if(intersectionTrip[ii][0][0][0]=='A'):
            b = trajectoryCoorninates[ii][0][0][1] - strK * trajectoryCoorninates[ii][0][0][0]
            bNum = int((b - strSF) / strStep)
            if (b - B[bNum] < B[bNum + 1] - b):
                intersectionTrip[ii].append(('S', bNum))
            else:
                intersectionTrip[ii].append(('S', bNum + 1))
        else:
            b = trajectoryCoorninates[ii][0][0][1] - aveK * trajectoryCoorninates[ii][0][0][0]
            if (b > -369):
                bNum = int((b - aveB6) / 80)
                if ((52 + bNum + 1) <= 58):
                    if (abs(b - B[52 + bNum]) < abs(B[52 + bNum + 1] - b)):
                        intersectionTrip[ii].append(('A', bNum + 6))
                    else:
                        intersectionTrip[ii].append(('A', bNum + 7))
                else:
                    intersectionTrip[ii].append(('A', 12))
            if (b <= -369 and b >= -504):
                bNum = int((b - aveB2) / 42)
                if (abs(b - B[48 + bNum]) < abs(B[48 + bNum + 1] - b)):
                    intersectionTrip[ii].append(('A', bNum + 2))
                else:
                    intersectionTrip[ii].append(('A', bNum + 3))
            if (b <= -504):
                bNum = int((b - aveSF) / 63)
                if (abs(b - B[46 + bNum]) < abs(B[46 + bNum + 1] - b)):
                    intersectionTrip[ii].append(('A', bNum))
                else:
                    intersectionTrip[ii].append(('A', bNum + 1))

# end  point
for ii in range(len(trajectoryCoorninates)):
    if(intersectionTrip[ii]):
        if (intersectionTrip[ii][-2][-1][0] == 'A'):
            b = trajectoryCoorninates[ii][0][-1][1] - strK * trajectoryCoorninates[ii][0][-1][0]
            bNum = int((b - strSF) / strStep)
            if (b - B[bNum] < B[bNum + 1] - b):
                intersectionTrip[ii].append(('S', bNum))
            else:
                intersectionTrip[ii].append(('S', bNum + 1))
        else:
            b = trajectoryCoorninates[ii][0][-1][1] - aveK * trajectoryCoorninates[ii][0][-1][0]
            if (b > -369):
                bNum = int((b - aveB6) / 80)
                if ((52 + bNum + 1) <= 58):
                    if (abs(b - B[52 + bNum]) < abs(B[52 + bNum + 1] - b)):
                        intersectionTrip[ii].append(('A', bNum + 6))
                    else:
                        intersectionTrip[ii].append(('A', bNum + 7))
                else:
                    intersectionTrip[ii].append(('A', 12))

            if (b <= -369 and b >= -504):
                bNum = int((b - aveB2) / 42)
                if (abs(b - B[48 + bNum]) < abs(B[48 + bNum + 1] - b)):
                    intersectionTrip[ii].append(('A', bNum + 2))
                else:
                    intersectionTrip[ii].append(('A', bNum + 3))
            if (b <= -504):
                bNum = int((b - aveSF) / 63)
                if (abs(b - B[46 + bNum]) < abs(B[46 + bNum + 1] - b)):
                    intersectionTrip[ii].append(('A', bNum))
                else:
                    intersectionTrip[ii].append(('A', bNum + 1))

#------------------Reorder an Filter the Trip-------------------

#######REDUCE NUMBER OF TRIP#########

count = 0
for trip in intersectionTrip:
    finalIntersectionTrip.append([])
    if (trip):
        #add start point intersection
        if(trip[-2][0]=='S' and trip[-2][1]!=trip[0][0][1] and trip[-2][1]!=trip[0][1][1]):
            # if the start point is not the first turning intersection and the S info is stored in the place
            finalIntersectionTrip[count].append([trip[-2], trip[0][0]])
        if(trip[-2][0]=='A' and trip[-2][1]!=trip[0][0][1] and trip[-2][1]!=trip[0][1][1]):
            finalIntersectionTrip[count].append([ trip[0][0],trip[-2]])
        #add middle turning intersections
        for item in trip[:-2]:
            if(item[0][0]=='S'):
                finalIntersectionTrip[count].append(item)
            else:
                finalIntersectionTrip[count].append([item[1],item[0]])
        #add end point intersection
        if(trip[-1][0]=='S' and trip[-1][1]!=trip[-3][0][1] and  trip[-1][1]!=trip[-3][1][1]):
            # if the end point is not the last turning intersection and the S info is stored in the place
            finalIntersectionTrip[count].append([trip[-1], trip[-3][1]])
        if(trip[-1][0]=='A' and trip[-1][1]!=trip[-3][0][1] and  trip[-1][1]!=trip[-3][1][1]):
            finalIntersectionTrip[count].append([trip[-3][1],trip[-1]])
    count += 1

#------------------Complete the Trip-------------------

ii = 0
for trip in finalIntersectionTrip:
    if(trip):
        ii = 0
        for pp in range(len(trip) - 1):
            if (trip[ii][0][1] != trip[ii + 1][0][1] and abs(trip[ii + 1][0][1] - trip[ii][0][1]) != 1):  # S change
                A = trip[ii][1]
                S = trip[ii][0][1]
                dd = trip[ii + 1][0][1] - trip[ii][0][1]
                if (dd < 0):
                    for jj in range(abs(dd) - 1):
                        trip.insert(ii + 1 + jj, [('S', S - jj - 1), A])
                    ii = ii + (abs(dd) - 1)
                else:
                    for jj in range(dd - 1):
                        trip.insert(ii + 1 + jj, [('S', S + jj + 1), A])
                    ii = ii + (abs(dd) - 1)
            if (trip[ii][1][1] != trip[ii + 1][1][1] and abs(trip[ii + 1][0][1] - trip[ii][0][1]) != 1):  # A change
                S = trip[ii][0]
                A = trip[ii][1][1]
                dd = trip[ii + 1][1][1] - trip[ii][1][1]
                if (dd < 0):
                    for jj in range(abs(dd) - 1):
                        trip.insert(ii + 1 + jj, [S, ('A', A - jj - 1)])
                    ii += abs(dd) - 1
                else:
                    for jj in range(dd - 1):
                        trip.insert(ii + jj + 1, [S, ('A', A + jj + 1)])
                    ii += abs(dd) - 1
            ii += 1

# print ('Length of finalIntersectionTrip: ', len(finalIntersectionTrip))

# ------------------Delete 'S' and 'A' Simplifying the Trip-------------------

simpleTrip = []
count = 0
for trip in finalIntersectionTrip:
    if(trip):
        simpleTrip.append([])
        ii = 0
        for jj in range(len(trip)):
            if (ii + 1 < len(trip) - 1):
                if (trip[ii][0][1] == trip[ii + 1][0][1] and trip[ii][1][1] == trip[ii + 1][1][1]):
                    # exclude bad points that two consecutive points are the same
                    continue
                else:
                    intersection_x_y = []
                    intersection_x_y.append(trip[ii][0][1])
                    intersection_x_y.append(trip[ii][1][1])
                    simpleTrip[count].append(intersection_x_y)
            else:
                intersection_x_y = []
                intersection_x_y.append(trip[ii][0][1])
                intersection_x_y.append(trip[ii][1][1])
                simpleTrip[count].append(intersection_x_y)
            ii += 1
        count += 1

# print ('Length of simpleTrip: ', len(simpleTrip))

# ------------------Filter the Trip-------------------
count = 0
for trip in simpleTrip:
    if (trip!=""):
        finalTrip.append([])
        for item in trip:
            if (item[0] > 0 and item[1] > 0):
                finalTrip[count].append(item)
    count+=1

while [] in finalTrip:
    finalTrip.remove([])

# print ('Length of finalTrip: ', len(finalTrip))

count = 0
finalTrip2 =[]
for trip in finalTrip:
    finalTrip2.append([])
    jj = 0
    if(len(trip)>=3):
        while (jj < len(trip) - 2):
            now = trip[jj + 1]
            before = trip[jj]
            after = trip[jj + 2]
            _, _, flag = getLabel(now=now, before=before, after=after)
            if (flag == 0):
                finalTrip2[count].append(trip[jj])
                jj += 1
            else:
                finalTrip2[count].append(trip[jj])
            jj += 1
        if (jj == len(trip) - 2):
            finalTrip2[count].append(trip[jj])
            finalTrip2[count].append(trip[jj + 1])
        count += 1

while [] in finalTrip2:
    finalTrip2.remove([])

finalTrip3 = []
for trip in finalTrip2:
    if(len(trip)>=3):
        finalTrip3.append(trip)

# print ('Length of finalTrip3: ', len(finalTrip3))

with open('standardIntersectionTrip.csv', 'w') as f:
    writer = csv.writer(f)
    for trip in finalTrip3:
        writer.writerow(trip)

# ------------------Add Label to finalTrip-------------------

count = 0
for trip in finalTrip3:
    Label_two_classes.append([])
    Label_three_classes.append([])
    # oneHotLabel_three_classes.append([])
    # oneHotLabel_two_classes.append([])
    for jj in range(len(trip)-2):
        now = trip[jj+1]
        before = trip[jj]
        after = trip[jj+2]
        label_three_classes,label_two_classes,_ = getLabel(now=now,before=before,after=after)
        Label_two_classes[count].append(label_two_classes)
        Label_three_classes[count].append(label_three_classes)
        # oneHotLabel_three_classes[count].append(enc_3.transform(label_three_classes).toarray())
        # oneHotLabel_two_classes[count].append(enc_2.transform(label_two_classes).toarray())
    count += 1

#delete start and end
for ii in range(len(finalTrip3)):
    finalTrip3[ii] = finalTrip3[ii][1:-1]
