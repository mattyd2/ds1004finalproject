#!/usr/bin/python

import sys
import math
from haversine import haversine


def amountcalc(ridertype, duration):
    # print "duration value", duration
    mins = float(duration)/60.
    # print "minutes calculation", mins
    if ridertype == 'Subscriber':
        if mins < 45:
            return 0.0
        elif mins >= 45 and mins < 75:
            # print "Subscriber AND if mins > 45 and mins < 75:", 2.50
            return 2.50
        elif mins >= 75 and mins < 105:
            # print 'Subscriber AND if mins > 75 and mins < 105:', 11.50
            return 11.50
        elif mins >= 105:
            # print 'Subscriber AND over 105'
            mins = mins-105
            mincharges = mins/30
            # print mincharges*9.
            return mincharges*9.
    elif ridertype == 'Customer':
        if mins < 30:
            return 0.0
        elif mins >= 30 and mins < 60:
            # print "customer AND mins > 30 and mins < 60", 4.
            return 4.
        elif mins >= 60 and mins < 90:
            # print "customer AND mins > 60 and mins < 90:", 13.
            return 13.
        elif mins >= 90:
            # print "customer ADN over 90 min"
            mins = mins-90
            mincharges = math.ceil(mins/30)
            # print "mincharges*12.", mincharges*12.
            return mincharges*12.


def manhattandist(start_lat, start_lon, end_lat, end_lon):
    '''this function is used to calculate the approximate manhattan distance
    between two sets of lat and lon points. it was built referencing 

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
    # print '+_+_+_+_+_+', key
    valueList = values.split(',')
    duration = float(valueList[8])
    ridertype = valueList[9]

    if key == currentKey:
        totaltrips += 1.0
        duration += duration
        amount += amountcalc(ridertype, duration)
        # print "amount += amountcalc(ridertype, duration)", amount
    else:
        # if the currentKey is NOT None then evals to True
        if currentKey is not None:
            if distance is None:
                start_lat = float(valueList[2])
                start_lon = float(valueList[3])
                end_lat = float(valueList[6])
                end_lon = float(valueList[7])
                distance = "{0:.2f}".format(manhattandist(start_lat, start_lon, end_lat,
                                         end_lon))
            avg_amount = "{0:.2f}".format(amount/totaltrips)
            if duration > 0:
                avg_duration = "{0:.2f}".format(duration/totaltrips)
            if totaltrips > 5:
                print "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (currentKey, avg_duration, duration, distance,
                                                      avg_amount, amount, totaltrips)
        currentKey = key
        totaltrips = 1.0
        duration = float(valueList[8])
        amount = amountcalc(ridertype, duration)
        distance = None

start_lat = float(valueList[2])
start_lon = float(valueList[3])
end_lat = float(valueList[6])
end_lon = float(valueList[7])
distance = manhattandist(start_lat, start_lon, end_lat, end_lon)
print "final entry"
print "%s\t%s\t%s\t%s\t%s\t%s\t%s" % (currentKey, avg_duration, duration, distance,
                                      avg_amount, amount, totaltrips)
