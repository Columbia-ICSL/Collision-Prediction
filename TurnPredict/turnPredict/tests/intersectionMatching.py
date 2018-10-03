import showMap
import numpy as np
import csv
import pandas as pd


intersectionFile = open('intersectionFinal.csv','r')
reader = csv.reader(intersectionFile)
newlist = []
intersection = []
intersectionStreet = []
intersectionAve = []
streetLin = []
aveLin = []
for item in reader:
    newlist.append(showMap.str2float(item[0]))
    newlist.append(showMap.str2float(item[1]))
intersectionFile.close()
count = 0
count2 = 0
for streetNum in range(46) :
    intersection.append([])
    for aveNum in range(13):
        intersection[count].append([newlist[count2],newlist[count2+1]])
        count2 += 2
    count += 1
intersection = np.array(intersection)
print np.shape(intersection)


for i in range(46):
    M = showMap.latLonToPixelArray(intersection[i])
    intersectionStreet.append(M)
for i in range(13):
    M = showMap.latLonToPixelArray(intersection[:,i])
    intersectionAve.append(M)

intersectionStreet = np.array(intersectionStreet)
intersectionAve = np.array(intersectionAve)
for street in intersectionStreet:
    z = np.polyfit(street[:,0],street[:,1],1)
    streetLin.append(z)
    print z
for ave in intersectionAve:
    z = np.polyfit(ave[:,0],ave[:,1],1)
    aveLin.append(z)
    print z
streetLin = np.array(streetLin)
strk = np.mean(streetLin[:,0])
strkv = np.std(streetLin[:,0])
distanceb = []
count = 0
for item in streetLin:
    if(count==0):
        pre = item[1]
        count = 1
    else:
        now = item[1]
        distanceb.append(now - pre)
        pre = item[1]

distanceb = np.array(distanceb)
strb = np.mean(distanceb)
strbv = np.std(distanceb)
print ("k mean: %f  k var: %f  b mean: %f  b var: %f"%(strk,strkv,strb,strbv))

aveLin = np.array(aveLin)
avek = np.mean(aveLin[:,0])
avekv = np.std(aveLin[:,0])
distance2b = []
count = 0
for item in aveLin:
    if(count==0):
        pre = item[1]
        count = 1
    else:
        now = item[1]
        distance2b.append(now - pre)
        pre = item[1]

distance2b = np.array(distance2b)
aveb = np.mean(distance2b)
avebv = np.std(distance2b)
print ("k mean: %f  k var: %f  b mean: %f  b var: %f"%(avek,avekv,aveb,avebv))


'''
with open('LinearB.csv','w') as f:
    writer=csv.writer(f)
    writer.writerow(streetLin[:,1])
    writer.writerow(aveLin[:,1])
'''