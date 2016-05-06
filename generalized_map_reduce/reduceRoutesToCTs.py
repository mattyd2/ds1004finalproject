#!/usr/bin/python

import sys
import math
from haversine import haversine

currentKey = None
totaltrips = 0.0
duration = 0.0
start_lat = 0.0
start_lon = 0.0
end_lat = 0.0
end_lon = 0.0

# add max and min values to confirm quality

for line in sys.stdin:
    key, tmp = line.strip().split('\t')
    valuesList = tmp.split(',')

    # aggregrate values for given Key
    if key == currentKey:
        start_lat += float(valuesList[0])
        start_lon += float(valuesList[1])
        end_lat += float(valuesList[2])
        end_lon += float(valuesList[3])
        totaltrips += 1.0
        duration += int(float(valuesList[4]))

    else:
        if currentKey is not None:
            start_avg_lat = float(start_lat/totaltrips)
            start_avg_lon = float(start_lon/totaltrips)
            end_avg_lat = float(end_lat/totaltrips)
            end_avg_lon = float(end_lon/totaltrips)
            avg_duration = int(float(duration/totaltrips))
            start_cen_tract = currentKey.split('_')[0]
            end_cen_tract = currentKey.split('_')[1]
            print "%s,%s,%s,%s,%s,%s,%s" % (start_cen_tract, end_cen_tract,
                                            start_avg_lat, start_avg_lon,
                                            end_avg_lat, end_avg_lon,
                                            avg_duration)

        # set the flow control variables equal to values of current entry
        currentKey = key
        start_lat = float(valuesList[0])
        start_lon = float(valuesList[1])
        end_lat = float(valuesList[2])
        end_lon = float(valuesList[3])
        totaltrips = 1.0
        duration = int(float(valuesList[4]))

avg_duration = int(float(duration/totaltrips))
start_avg_lat = float(start_lat/totaltrips)
start_avg_lon = float(start_lon/totaltrips)
end_avg_lat = float(end_lat/totaltrips)
end_avg_lon = float(end_lon/totaltrips)
start_cen_tract = currentKey.split('_')[0]
end_cen_tract = currentKey.split('_')[1]
print "%s,%s,%s,%s,%s,%s,%s" % (start_cen_tract, end_cen_tract, start_avg_lat,
                                start_avg_lon, end_avg_lat, end_avg_lon,
                                avg_duration)
