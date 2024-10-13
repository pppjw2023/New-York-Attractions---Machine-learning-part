import pickle
import pandas as pd

# >>>>> convert POI data to table
# >>>>> >>>>> load POI data from disk
path = 'D:/PythonProjects/practicumProject/'

with open(path+'POIs.pickle', 'rb') as file:
    POIs = pickle.load(file)

poi = POIs['allPOIs']
# <<<<< <<<<< load POI data from disk

names = []
lats = []
lons = []
types = []
opening_hours = []
opening_hours_covid19 = []
opening_hours_url = []

sn = 0
for k in range(len(poi)):
    print([k, '***', len(poi)])
    temp = poi[k]

    if 'name' in temp['tags']:
        names.append(temp['tags']['name'])
        print(temp['tags']['name'])
    else:
        print('No Name!')
        sn += 1
        names.append('Viewpoint' + str(sn))

    lats.append(temp['lat'])
    lons.append(temp['lon'])
    types.append(temp['tags']['tourism'])

    if 'opening_hours' in temp['tags']:
        opening_hours.append(temp['tags']['opening_hours'])
    else:
        opening_hours.append('NA')

    if 'opening_hours:covid19' in temp['tags']:
        opening_hours_covid19.append(temp['tags']['tourism'])
    else:
        opening_hours_covid19.append('NA')

    if 'opening_hours:url' in temp['tags']:
        opening_hours_url.append(temp['tags']['tourism'])
    else:
        opening_hours_url.append('NA')

poi_table = pd.DataFrame({'names':names,
                          'lats':lats,
                          'lons':lons,
                          'types':types,
                          'opening_hours':opening_hours,
                          'opening_hours_covid19':opening_hours_covid19,
                          'opening_hours_url':opening_hours_url
                        })
poi_table = poi_table.drop_duplicates()

poi_table.to_excel('D:\PythonProjects\practicumProject\poi_table_raw.xlsx', index=False)
# <<<<< convert POI data to table


# >>>>> Add opening time


# <<<<< Add opening time
