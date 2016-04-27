#!/usr/bin/python

# http://docs.aws.amazon.com/ElasticMapReduce/latest/DeveloperGuide/emr-plan-input-distributed-cache.html
# mappings -- https://docs.google.com/spreadsheets/d/1kBPt5aOic7KlyvVIHv7dhrKH7DFZJRNzEC4DvfWr04A/edit?usp=sharing

import sys
from datetime import datetime
import json
from shapely.geometry import shape, Point
import math

# load GeoJSON file containing sectors
with open('../../nyccensustracts.json', 'r') as f:
    js = json.load(f)


def amountcalc(ridertype, duration):
    # print "duration value", duration
    mins = duration/60.
    # print "minutes calculation", mins
    if ridertype == 'Subscriber':
        if mins < 45:
            return 0.0
        elif mins >= 45 and mins < 75:
            # print "Subscriber AND if mins > 45 and mins < 75:", 2.50
            return 2.50
        elif mins >= 75 and mins < 105:
            # print 'Subscriber AND if mins > 75 and mins < 105:', 11.50
            return 11.50
        elif mins >= 105:
            # print 'Subscriber AND over 105'
            mins = mins-105
            mincharges = mins/30
            # print mincharges*9.
            return mincharges*9.
    elif ridertype == 'Customer':
        if mins < 30:
            return 0.0
        elif mins >= 30 and mins < 60:
            # print "customer AND mins > 30 and mins < 60", 4.
            return 4.
        elif mins >= 60 and mins < 90:
            # print "customer AND mins > 60 and mins < 90:", 13.
            return 13.
        elif mins >= 90:
            # print "customer ADN over 90 min"
            mins = mins-90
            mincharges = math.ceil(mins/30)
            # print "mincharges*12.", mincharges*12.
            return mincharges*12.


for line in sys.stdin:
    l = line.strip().split(',')

    # Citi Bike Mapper
    if len(l) == 15:
        if 'tripduration' not in l[0]:

            # calculate amount
            total_amount = amountcalc(l[12], float(l[0]))
            start_station_id = l[3]
            end_station_id = l[7]
            duration = l[0]
            key = 'bike'+str(start_station_id)+str(end_station_id)
            #               0                   1               2
            value = start_station_id+','+end_station_id+','+duration
            print "%s\t%s" % (key, value)
