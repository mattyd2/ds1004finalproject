#!/usr/bin/python

# this mapper loads all the nodes classified by mike and maps them
# to census track ids

import sys
import json
from shapely.geometry import shape, Point

# load GeoJSON file containing sectors
with open('../../nyccensustracts.json', 'r') as f:
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
    if 'start_lat' not in l[0]:

        start_lat = float(l[0])
        start_lon = float(l[1])
        start_census_tract = geocoder(start_lat, start_lon)

        end_lat = float(l[2])
        end_lon = float(l[3])
        end_census_tract = geocoder(end_lat, end_lon)

        key = start_census_tract+"_"+end_census_tract
        duration = l[4]
        # if the census tracks are the same then we don't consider
        if end_census_tract != start_census_tract:
            print "%s\t%s,%s,%s,%s,%s" % (key, start_lat, start_lon, end_lat,
                                          end_lon, duration)
