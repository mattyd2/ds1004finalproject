#!/usr/bin/python

import sys

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
                census_tract = properties.get('CT2010')
                return census_tract

for line in sys.stdin:
    l = line.strip().split(',')
    if l[0] != 'tripduration':

        start_census_tract = geocoder(float(l[6]), float(l[5]))
        end_census_tract = geocoder(float(l[10]), float(l[9]))
        key = 'bike'+str(start_census_tract)+str(end_census_tract)

        #         0        1        2        3        4        5        6        7         8        9
        value = l[3]+','+l[1]+','+l[5]+','+l[6]+','+l[7]+','+l[2]+','+l[9]+','+l[10]+','+l[0]+','+l[12]
        print "%s\t%s" % (key, value)
