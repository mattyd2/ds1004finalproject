#!/usr/bin/python

import sys
import math
from haversine import haversine

currentKey = None
distance = None
totaltrips = 0.0
lat = 0.0
lon = 0.0

# add max and min values to confirm quality

for line in sys.stdin:
    key, tmp = line.strip().split('\t')
    valuesList = tmp.split(',')
    # lat = float(valuesList[0])
    # lon = float(valuesList[1])
    
    # aggregrate values for given Key
    if key == currentKey:
        lat = float(valuesList[0])
        lon = float(valuesList[1])
        totaltrips += 1.0
        duration += int(float(tmp))

    else:
        if currentKey is not None:
            avg_lat = float(lat/totaltrips)
            avg_lon = float(lon/totaltrips)
            mikesId = valuesList[2]
            print "%s,%s,%s" % (start_station, end_station, avg_duration)

        # set the flow control variables equal to values of current entry
        currentKey = key
        totaltrips = 1.0
        duration = int(float(tmp))

avg_duration = int(duration/totaltrips)
start_station = currentKey.split('_')[0]
end_station = currentKey.split('_')[1]
print "%s,%s,%s" % (start_station, end_station, avg_duration)
