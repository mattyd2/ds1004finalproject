#!/usr/bin/python

import sys
import math

currentKey = None
totaltrips = 0
days = []


def amountcalc(ridertype, duration):
    mins = duration/60
    if ridertype == 'Subscriber':
        if mins > 45 and mins < 75:
            return 2.50
        if mins > 75 and mins < 105:
            return 2.50
        else:
            mins = mins-105
            mincharges = mins/30
            return mincharges*9
    if ridertype == 'Customer':
        if mins > 30 and mins < 60:
            return 4
        if mins > 60 and mins < 90:
            return 9
        else:
            mins = mins-90
            mincharges = math.ceil(mins/30)
            return mincharges*12

for line in sys.stdin:
    key, values = line.strip().split(',')
    if key == currentKey:
        totaltrips += 1
        days = list(set(days + [value]))

    else:
        if currentKey:
            numDays = len(set(days))
            aveTrips = "{0:.2f}".format(totaltrips/float(numDays))
            print "%s\t%s,%s" %(currentKey, totaltrips, aveTrips)       
        currentKey =  key
        totaltrips = 1
        days = [value]
                

aveTrips = "{0:.2f}".format(totaltrips/float(numDays))
print "%s\t%s,%s" %(currentKey, totaltrips, aveTrips)       


print "%s\t%s,%s" % (currentKey, value, value2)
