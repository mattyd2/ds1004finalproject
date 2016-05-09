from haversine import haversine
import pandas as pd
import requests
import time
import json
from shapely.geometry import shape, Point
from geopy.distance import vincenty


# raw = pd.read_csv('/Users/matthewdunn/Dropbox/NYU/Spring2016/BigData/GroupProject/data/mta_bus/mergedbusroutes/reducedStopsRad001WithBus.csv')
# df = raw.drop(['Unnamed: 0', 'id'], axis=1)
# df.head()

# def f(x):
#     return pd.Series(dict(lat=x['lat'].mean(),
#                           long=x['long'].mean(),
#                           transtype="[%s]" % ', '.join(x['type'].unique())))

# df = df.groupby('assigned').apply(f)


# def concatenatorator(x):
#     x = x[1:-1]
#     x = x.split(',')
#     x = [y.strip() for y in x]
#     x.sort()
#     tmp = str()
#     for i in x:
#         if i == "bikeStop":
#             tmp = tmp+'bi'
#         elif i == "busStop":
#             tmp = tmp+'bu'
#         elif i == "trainStop":
#             tmp = tmp+'tr'
#     return tmp

# finaldf = df.copy()
# finaldf['assigned'] = df.index.values
# finaldf['convertTrans'] = finaldf['transtype'].apply(concatenatorator)
# finaldf['mikeStationId'] = finaldf['convertTrans']+finaldf['assigned'].astype(str)
# finaldf.drop(['transtype', 'convertTrans'], axis=1, inplace=True)
# finaldf.to_csv("/Users/matthewdunn/Dropbox/NYU/Spring2016/BigData/GroupProject/data/nodes.csv", index=False)
finaldf = pd.read_csv("/Users/matthewdunn/Dropbox/NYU/Spring2016/BigData/GroupProject/data/nodes.csv")


# def concatenatorator2(x):
#     tmp = str()
#     if x == "bikeStop":
#         tmp = 'bi'
#     elif x == "busStop":
#         tmp = 'bu'
#     elif x == "trainStop":
#         tmp = 'tr'
#     return tmp

# # use the raw loaded data to create a complete list of all
# # mta station ids and mike's assigned ids
# # this is different then the groupby approach above.
# mergetable = raw.drop(['Unnamed: 0', 'lat', 'long'], axis=1)
# mergetable['type2'] = mergetable['type'].apply(concatenatorator2)
# mergetable['type'] = mergetable['type2']
# mergetable['mtaTypeStatId'] = mergetable['type']+mergetable['id'].astype(str)
# mergetable.drop('type2', axis=1, inplace=True)
# mergetable.head()


# # join the groupby of mikes id and the complete list of mta stations
# joined_dfs = mergetable.merge(finaldf, how='inner', on='assigned')
# joined_dfs.to_csv('/Users/matthewdunn/Dropbox/NYU/Spring2016/BigData/GroupProject/data/prepped_edges.csv', index=False)
joined_dfs = pd.read_csv('/Users/matthewdunn/Dropbox/NYU/Spring2016/BigData/GroupProject/data/prepped_edges.csv')

joined_dfs_dropped = joined_dfs.drop(['id', 'type', 'assigned', 'mtaTypeStatId'], axis=1)
joined_dfs_grouped = joined_dfs_dropped.groupby('mikeStationId').mean()
print 'joined_dfs_grouped.head()\n', joined_dfs_grouped.head()


with open('/Users/matthewdunn/Dropbox/NYU/Spring2016/BigData/GroupProject/nyccensustracts.json', 'r') as f:
    js = json.load(f)


def geocoder(lat, lon):
    point = Point(lon, lat)
    for feature in js['features']:
        geometry = feature.get('geometry')
        polygon = shape(geometry)
        if polygon.contains(point):
                properties = feature.get('properties')
                census_tract = properties.get('BoroCT2010')
                return census_tract

censustracts = []
for i, row in joined_dfs_grouped.iterrows():
    censustract = geocoder(row.lat, row['long'])
    censustracts.append(censustract)
censustracts

joined_dfs_grouped['censustract'] = censustracts
joined_dfs_grouped.head()

# take optimized route data and reshape and then append census tract info
allpairsBus = pd.read_csv("./data/allPairDistancesBusTrain.csv")
print 'allpairsBus.head()\n', allpairsBus.head()

allpairsBus_drop = allpairsBus.drop(['assigned', 'Unnamed: 0.1'], 1)
allpairsBus_drop = allpairsBus_drop.drop([0, 1])
cols = list(allpairsBus_drop.columns.values)
cols = cols[1:]
duration_df = pd.melt(allpairsBus_drop, id_vars=['Unnamed: 0'], value_vars=cols)
duration_df.columns = ['mikestartId', 'mikeendId', 'duration']
duration_df = duration_df[duration_df.mikestartId != duration_df.mikeendId]
print 'duration_df.head()\n', duration_df.head()

# merge duration wth the values for mike's station id
merged_duration = duration_df.merge(joined_dfs_grouped, how='left', left_on='mikestartId', right_index=True)
merged_duration.columns = ['mikestartId', 'mikeendId', 'duration','start_lat','start_long','start_censustract']
print 'merged_duration.head()\n', merged_duration.head()

merged_duration_final = merged_duration.merge(joined_dfs_grouped, how='left', left_on='mikeendId', right_index=True)
merged_duration_final.columns = ['mikestartId','mikeendId','duration','start_lat','start_long','start_censustract','end_lat','end_long','end_censustract']
print 'merged_duration_final.head()\n', merged_duration_final.head()

merged_duration_final['arguments'] = zip(merged_duration_final.start_lat,
                                         merged_duration_final.start_long,
                                         merged_duration_final.end_lat,
                                         merged_duration_final.end_long)

print 'merged_duration_final.head()', merged_duration_final.head()


merged_duration_final['distance'] = merged_duration_final['arguments'].apply(lambda x: vincenty((x[0], x[1]), (x[2], x[3])).miles)

print 'merged_duration_final.head()', merged_duration_final.head()

merged_duration_final.to_csv("/Users/matthewdunn/Dropbox/NYU/Spring2016/BigData/GroupProject/data/nodes.csv", index=False)

# distances = []
# for i, row in merged_duration_final.iterrows():
#     distance = manhattandist(row.start_lat, row.start_long, row.end_lat, row.end_long)
#     distances.append(distance)
# print 'len(distances)\n', len(distances)

# merged_duration_final['distance'] = distances
# print merged_duration_final.head()

# merged_duration_final.to_csv('/Users/matthewdunn/Dropbox/NYU/Spring2016/BigData/GroupProject/data/mikeCTsAvgLatLonDist.csv')
