#!/usr/bin/python

import sys
import math
from haversine import haversine


def haversine_dist(start_lat, start_lon, end_lat, end_lon):
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
            avg_distance = haversine_dist(start_avg_lat, start_avg_lon,
                                          end_avg_lat, end_avg_lon)
            avg_duration = int(float(duration/totaltrips))
            start_cen_tract = currentKey.split('_')[0]
            end_cen_tract = currentKey.split('_')[1]

            # build string to print
            deliminator = ','
            string_values = (start_cen_tract, end_cen_tract,
                             str(start_avg_lat), str(start_avg_lon),
                             str(end_avg_lat), str(end_avg_lon),
                             str(avg_duration), str(avg_distance))

            strings = deliminator.join(string_values)
            print "%s" % (strings)

        # set the flow control variables equal to values of current entry
        currentKey = key
        start_lat = float(valuesList[0])
        start_lon = float(valuesList[1])
        end_lat = float(valuesList[2])
        end_lon = float(valuesList[3])
        totaltrips = 1.0
        duration = int(float(valuesList[4]))

# calculate values for final key
avg_duration = int(float(duration/totaltrips))
start_avg_lat = float(start_lat/totaltrips)
start_avg_lon = float(start_lon/totaltrips)
end_avg_lat = float(end_lat/totaltrips)
end_avg_lon = float(end_lon/totaltrips)
avg_distance = haversine_dist(start_avg_lat, start_avg_lon,
                              end_avg_lat, end_avg_lon)
start_cen_tract = currentKey.split('_')[0]
end_cen_tract = currentKey.split('_')[1]

# build string to print
deliminator = ','
string_values = (start_cen_tract, end_cen_tract,
                 str(start_avg_lat), str(start_avg_lon),
                 str(end_avg_lat), str(end_avg_lon),
                 str(avg_duration), str(avg_distance))

strings = deliminator.join(string_values)
print "%s" % (strings)
