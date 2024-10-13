# get the Zone-TimeWindow-Passenger Data from NYC Taxi Dataset
import pandas as pd
from datetime import datetime, timedelta
import copy
import pickle
import re
import numpy as np

path = 'D:/PythonProjects/practicumProject/'

# read the taxi zone and poi data.
poi_zone = pd.read_excel(path+'poi_zone.xlsx')
# take out all the involed zone id
poi_zone['location_id'] = poi_zone['location_id'].astype(str)
all_location_id = set(poi_zone['location_id'])

# >>>>> read and prepare the taxi data
# read the yearly Yellow taxi data
year = 2019
taxiYearly = pd.read_csv(path+'2019_Yellow_Taxi_Trip_Data.csv', usecols=['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime','passenger_count'], dtype=str)


# take out all the rows with the POI-related zones.
taxiYearly = taxiYearly[taxiYearly['PULocationID'].isin(all_location_id) | taxiYearly['DOLocationID'].isin(all_location_id)]
print(taxiYearly.shape)

# correct all the 'year',and convert the time to time format
taxiYearly['tpep_pickup_datetime']
temp = list(taxiYearly['tpep_pickup_datetime'].copy())
temp = [re.sub(r'\b(\d{2}/\d{2}/)\d{4}\b', r'\g<1>{}'.format(year), k) for k in temp]

temp = ['02/28'+k[5:] if k[0:5]=='02/29' else k for k in temp]
temp = [datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p') for x in temp]
taxiYearly['tpep_pickup_datetime'] = temp

temp = list(taxiYearly['tpep_dropoff_datetime'].copy())
temp = [re.sub(r'\b(\d{2}/\d{2}/)\d{4}\b', r'\g<1>{}'.format(year), k) for k in temp]

temp = ['02/28'+k[5:] if k[0:5]=='02/29' else k for k in temp]
temp = [datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p') for x in temp]
taxiYearly['tpep_dropoff_datetime'] = temp

# change nan to 1
taxiYearly['passenger_count'] = taxiYearly['passenger_count'].fillna('1')
print(set(taxiYearly['passenger_count']))

# conver the passenger count columns form string to integer objects.
taxiYearly['passenger_count'] = taxiYearly['passenger_count'].astype(float)
taxiYearly['passenger_count'] = taxiYearly['passenger_count'].astype(int)


def giveValue(count):
    if count > 4:
        return np.random.randint(1, 5)
    else:
        return count
taxiYearly['passenger_count'] = taxiYearly['passenger_count'].apply(giveValue)
# <<<<< read and prepare the taxi data

# >>>>> 暂存中间结果
# save data object to disk as a pickle file
with open(path + '临时.pickle', 'wb') as file:
    pickle.dump(taxiYearly, file)

# # load data object from a pickle file
# with open(path + '临时.pickle', 'rb') as f:
#     taxiYearly = pickle.load(f)
# # <<<<< 暂存中间结果



# >>>>> retrieve the data for each zone-halfhour
# >>>>> >>>>> generate the window start and window end list
window_width = 30
start = [datetime(year, 1, 1, 0, 0)]
while start[-1] < datetime(year, 12, 31, 23, 30):
    start.append(start[-1] + timedelta(minutes=window_width))

end = [t+timedelta(minutes=window_width) for t in start]
windowNum = len(end)
# <<<<< <<<<< generate the window start and window end list

# >>>>> >>>>> sum the passenger number for a time window
all_location_id = list(all_location_id )

zone_id = []
time_start = []
time_end = []
taxi_pick =[]
taxi_drop =[]

for k in range(0, len(all_location_id)):
    tempZoneId = all_location_id[k] # take out this zone id
    # take out all the rows belongs to the zone
    tempZoneData = taxiYearly[(taxiYearly['PULocationID']==tempZoneId) | (taxiYearly['DOLocationID']==tempZoneId)]

    # take out each window's data for the zone
    for kk in range(windowNum):
        window_start = start[kk]
        window_end = end[kk]
        # take out the pickup data in this window
        tempZoneWindowPick = tempZoneData[(tempZoneData['tpep_pickup_datetime']>window_start)&(tempZoneData['tpep_pickup_datetime']<window_end)]
        # take out the dropoff data in this window
        tempZoneWindowDrop = tempZoneData[(tempZoneData['tpep_dropoff_datetime']>window_start)&(tempZoneData['tpep_dropoff_datetime']<window_end)]
        # store each value for this zone-window
        zone_id.append(tempZoneId)
        time_start.append(window_start)
        time_end.append(window_end)
        taxi_pick.append(tempZoneWindowPick['passenger_count'].sum())
        taxi_drop.append(tempZoneWindowDrop['passenger_count'].sum())

        print([k, len(all_location_id), str(window_start), str(window_end)])
        print([taxi_pick[-1], taxi_drop[-1]])
# <<<<< <<<<< sum the passenger number for a time window
# <<<<< retrieve the data for each zone-halfhour



zone_time_taxi2019 = {'zone_id': zone_id, 'time_start': time_start, 'time_end': time_end, 'taxi_pick':taxi_pick, 'taxi_drop':taxi_drop}

# save data object to disk as a pickle file
with open(path + 'zone_time_taxi2019.pickle', 'wb') as file:
    pickle.dump(zone_time_taxi2019, file)

# load data object from a pickle file
with open(path + 'zone_time_taxi2019.pickle', 'rb') as f:
    data = pickle.load(f)


