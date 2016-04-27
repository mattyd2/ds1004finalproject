#!/usr/bin/python

import sys
import math
from haversine import haversine


def manhattandist(start_lat, start_lon, end_lat, end_lon):
    '''this function is used to calculate the approximate manhattan distance
    between two sets of lat and lon points. it was built referencing

    http://stackoverflow.com/questions/15736995/how-can-i-quickly-estimate-the-distance-between-two-latitude-longitude-points
    http://stackoverflow.com/questions/32923363/manhattan-distance-for-two-geolocations
    http://www.movable-type.co.uk/scripts/latlong.html

    input: two sets of lat and long points

    returns: approximate manhattan distnace'''

    start_station_location = (start_lat, start_lon)
    end_station_location = (end_lat, end_lon)
    return haversine(start_station_location, end_station_location, miles=True)

currentKey = None
distance = None
totaltrips = 0.0
amount = 0.0
duration = 0.0

# add max and min values to confirm quality

for line in sys.stdin:
    key, values = line.strip().split('\t')
    valueList = values.split(',')
    # print ",".join(valueList[10:12])
    # print key
    # for idx, i in enumerate(valueList):
    #     print idx, i
    # print key float(valueList[8])

    # aggregrate values for given Key
    if key == currentKey:
        totaltrips += 1.0
        # print 'BEFORE amount += float(valueList[8])', amount
        amount += float(valueList[8])
        # print 'AFTER amount += float(valueList[8])', amount
        # print 'BEFORE duration += float(valueList[9])', duration
        duration += float(valueList[9])
        # print 'AFTER duration += float(valueList[9])', duration
        if currentKey[0:4] != 'bike':
            distance += float(valueList[12])

    else:
        # check if currentKey is set
        if currentKey is not None:
            if currentKey[0:4] == 'bike':
                start_lat = float(valueList[2])
                start_lon = float(valueList[3])
                end_lat = float(valueList[6])
                end_lon = float(valueList[7])
                avg_distance = "{0:.2f}".format(manhattandist(start_lat,
                                                              start_lon,
                                                              end_lat,
                                                              end_lon))
            else:
                avg_distance = distance/totaltrips
            avg_amount = "{0:.2f}".format(amount/totaltrips)
            avg_duration = "{0:.2f}".format(duration/totaltrips)
            print "%s,%s,%s,%s,%s,%s,%s,%s" % (currentKey,
                                               ",".join(valueList[2:4]),
                                               ",".join(valueList[6:8]),
                                               avg_amount,
                                               avg_duration,
                                               ",".join(valueList[10:12]),
                                               avg_distance,
                                               totaltrips)

        # set the flow control variables equal to values of current entry
        currentKey = key
        totaltrips = 1.0
        duration = float(valueList[9])
        amount = float(valueList[8])
        if currentKey[0:4] != 'bike':
            distance = float(valueList[12])

if currentKey[0:4] == 'bike':
    start_lat = float(valueList[2])
    start_lon = float(valueList[3])
    end_lat = float(valueList[6])
    end_lon = float(valueList[7])
    avg_distance = "{0:.2f}".format(manhattandist(start_lat,
                                                  start_lon,
                                                  end_lat, end_lon))
else:
    avg_distance = distance/totaltrips
print "%s,%s,%s,%s,%s,%s,%s,%s" % (currentKey,
                                   ",".join(valueList[2:4]),
                                   ",".join(valueList[6:8]),
                                   avg_amount,
                                   avg_duration,
                                   ",".join(valueList[10:12]),
                                   avg_distance,
                                   totaltrips)
