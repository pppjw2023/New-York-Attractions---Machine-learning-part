import pickle
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
import numpy as np
import holidays


path = 'D:/PythonProjects/practicumProject/'

# >>>>> load the data and merge them
# load traffic busyness data
with open(path + 'trafficData.pickle', 'rb') as file:
    trafficData = pickle.load(file)
    trafficData = trafficData[['poi_id', 'time_start', 'time_end', 'taxi_all', 'bikeCount']]

# load weather data
with open(path + 'time_weather2019.pickle', 'rb') as file:
    time_weather2019 = pickle.load(file)
with open(path + 'time_weather2018.pickle', 'rb') as file:
    time_weather2018 = pickle.load(file)

# merge the two yearly data
time_weather = pd.concat([time_weather2018, time_weather2019], axis=0)

# Merge by rows
allData = pd.merge(trafficData, time_weather, on=['time_start', 'time_end'], how='left')

allData = allData.dropna(how='any')
# <<<<< load the data and merge them


# >>>>> normalize columns and compute the busyness
# normalize the numeric columns
scaler = StandardScaler()
columnsToScale = ['taxi_all','bikeCount', 'temperature', 'windSpeed']
columnsScaled = ['taxiAll_norm','bikeCount_norm', 'temperature_norm', 'windSpeed_norm']
allData[columnsScaled] = scaler.fit_transform(allData[scalerOrder])

# convert to string column
allData['weatherCode'] = allData['weatherCode'].astype(int)
allData['weatherCode'] = allData['weatherCode'].astype(str)
allData.reset_index(drop=True, inplace=True)
# <<<<< normalize columns and compute the busyness


# >>>>> construct weekday and holiday
# construct weekday
allData['weekday']=allData['time_start'].dt.strftime('%A')

# Create a holiday object and specify New York State
ny_holidays = holidays.US(state='NY')
allData['holiday'] = allData['time_start'].apply(lambda x: x in ny_holidays)

# Mark the time window
allData['timeWindow'] = allData['time_start'].dt.strftime('%H:%M:%S')
# <<<<< construct weekday and holiday


# >>>>> take out useful columns
useColumns = ['poi_id', 'weekday', 'holiday', 'timeWindow', 'taxiAll_norm','bikeCount_norm', 'temperature_norm', 'windSpeed_norm', 'weatherCode']
allData = allData[useColumns]
# <<<<<  take out useful columns


# >>>>> compute the principal componet
temp = allData[['taxiAll_norm','bikeCount_norm']]
# Specify the number of principal components to retain.
pca = PCA(n_components=1)
pca.fit(temp)
pincipals = pca.transform(temp)

# convert pricipal to list
pincipals = pincipals.ravel()
pincipals = pincipals.tolist()
# put the busyness into the data set
allData['busyness'] = pincipals
# drop the unuseful columns
allData = allData.drop(columns=['taxiAll_norm', 'bikeCount_norm'])

# save data set
dataForModel = {'data':allData, 'columnsToScale':columnsToScale, 'columnsScaled':columnsScaled, 'scaler':scaler}
with open(path + 'dataForModel.pickle', 'wb') as file:
    pickle.dump(dataForModel, file)

# # Obtain the eigenvalue of each principal component.
# component_variances = pca.explained_variance_
#
# # Print the eigenvalue of each principal component.
# for i, variance in enumerate(component_variances):
#     print(f"Principal Component {i+1}'s eigen-value: {variance}")

# <<<<< compute the principal componet


# ￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥
#      Random Forest
# ￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥￥

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, mean_squared_error
import joblib


# load data set
path = 'D:/PythonProjects/practicumProject/'
with open(path + 'dataForModel.pickle', 'rb') as file:
    dataForModel = pickle.load(file)
scaler = dataForModel['scaler']
data = dataForModel['data']
columnsToScale = dataForModel['columnsToScale']
columnsScaled = dataForModel['columnsScaled']

# seperate the target and input
subData = data.sample(frac=0.1, replace=False, random_state=44215)
X = (subData.drop(columns=['busyness']))
y = subData['busyness']

# convert categorical variables to one-hot coded variables
categoricalColumns = ['poi_id', 'weekday', 'timeWindow', 'weatherCode']
X[categoricalColumns] = X[categoricalColumns].astype(str)
X = pd.get_dummies(X, columns=categoricalColumns)
X_columns = X.columns

# divid data to traning set and test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Create a Random Forest Regressor
n_estimators = 50
max_depth = 100
# model to be evalued
#rf_regressor = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=4452)
# model to be saved.
rf_regressor = RandomForestRegressor(n_estimators=n_estimators, max_depth=max_depth, random_state=4452, oob_score = False)

# train regressor on training data
rf_regressor.fit(X_train, y_train)

# predition on test data
y_pred = rf_regressor.predict(X_test)

# calculate mse
mse = mean_squared_error(y_test, y_pred)

print('n_estimators = ', n_estimators)
print('max_depth = ', max_depth)
print('Mean Squared Error:', mse, end='\n')


# >>>>> save the trained model of Random Forest Regression
trainnedModel = {'model':rf_regressor,
                 'columnsToScale':columnsToScale,
                 'columnsScaled':columnsScaled,
                 'X_columns':X_columns,
                 'scaler':scaler}
with open(path+'trainedModel.pickle', 'wb') as file:
    pickle.dump(trainedModel, file)
# <<<<< save the trained model of Random Forest Regression
