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


for line in sys.stdin:
    l = line.strip().split(',')

    # Citi Bike Mapper
    if len(l) == 11:
        if 'duration' not in l[10]:

            start_station_id = str(int(float(l[3])))
            end_station_id = str(int(float(l[2])))
            duration = str(int(float(l[10])*60))
            key = 'bus'+str(start_station_id)+str(end_station_id)
            #               0                   1               2
            value = start_station_id+','+end_station_id+','+duration
            print "%s\t%s" % (key, value)
