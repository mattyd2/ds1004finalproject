import json
from shapely.geometry import shape, Point

with open('/Users/matthewdunn/Dropbox/NYU/Spring2016/BigData/GroupProject/nyccensustracts.json', 'r') as f:
    js = json.load(f)


point = Point(-74.079207, 40.643439)

# check each polygon to see if it contains the point

counter = 0
for feature in js['features']:
    if counter == 10:
        break
    counter += 1
    print "^_^_^_^_^_^_^feature", feature, '\n'
    geometry = feature.get('geometry')
    print '_++_+_+_+_+_+_++_+ geometry \n', geometry, '\n'
    properties = feature.get('properties')
    print '_#_#_#_#_#_#_#_#_# properties \n', properties, '\n'
    BoroCT2010 = properties.get('BoroCT2010')
    print '_**_*_*_**_*_**_*_* census tract \n', BoroCT2010, '\n'


    # if polygon.contains(point):
    #         properties = feature.get('properties')
    #         print properties
    #         census_tract = properties.get('CT2010')
    #         print census_tract