#!/usr/bin/python

import sys
from datetime import datetime
import json
import shapely
from shapely.geometry import shape, Point
import urllib
from geoindex import GeoGridIndex, GeoPoint

# read NYC shape file
myurl = "https://s3.amazonaws.com/kve216-ds-1004-sp16/nyct2010.json"
opener = urllib.URLopener()
myfile = opener.open(myurl)
js = json.load(myfile)

# build index of tract representative points
index = GeoGridIndex()
for feature in js['features']:
    # get feature properties and unique tract identifier
    properties = feature.get('properties')
    BoroCT2010 = properties.get('BoroCT2010')
    # geometry of tract
    geometry = feature.get('geometry')    
    polygon = shape(geometry)
    # get a representative point from each tract
    lon, lat = polygon.representative_point().coords[0]
    # add representative point to index
    index.add_point(GeoPoint(lat, lon, ref=BoroCT2010))


# function returning the Census tract of a point
def geocoder(lat, lon, rad=.5):
    taxi_point = GeoPoint(lat, lon)
    # iterate throug the nearest tracts to the point 
    for point, distance in index.get_nearest_points(taxi_point, rad, unit='km'):
        for feature in js['features']:
            properties = feature.get('properties')
            BoroCT2010 = properties.get('BoroCT2010')
            # check if the point belongs to one of the nearest tracts to it
            if point.ref == BoroCT2010:
                geometry = feature.get('geometry')
                polygon = shape(geometry)
                if polygon.contains(Point(lon, lat)):
                    return BoroCT2010
    # if no tract is found, return an invalid string
    return "notfound"
    #return geocoder(lat,lon,10)

# read in the taxi data
for line in sys.stdin:
    l = line.strip().split(',')
    #if l[0] != 'vendor_id':
    if l[0] != 'VendorID' and len(l) == 19:

        # get duration
        start_datetime = datetime.strptime(l[1], "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.strptime(l[2], "%Y-%m-%d %H:%M:%S")
        duration = end_datetime-start_datetime
        duration_mins = (duration.seconds//60)%60
        
        # get start and end censustracts
        start_census_tract = geocoder(float(l[6]), float(l[5]))
        end_census_tract = geocoder(float(l[10]), float(l[9]))

        # create key from start and end censustracts
        key = start_census_tract+"_"+end_census_tract

        # collect cost and distance data
        cost = l[17]
        distance = l[4]

        # if the tracts found are valid, output key and values
        if len(start_census_tract) == 7 and len(end_census_tract) == 7:
            value = str(duration_mins)+','+cost+','+distance
            print "%s\t%s" % ("this worked", value)
