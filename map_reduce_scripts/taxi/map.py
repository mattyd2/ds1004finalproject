#!/usr/bin/python

# http://docs.aws.amazon.com/ElasticMapReduce/latest/DeveloperGuide/emr-plan-input-distributed-cache.html

import sys
from datetime import datetime
import json
import shapely
from shapely.geometry import shape, Point
from geoindex import GeoGridIndex, GeoPoint

# load GeoJSON file containing sectors
with open('/Users/matthewdunn/Dropbox/NYU/Spring2016/BigData/GroupProject/nyccensustracts.json', 'r') as f:
    js = json.load(f)


index = GeoGridIndex()
for feature in js['features']:
    # print 'feature+_+_+_++_+\n', feature
    properties = feature.get('properties')
    # print 'properties+_+_+_+_+_\n', properties
    BoroCT2010 = properties.get('BoroCT2010')
    # print 'BoroCT2010+_+_++__+_\n', BoroCT2010
    geometry = feature.get('geometry')
    # print 'geometry+_+_+_+_+_+\n', geometry
    polygon = shape(geometry)
    lon, lat = polygon.representative_point().coords[0]
    index.add_point(GeoPoint(lat, lon, ref=BoroCT2010))


def geocoder(lat, lon, rad=.5):
    taxi_point = GeoPoint(lat, lon)
    for point, distance in index.get_nearest_points(taxi_point, rad, unit='km'):
        for feature in js['features']:
            properties = feature.get('properties')
            BoroCT2010 = properties.get('BoroCT2010')
            if point.ref == BoroCT2010:
                geometry = feature.get('geometry')
                polygon = shape(geometry)
                if polygon.contains(Point(lon, lat)):
                    return BoroCT2010
    return str(taxi_point)

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
        if start_census_tract is None:
            startcounter += 1
        if end_census_tract is None:
            endcounter += 1
        print start_census_tract, end_census_tract

        #           0           1        2        3          4            5        6         7        8            9                    10                   11
        value = l[5]+l[6]+','+l[1]+','+l[6]+','+l[5]+','+l[9]+l[10]+','+l[2]+','+l[10]+','+l[9]+','+l[17]+','+str(duration)+','+start_census_tract+','+end_census_tract
        print "%s\t%s" % (key, value)
