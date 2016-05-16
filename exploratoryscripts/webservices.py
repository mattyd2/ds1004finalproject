import requests

payload = {'latitude': 40.682752, 'longitude': -73.945804, 'showall': 'false'}
# https://www.census.gov/geo/maps-data/data/baf_description.html
# BLOCKID:  15-character code that is the concatenation of fields consisting
# of the 2-character state FIPS code, the 3-character county FIPS code,
# the 6-character cen`, and the 4-character tabulation block code.
r = requests.get('http://data.fcc.gov/api/block/find?format=json&', params=payload)
blockid = r.json().get('Block').get('FIPS')
print r.json()
print blockid
print blockid[5:11]