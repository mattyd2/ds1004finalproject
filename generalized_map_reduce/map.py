#!/usr/bin/python

# http://docs.aws.amazon.com/ElasticMapReduce/latest/DeveloperGuide/emr-plan-input-distributed-cache.html
# mappings -- https://docs.google.com/spreadsheets/d/1kBPt5aOic7KlyvVIHv7dhrKH7DFZJRNzEC4DvfWr04A/edit?usp=sharing

import sys
from datetime import datetime
import json
from shapely.geometry import shape, Point
import math

# load GeoJSON file containing sectors
with open('/Users/matthewdunn/Dropbox/NYU/Spring2016/BigData/GroupProject/nyccensustracts.json', 'r') as f:
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


def geocoder(lat, lon):
    point = Point(lon, lat)

    # check each polygon to see if it contains the point
    for feature in js['features']:
        geometry = feature.get('geometry')
        polygon = shape(geometry)
        if polygon.contains(point):
                properties = feature.get('properties')
                BoroCT2010 = properties.get('BoroCT2010')
                return BoroCT2010

for line in sys.stdin:
    l = line.strip().split(',')

    # Citi Bike Mapper
    if len(l) == 15:
        if 'tripduration' not in l[0]:

            # calculate amount
            total_amount = amountcalc(l[12], float(l[0]))

            start_census_tract = geocoder(float(l[5]), float(l[6]))
            end_census_tract = geocoder(float(l[9]), float(l[10]))
            key = 'bike'+str(start_census_tract)+str(end_census_tract)
            #         0        1        2        3        4        5        6        7               8               9                10                         11
            value = l[3]+','+l[1]+','+l[5]+','+l[6]+','+l[7]+','+l[2]+','+l[9]+','+l[10]+','+str(total_amount)+','+l[0]+','+str(start_census_tract)+','+str(end_census_tract)
            print "%s\t%s" % (key, value)

    # Taxi Mapper
    elif len(l) == 18:
        if l[0] != 'vendor_id':

            # calc duration
            start_datetime = datetime.strptime(l[1], "%m/%d/%y %H:%M")
            end_datetime = datetime.strptime(l[2], "%m/%d/%y %H:%M")
            duration = end_datetime-start_datetime
            duration = int(duration.total_seconds())

            start_census_tract = geocoder(float(l[6]), float(l[5]))
            end_census_tract = geocoder(float(l[10]), float(l[9]))
            key = 'taxi'+str(start_census_tract)+str(end_census_tract)
            #           0           1        2        3          4            5        6         7        8            9                      10                         11
            value = l[5]+l[6]+','+l[1]+','+l[6]+','+l[5]+','+l[9]+l[10]+','+l[2]+','+l[10]+','+l[9]+','+l[17]+','+str(duration)+','+str(start_census_tract)+','+str(end_census_tract)+','+l[4]
            print "%s\t%s" % (key, value)

    # Bus Mapper
    elif len(l) == 11:
        if l[0] != 'Unnamed: 0':
            day_string = l[1]
            if 'Weekday' in day_string:
                date = '4/4/16'
            elif 'Sunday' in day_string or 'Saturday' in day_string:
                date = '4/3/16'

            start_census_tract = geocoder(float(l[6]), float(l[5]))
            end_census_tract = geocoder(float(l[10]), float(l[9]))
            key = 'bus'+str(start_census_tract)+str(end_census_tract)
            #           0           1        2        3          4            5        6         7        8            9                      10                         11
            value = l[5]+l[6]+','+l[1]+','+l[6]+','+l[5]+','+l[9]+l[10]+','+l[2]+','+l[10]+','+l[9]+','+l[17]+','+str(duration)+','+str(start_census_tract)+','+str(end_census_tract)+','+l[4]
            print "%s\t%s" % (key, value)
