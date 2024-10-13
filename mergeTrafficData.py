import pandas as pd
import pickle
from datetime import datetime, timedelta


path = 'D:/PythonProjects/practicumProject/'


# >>>>> load the taxi data and merge with poi
# load poi_zone table
poi_zone = pd.read_excel(path+'poi_zone.xlsx', usecols=['poi_id', 'zone_id'], dtype=int)


# load each year's data and convert to data frame
with open(path + 'zone_time_taxi2019.pickle', 'rb') as file:
    zone_time_taxi2019 = pickle.load(file)
zone_time_taxi2019 = pd.DataFrame(zone_time_taxi2019)

with open(path + 'zone_time_taxi2018.pickle', 'rb') as file:
    zone_time_taxi2018 = pickle.load(file)
zone_time_taxi2018 = pd.DataFrame(zone_time_taxi2018)


# merge all the yearly data
zone_time_taxi = pd.concat([zone_time_taxi2019, zone_time_taxi2018], axis=0)
# sum the pickup and dropoff
zone_time_taxi['taxi_all'] = zone_time_taxi['taxi_pick'] + zone_time_taxi['taxi_drop']

# set the type of the column to be int
zone_time_taxi['zone_id'] = zone_time_taxi['zone_id'].astype('int')
# assign data to each poi
poi_time_taxi = pd.merge(poi_zone, zone_time_taxi, on = 'zone_id', how = 'left')
# <<<<< load the taxi data


# >>>>> load the bike count data
# load the poi_counter table
poi_counter2018 = pd.read_excel(path+'poi_bikeCounter2018.xlsx', usecols=['poi_id', 'counter_id'], dtype=int)
poi_counter2019 = pd.read_excel(path+'poi_bikeCounter2018.xlsx', usecols=['poi_id', 'counter_id'], dtype=int)


# load each year's data and convert to data frame
with open(path + 'counter_window_bike2019.pickle', 'rb') as file:
    counter_window_bike2019 = pickle.load(file)
counter_window_bike2019 = pd.DataFrame(counter_window_bike2019)

with open(path + 'counter_window_bike2018.pickle', 'rb') as file:
    counter_window_bike2018 = pickle.load(file)
counter_window_bike2018 = pd.DataFrame(counter_window_bike2018)

# assign poi_id to the yearly bike data
poi_window_bike2018 = pd.merge(poi_counter2018, counter_window_bike2018, on = 'counter_id', how = 'left')
poi_window_bike2019 = pd.merge(poi_counter2019, counter_window_bike2019, on = 'counter_id', how = 'left')

# merge all the yearly data
poi_time_bike = pd.concat([poi_window_bike2018, poi_window_bike2019], axis=0)
# <<<<< load the bike count data


# >>>>> merge data and save data
# merge the taxi trip data and bike count data
poi_time_taxi = poi_time_taxi.drop_duplicates()
poi_time_bike = poi_time_bike.drop_duplicates()
trafficData = pd.merge(poi_time_taxi, poi_time_bike, on=['poi_id', 'time_start', 'time_end'], how='inner')

# save the data to disck
with open(path + 'trafficData.pickle', 'wb') as file:
    pickle.dump(trafficData, file)
# <<<<< merge data and normalize data









# >>>>> compute the principal componet
temp = trafficData[['taxiAll_norm','bikeCount_norm']]
pca = PCA(n_components=1)  # specify the number of pincipal needed
pca.fit(temp)
pincipals = pca.transform(temp)

#convert pricipal to list
pincipals = pincipals.ravel()
pincipals = pincipals.tolist()
busyness = pincipals


# get the eigen-value of each principal component
component_variances = pca.explained_variance_

# print the eigen-value of each principal component
for i, variance in enumerate(component_variances):
    print(f"principal component {i+1}'s eigen-value: {variance}")
# <<<<< compute the principal componet


# save data object to disk as a pickle file
trafficData['busyness'] = busyness

