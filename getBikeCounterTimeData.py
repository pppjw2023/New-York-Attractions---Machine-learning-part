
import pandas as pd
from datetime import datetime, timedelta
import copy
import pickle

path = 'D:/PythonProjects/practicumProject/'
window_width = 30

# >>>>> prepare the POI dat and the bike count data
# read the POI data into a pandas data frame
poi = pd.read_excel(path+'poi_table.xlsx')

# read the bike count data
rawCountData = pd.read_csv(path + 'Bicycle_Counts.csv')
# read the bike counter data
rawCounterData = pd.read_csv(path + 'Bicycle_Counters.csv')
# convert the date column to time format
rawCountData['date'] = rawCountData['date'].apply(lambda x: datetime.strptime(x, '%m/%d/%Y %I:%M:%S %p'))
# take out the year column
rawCountData['year'] = rawCountData['date'].apply(lambda x: x.year)

# take out the data of the counters in Manhattan
rawCounterData = rawCounterData[rawCounterData['Manhattan']==1]
# <<<<< prepare the POI dat and the bike count data


# <<<<<<<<<<<<<<<<< >>>>>>>>>>>>>>>>>>
# produce the yearly bike count data for POI
# <<<<<<<<<<<<<<<<< >>>>>>>>>>>>>>>>>>
year = 2019 # set the year value

# >>>>> match the POI with counter by distance
# take out the year's raw count data
rawCountDataYearly = rawCountData[rawCountData['year']==year]
# take out all the counter id in this year
allCounter = set(rawCountDataYearly['id'])
# take out the effective counter data in this year
rawCounterDataYearly = rawCounterData[rawCounterData['id'].isin(allCounter)]
# delete the counter with only zero
goodCounters = []
for k in allCounter:
    temp = rawCountDataYearly[rawCountDataYearly['id']==k]
    if temp['counts'].sum()!=0:
        goodCounters.append(k)
# take out the effective counter data in this year
rawCounterDataYearly = rawCounterDataYearly[rawCounterDataYearly['id'].isin(goodCounters)]

# reset index
poi = poi.reset_index(drop=True)
rawCountDataYearly = rawCountDataYearly.reset_index(drop=True)
rawCounterDataYearly = rawCounterDataYearly.reset_index(drop=True)

# add a column to store the matched counter id
poi['counter_id'] = 0
# match the poi and counter by distance
for k in range(len(poi['poi_name'])):
    tempDist = []
    for kk in range(len(rawCounterDataYearly['id'])):
        print([k, len(poi['poi_name']), '***', kk, len(rawCounterDataYearly['id'])])
        dist = abs(poi['lat'][k]-rawCounterDataYearly['latitude'][kk])+abs(poi['lon'][k]-rawCounterDataYearly['longitude'][kk])
        tempDist.append(dist)
    minDist = min(tempDist)
    ind = tempDist.index(minDist)
    poi.loc[k, 'counter_id'] = rawCounterDataYearly.loc[ind, 'id']

# save the matched poi and bike counter id for this year
poi.to_excel(path + 'poi_bikeCounter{}.xlsx'.format(year), index = False)
# <<<<< match the POI with counter by distance


# >>>>> take out the poi-related count data
# take out the id of Manhattan counter
relatedCounterIDs = set(poi['counter_id'])
# take out the data of Manhattan
rawCountDataYearly = rawCountDataYearly[rawCountDataYearly['id'].isin(relatedCounterIDs)]
rawCountDataYearly = rawCountDataYearly[rawCountDataYearly['id'].isin(relatedCounterIDs)]
# <<<<< take out the poi-related count data

# >>>>> generate half hour window data for a year
relatedCounterIDs = list(relatedCounterIDs)
# copy the yearly data
countDataYearly = copy.deepcopy(rawCountDataYearly)

# create an empty dataframe
counter_id = []
time_start = []
time_end = []
bikeCount =[]

for k in range(len(relatedCounterIDs)):
    # take out the yearly data of a counter ID
    thisId = relatedCounterIDs[k]
    thisIdData = countDataYearly[countDataYearly['id']==thisId]
    # get the time window data for this counter ID
    window_start = datetime(year, 1, 1, 0, 0)
    while window_start<= datetime(year, 12, 31, 23, 30):
        window_end = window_start + timedelta(minutes=window_width)
        # take out the count data in this window
        tempIdWindowCount = thisIdData[(thisIdData['date']>=window_start)&(thisIdData['date']<window_end)]
        # store result
        counter_id.append(thisId)
        time_start.append(window_start)
        time_end.append(window_end)

        if len(tempIdWindowCount)>0:
            bikeCount.append(tempIdWindowCount['counts'].sum())
        else:
            bikeCount.append(9999)

        print([k, len(relatedCounterIDs), str(time_start[-1]), str(time_end[-1]), bikeCount[-1]])
        window_start = window_end
# <<<<< generate half hour window data


# >>>>> generate half hour window data
counter_window_bike = {'counter_id': counter_id,
                            'time_start': time_start,
                            'time_end': time_end,
                            'bikeCount': bikeCount
                           }
with open(path + 'counter_window_bike{}.pickle'.format(year), 'wb') as file:
    pickle.dump(counter_window_bike, file)
# <<<<< generate half hour window data for a year












