#!/usr/bin/python

import sys
import math
from haversine import haversine

currentKey = None
distance = None
totaltrips = 0.0
amount = 0.0
duration = 0.0

# add max and min values to confirm quality

for line in sys.stdin:
    key, tmp = line.strip().split('\t')

    # aggregrate values for given Key
    if key == currentKey:
        totaltrips += 1.0
        duration += int(float(tmp))

    else:
        if currentKey is not None:
            avg_duration = int(duration/totaltrips)
            start_station = currentKey.split('_')[0]
            end_station = currentKey.split('_')[1]
            print "%s,%s,%s" % (start_station, end_station, avg_duration)

        # set the flow control variables equal to values of current entry
        currentKey = key
        totaltrips = 1.0
        duration = int(float(tmp))

avg_duration = int(duration/totaltrips)
start_station = currentKey.split('_')[0]
end_station = currentKey.split('_')[1]
print "%s,%s,%s" % (start_station, end_station, avg_duration)
