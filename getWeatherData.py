import pickle
from datetime import datetime, timedelta
import pandas as pd



# load the weather data
path = 'D:/PythonProjects/practicumProject1/'
tempData = pd.read_excel(path +'weather.xlsx')
print(tempData.dtypes)

# >>>>> generate the window start and window end list
window_width = 30
start = [datetime(2022, 1, 1, 0, 0)]
while start[-1] < datetime(2023, 4, 30, 23, 30):
    start.append(start[-1] + timedelta(minutes=window_width))

end = [t+timedelta(minutes=window_width) for t in start]
windowNum = len(end)
# <<<<< generate the window start and window end list


# >>>>> assign the weather to each time windoe
timeWindow = []
temperature = []
precipitation = []
windSpeed = []
weatherCode = []
for k in range(len(start)):
    print([k, len(start)])
    if k % 2 == 0:
        temp = tempData[tempData['datetime']==start[k]]
    else:
        temp = tempData[tempData['datetime']==end[k]]

    if len(temp)>0:
        temp = temp.iloc[0]
        temperature.append(temp[1])
        precipitation.append(temp[2])
        windSpeed.append(temp[4])
        weatherCode.append(temp[3])
        timeWindow.append(start[k])

time_weather = pd.DataFrame({'timeWindow':timeWindow,
                             'temperature':temperature,
                             'precipitation':precipitation,
                             'windSpeed':windSpeed,
                             'weatherCode':weatherCode})
# <<<<< assign the weather to each time window


# save data object to disk as a pickle file
with open(path + 'time_weather.pickle', 'wb') as file:
    pickle.dump(time_weather, file)




