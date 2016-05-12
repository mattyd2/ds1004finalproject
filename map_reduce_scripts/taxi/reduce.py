#!/usr/bin/python

import sys
import math

currentKey = None
distance = None
totaltrips = 0.0
amount = 0.0
duration = 0.0

# add max and min values to confirm quality

for line in sys.stdin:
    key, values = line.strip().split('\t')
    valueList = values.split(',')
    # print "key", key, "==", 'currentKey', currentKey
    if key == currentKey:
        totaltrips += 1.0
        # print 'totaltrips', totaltrips
        duration += float(valueList[0])
        # print 'duration', duration
        amount += float(valueList[1])
        # print 'amount', amount
        distance += float(valueList[2])
    else:
        if currentKey is not None:
            avg_amount = "{0:.2f}".format(amount/totaltrips)
            avg_duration = "{0:.2f}".format(duration/totaltrips)
            avg_distance = "{0:.2f}".format(distance/totaltrips)

            # build string to print
            deliminator = ','
            string_values = (str(avg_amount), str(avg_duration),
                             str(avg_distance), str(totaltrips))

            strings = deliminator.join(string_values)
            print "%s" % (strings)

        # reset values
        currentKey = key
        totaltrips = 1.0
        duration = float(valueList[0])
        amount = float(valueList[1])
        distance = float(valueList[2])

avg_amount = "{0:.2f}".format(amount/totaltrips)
avg_duration = "{0:.2f}".format(duration/totaltrips)
avg_distance = "{0:.2f}".format(distance/totaltrips)

# build string to print
deliminator = ','
string_values = (str(avg_amount), str(avg_duration),
                 str(avg_distance), str(totaltrips))

strings = deliminator.join(string_values)
print "%s" % (strings)
