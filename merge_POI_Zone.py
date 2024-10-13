import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# >>>>> Read data
path = 'D:/PythonProjects/practicumProject/'

# read the taxi zone  data into a geopandas data frame
zone = gpd.read_file(path +'NYC Taxi Zones.geojson')
# rename the zone_id column
zone.rename(columns={'location_id':'zone_id'}, inplace=True)
# delete the duplicate column
zone.drop('objectid', axis=1, inplace=True)

# read the POI data into a pandas data frame
poi = pd.read_excel(path+'poi_table.xlsx')
# <<<<< Read data


# >>>>> assign the taxi zone id to the poi
poi['zone_id'] = 'NA'

for k in range(len(poi['poi_name'])):
    print([k, '&&&&&', len(poi['poi_name'])])
    # create a Point object
    point = Point(poi['lon'][k], poi['lat'][k])
    # judge whether the point is in a zone
    result = zone.contains(point)
    # take out the id of the zone containing the point
    if len(result[result])>0:
        index = result[result].index[0]
        poi.at[k, 'zone_id'] = zone.at[index, 'zone_id']
    else:
        print('No zone')

# delete all the pois that have no zone assigned
poi = poi[poi['zone_id'] != 'NA']
# merge the POI table with the zone table
poi_zone = pd.merge(poi, zone, on='zone_id', how='inner')

poi_zone.to_excel(path+'poi_zone.xlsx', index=False)
# <<<<< assign the taxi zone id to the poi


