import pandas as pd

df = pd.read_csv('/Users/matthewdunn/Dropbox/NYU/Spring2016/BigData/GroupProject/data/mta_bus/mergedbusroutes/reducedStopsRad001WithBus.csv')
df.drop(['Unnamed: 0', 'id'], axis=1, inplace=True)


# Define groupby function to take mean of lat and long, and concat trans type
def f(x):
    return pd.Series(dict(lat=x['lat'].mean(),
                          long=x['long'].mean(),
                          transtype="[%s]" % ', '.join(x['type'].unique())))

# Apply the groupby function
df = df.groupby('assigned').apply(f)
finaldf = df.copy()
finaldf['assigned'] = df.index.values
finaldf['stationID'] = finaldf['transtype']+finaldf['assigned'].astype(str)
finaldf.drop(['transtype', 'assigned'], axis=1, inplace=True)
finaldf.to_csv("/Users/matthewdunn/Dropbox/NYU/Spring2016/BigData/GroupProject/data/mta_bus/nodes.csv", index=False)
