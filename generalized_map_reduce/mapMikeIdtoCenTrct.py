#!/usr/bin/python

# this mapper loads all the nodes classified by mike and maps them
# to census track ids

import sys
from datetime import datetime
import json
from shapely.geometry import shape, Point
import math

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
    if 'lat' not in l[0]:
        lat = float(l[0])
        lon = float(l[1])
        mikeId = l[3]
        census_tract = geocoder(lat, lon)
        print "%s,%s,%s,%s" % (census_tract, str(lat), str(lon), mikeId)
