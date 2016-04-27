#!/usr/bin/python

import sys
import math
import shapefile
from haversine import haversine

currentKey = None
distance = None
totaltrips = 0.0
amount = 0.0
duration = 0.0

# add max and min values to confirm quality

for line in sys.stdin:
    key, values = line.strip().split('\t')
    valueList = values.split(',')
    ridertype = valueList[9]
    # print "key", key, "==", 'currentKey', currentKey
    if key == currentKey:
        totaltrips += 1.0
        # print 'totaltrips', totaltrips
        duration += float(valueList[8])
        # print 'duration', duration
        amount += amountcalc(ridertype, duration)
        # print 'amount', amount
        # print "amount += amountcalc(ridertype, duration)", amount
    else:
        if currentKey is not None:
            start_lat = float(valueList[2])
            start_lon = float(valueList[3])
            end_lat = float(valueList[6])
            end_lon = float(valueList[7])
            distance = "{0:.2f}".format(manhattandist(start_lat, start_lon,
                                                      end_lat, end_lon))
            avg_amount = "{0:.2f}".format(amount/totaltrips)
            avg_duration = "{0:.2f}".format((duration/60)/totaltrips)
            currentKey = 'bike'+currentKey
            print "%s\t%s,%s,%s,%s,%s" % (currentKey, ",".join(valueList[0:7]),
                                          avg_duration, distance, avg_amount,
                                          totaltrips)
        currentKey = key
        totaltrips = 1.0
        duration = float(valueList[8])
        amount = amountcalc(ridertype, duration)
        distance = None

start_lat = float(valueList[2])
start_lon = float(valueList[3])
end_lat = float(valueList[6])
end_lon = float(valueList[7])
distance = "{0:.2f}".format(manhattandist(start_lat, start_lon, end_lat,
                                          end_lon))
currentKey = 'bike'+currentKey
print "%s\t%s,%s,%s,%s,%s" % (currentKey, ",".join(valueList[0:7]), avg_duration,
                              distance, avg_amount, totaltrips)
