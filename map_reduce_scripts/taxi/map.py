#!/usr/bin/python

import sys
from datetime import datetime
import json
import shapely
from shapely.geometry import shape, Point
from geoindex import GeoGridIndex, GeoPoint

# load GeoJSON file containing sectors
with open('./nyc.json', 'r') as f:
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

# read in the taxi data
for line in sys.stdin:
    l = line.strip().split(',')
    if l[0] != 'vendor_id':

        # get duration
        start_datetime = datetime.strptime(l[1], "%m/%d/%y %H:%M")
        end_datetime = datetime.strptime(l[2], "%m/%d/%y %H:%M")
        duration = end_datetime-start_datetime
        duration_mins = (duration.seconds//60)%60
        # get start and end censustracts
        start_census_tract = geocoder(float(l[6]), float(l[5]))
        end_census_tract = geocoder(float(l[10]), float(l[9]))

        # create key from start and end censustracts
        key = start_census_tract+"_"+end_census_tract

        cost = l[17]
        distance = l[4]

        if start_census_tract is not None and end_census_tract is not None:
            value = str(duration_mins)+','+cost+','+distance
            print "%s\t%s" % (key, value)
