#!/usr/bin/python

http://docs.aws.amazon.com/ElasticMapReduce/latest/DeveloperGuide/emr-plan-input-distributed-cache.html

import sys
from datetime import datetime
import json
from shapely.geometry import shape, Point

# load GeoJSON file containing sectors
with open('/Users/matthewdunn/Dropbox/NYU/Spring2016/BigData/GroupProject/nyccensustracts.json', 'r') as f:
    js = json.load(f)


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
    if l[0] != 'vendor_id':
        key = ','.join(l[0:3] + [l[5]])

        # get duration
        start_datetime = datetime.strptime(l[1], "%m/%d/%y %H:%M")
        end_datetime = datetime.strptime(l[2], "%m/%d/%y %H:%M")
        duration = end_datetime-start_datetime

        start_census_tract = geocoder(float(l[6]), float(l[5]))
        end_census_tract = geocoder(float(l[10]), float(l[9]))

        #           0           1        2        3          4            5        6         7        8            9                    10                   11
        value = l[5]+l[6]+','+l[1]+','+l[6]+','+l[5]+','+l[9]+l[10]+','+l[2]+','+l[10]+','+l[9]+','+l[17]+','+str(duration)+','+start_census_tract+','+end_census_tract
        print "%s\t%s" % (key, value)
