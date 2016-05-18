# ds1004finalproject
Final project for Big Data DS 1004

### Project
The main focus of this project was to build a transit accessibility score for each of the 2000+ Census Tracts within the five boroughs of New York City (NYC) and relate it to Census Tract data on demographics. The transit accessibility score is an aggregated measure reflecting the time needed to travel from a given tract to all other tracts. NYC bus and train data from the NYC Metropolitan Transit Authority (MTA) are used in computing the accessibility score. Our analysis shows that usually but not always people in tracts with lower mean income tend to experience longer travel times than people in tracts with higher mean income, among other results.

- Project Report and Poster are solid overviews of the focus of the project.

### Data
Train Schedule Data 
- http://web.mta.info/developers/data/nyct/subway/google_transit.zip

Bus Schedule Data
- Bronx - http://web.mta.info/developers/data/nyct/bus/google_transit_bronx.zip
- Brooklyn - http://web.mta.info/developers/data/nyct/bus/google_transit_brooklyn.zip
- Manhattan - http://web.mta.info/developers/data/nyct/bus/google_transit_manhattan.zip
- Queens - http://web.mta.info/developers/data/nyct/bus/google_transit_queens.zip
- Staten Island - http://web.mta.info/developers/data/nyct/bus/google_transit_staten_island.zip

Census Data
- https://drive.google.com/open?id=0B0omRFdoVVJ6NWlCS0h2ZUVFS0k

### Data Wrangling Scripts
- step1.ipynb is used to intial data wrangling, taking schedule data and transforming it into useable trip data.
- step2.ipynb is used to create nodes and edges for mapping the trips using the graphh theoretical framework
- step3.ipynb is used to compute optimal routes between all nodes using duration as edge weight

### Data Visualization
- d3resources contains the necessary scripts for running a d3 visualization of the prepared data.

### Map Reduce Scripts are used for exploratory data analysis.
- We used the map reduce framework to crunch down citibike data for visualization, but ultimately opted not to use the citiBike data as we don't think it is a consistent means of transport for the general population of NYC.
- Additional map reduce scripts were used to crunch down taxi data.
