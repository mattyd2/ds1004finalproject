#!/usr/bin/python

import sys
from datetime import datetime
import json
import shapely
from shapely.geometry import shape, Point
import urllib

# read NYC shape file
myurl = "https://s3.amazonaws.com/kve216-ds-1004-sp16/nyct2010.json"
opener = urllib.URLopener()
myfile = opener.open(myurl)
js = json.load(myfile)


# function returning census tract of a lat, lon
def geocoder(lat, lon):
    point = Point(lon, lat)

    # check each polygon to see if it contains the point
    for feature in js['features']:
        geometry = feature.get('geometry')
        polygon = shape(geometry)
        if polygon.contains(point):
            properties = feature.get('properties')
            census_tract = properties.get('BoroCT2010')
            return census_tract
    # if no census tract is found, return an invalid string
    return "notfound"

for line in sys.stdin:
    l = line.strip().split(',')
    # pass the header
    if l[0] != 'VendorID' and len(l) == 19:
        # get duration
        start_datetime = datetime.strptime(l[1], "%Y-%m-%d %H:%M:%S")
        end_datetime = datetime.strptime(l[2], "%Y-%m-%d %H:%M:%S")
        duration = end_datetime-start_datetime
        duration_mins = (duration.seconds//60)%60

        # get start and end censustracts
        start_census_tract = geocoder(float(l[6]), float(l[5]))
        end_census_tract = geocoder(float(l[10]), float(l[9]))
        # collect cost and distance data
        cost = l[17]
        distance = l[4]

        # if the tracts found are valid, output key and values
        if len(start_census_tract) == 7 and len(end_census_tract) == 7:
            value = str(duration_mins)+','+cost+','+distance
            print "%s\t%s" % (key, value)
                # if len(start_census_tract) == 7 and len(end_census_tract) == 7:
                #     value = str(duration_mins)+','+cost+','+distance
                #     print "%s\t%s" % (key, value)
