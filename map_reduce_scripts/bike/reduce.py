#!/usr/bin/python

import sys
import math


def amountcalc(ridertype, duration):
    # print "duration value", duration
    mins = float(duration)/60.
    # print "minutes calculation", mins
    if ridertype == 'Subscriber':
        if mins <= 45:
            return 0.0
        elif mins > 45 and mins < 75:
            # print "Subscriber AND if mins > 45 and mins < 75:", 2.50
            return 2.50
        elif mins > 75 and mins < 105:
            # print 'Subscriber AND if mins > 75 and mins < 105:', 11.50
            return 11.50
        elif mins >= 105:
            # print 'Subscriber AND over 105'
            mins = mins-105
            mincharges = mins/30
            # print mincharges*9.
            return mincharges*9.
    if ridertype == 'Customer':
        if mins <= 30:
            return 0.0
        elif mins > 30 and mins < 60:
            # print "customer AND mins > 30 and mins < 60", 4.
            return 4.
        elif mins > 60 and mins < 90:
            # print "customer AND mins > 60 and mins < 90:", 13.
            return 13.
        elif mins >= 90:
            # print "customer ADN over 90 min"
            mins = mins-90
            mincharges = math.ceil(mins/30)
            # print "mincharges*12.", mincharges*12.
            return mincharges*12.


def manhattandist():
    pass

currentKey = None
totaltrips = 0
amount = 0

for line in sys.stdin:
    key, values = line.strip().split('\t')
    print '+_+_+_+_+_+', key
    valueList = values.split(',')
    duration = valueList[8]
    ridertype = valueList[9]

    if key == currentKey:
        totaltrips += 1
        amount += amountcalc(ridertype, duration)
        print "amount += amountcalc(ridertype, duration)", amount
    else:
        # if the currentKey is NOT None then evals to True
        if currentKey:
            avg_amount = amount/totaltrips
            print "%s\t%s,%s" %(currentKey, totaltrips, amount) 
        currentKey = key
        totaltrips = 1
        amount = amountcalc(ridertype, duration)

avg_amount = amount/totaltrips
print "%s\t%s,%s" %(currentKey, totaltrips, amount) 
