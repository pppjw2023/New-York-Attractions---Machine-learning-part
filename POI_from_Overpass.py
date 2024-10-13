import overpass
import pickle
import os

# get the current path of this script
current_path = os.path.abspath(os.path.dirname(__file__))
# change the working directory to the current path
os.chdir(current_path)


# >>>>> Create an Overpass API object
api = overpass.API() # create an instance
api.timeout = 900 # increase the timeout to 300 seconds.
api.maxsize = 1073741824  # 1 GB
# <<<<< Create an Overpass API object


# >>>>> configure query
lat_start = 40.680086
lat_end = 40.883955

lon_start = -74.056602
lon_end = -73.898769

query = """
    area[name="Manhattan"]->.searchArea;
    (
        node(area.searchArea)[tourism]({},{},{},{});
    );
    out center
""".format(lat_start, lon_start, lat_end, lon_end)
# <<<<< configure query


# >>>>> Send the query and get response
response = api.get(query, responseformat="json")

if 'elements' in response:
    elements = response['elements']
else:
    print("No data found")
# <<<<< Send the query and get response


# >>>>> take out POIs
# take out all the values of tourism
tourism = [t['tags']['tourism'] for t in elements]
tourism = set(tourism)

# take out all the museum data
museums = [t for t in elements if t['tags']['tourism']=='museum']
# take out all the viewpoint data
viewpoints = [t for t in elements if t['tags']['tourism']=='viewpoint']

# pool museum data and viewpoint data to a POI data
allPOIs = museums + viewpoints
# <<<<< take out POIs

# >>>>> save POI data to disk
POIs = {'museums': museums, 'viewpoints': viewpoints, 'allPOIs': allPOIs}
with open('POIs.pickle', 'wb') as file:
    pickle.dump(POIs, file)
# <<<<< save POI data to disk


# # >>>>> load POI data from disk
# path = 'D:/PythonProjects/practicumProject/'
#
# with open(path+'POIs.pickle', 'rb') as file:
#     POIs = pickle.load(file)
#
# allPOIs = POIs['allPOIs']
# museums = POIs['museums']
# viewpoints = POIs['viewpoints']
# # <<<<< load POI data from disk