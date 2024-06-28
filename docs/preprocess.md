# Dataset and Preprocessing

We set out to research the correlation between weather and accidents in the US. To achieve this we took a look at three datasets, these being ‘US Accidents (2016 - 2023)’, ‘Traffic Violations in USA’ and ‘Historical Hourly Weather Data 2012-2017’. ‘US Accidents (2016 - 2023)’ (Moosavi et al.) is a detailed record of vehicle accidents in the US between 2016 and 2023, having recorded the time, place and severity of accidents, among many other variables. ‘Traffic Violations in USA’ (Gutierrez) is a dataset containing a large amount of information about traffic violations and the accidents caused by them. ‘Historical Hourly Weather Data 2012-2017’ (Beniaguev) is a record of weather across the US between the years 2012 and 2017. This dataset has recorded the hourly weather status of many large cities across the United States. With these three datasets we can analyze and compare the link between heavy weather and car accidents across the US.

The first dataset used in this data story is the dataset US Accidents (2016-2023), found on Kaggle. This dataset contains all traffic accidents in America from Febuary 2016 to March 2023. These datapoints are all collected with the help of multiple API's that record traffic accidents and reports them. These API's send out various traffic details which are captured by various entities, such as US and state departments of transportation, law enforcement agencies, traffic cameras, and traffic sensors within the road networks. This dataset contains 7728394 records and 46 different variables. It contains variables on where the accidents took place, when they took place, if any infrastructure was nearby and the severity of the accident. <br>
For this data story only the USA will be researched, so for this dataset we removed all states and cities that were not in the USA. As for the variables, all variables that were not used such as ID, Source, Timezone and so on. To find overlap between the this database and the database mentioned in the next paragraph, only the years 2016 and 2017 were used as these are the overlapping years between the databases.

The second dataset used in this data story is Historical Hourly Weather Data 2012-2017, also found on Kaggle. It contains the data of the weather in various US states as well as some canadian and israeli cities. The records are measured by the hour and records variables such as temparature, humidity, air pressure and wind speed. There are roughly 45300 records in the database.
The only country that will be researched is the US, so all the records of the other countries have been removed from the database. The variables of the database are all in a different csv file which made it more difficult to find correlation between the databases. To overcome this obstacle all the csv files were melted and filtered on year, after the filtering the database was merged to one csv file.

The "Traffic Violations in USA" dataset on Kaggle contains detailed records of traffic violations across the United States. It includes various attributes such as the date of the violation, the location, the type of violation, and details of the individuals involved in the traffic accidents. This dataset is valuable for analyzing traffic patterns, law enforcement practices, and demographic trends related to traffic violations.

## Variable descriptions

|                        | Discrete | Continuous | Ratio | Ordinal | Nominal | Interval |
|------------------------|----------|------------|-------|---------|---------|----------|
| Humidity               |          | X          | X     |         |         |          |
| Wind Speed             | X        |            |       | X       |         |          |
| Temparature            |          | X          | X     |         |         |          |
| State                  | X        |            |       |         | X       |          |
| Weather Score          |          | X          | X     |         |         |          |
| Date                   |          |            |       | X       |         | X        |
| Severity               | X        |            |       | X       |         |          |
| All road variables*    | X        |            |       |         | X       |          |
| All traffic violations** | X        |            |       |         | X       |          |

\* This variable group includes: Amenity, Bump, Crossing, Give_Way, Junction, No_Exit, Railway, Roundabout, Station, Stop, Traffic_Calming, Traffic_Signal, Turning_Loop\\
\** This variable group includes: Belts, Personal Injury, Fatal,Alcohol, Contributed To Accident

## Pre-processing
The code shown below preprocesses weather and accident datasets, and makes it into one universal dataset. It involves converting date formats, and filtering data for the years 2016-2017. The weather data had to be melted in order to merge all seperate csv files in to one dataframe. The datasets are merged on date and state, normalized, and a weather score is calculated. The weather score is made up of three variables; wind_speed, humidity and temperature. To make a general weather score, in which the hight of the score determines the severeness of the weather, we had to normalize all variables. Normalizing the tempereture was especially tricky because both a high and a low temperature is dangerous. This is becouse when temperature is below zero it freezes the road. But with a high temperature there can be more people on the road, as observed in the first visualization. This problem is sloved by making a parabolic function, which makes both the low and the high valus resolve around one. besides that there were no further complications. The final processed dataset, integrating weather conditions with accident data, is saved as weather_accidents.csv for further analysis and visualization.

## Code for perprocessing the main dataset
```python
# Imports
import pandas as pd

# Read all files in this cell
temp_raw = pd.read_csv('../../resources/dataset_weather/us_temperature.csv')
humidity_raw = pd.read_csv('../../resources/dataset_weather/us_humidity.csv')
wind_speed_raw = pd.read_csv('../../resources/dataset_weather/us_wind_speed.csv')
accidents_raw = pd.read_csv('../../resources/us_accidents.csv')

accidents_raw['Start_Time'] = pd.to_datetime(accidents_raw['Start_Time'])
accidents_raw['Date'] = accidents_raw['Start_Time'].dt.date
accidents = accidents_raw.drop(columns=['Start_Time','End_Time', 'Distance(mi)'])
accidents = accidents.sort_values('Date').reset_index(drop=True)

# Convert dates to DateTime format
temp_raw['datetime'] = pd.to_datetime(temp_raw['datetime'])
humidity_raw['datetime'] = pd.to_datetime(humidity_raw['datetime'])
wind_speed_raw['datetime'] = pd.to_datetime(wind_speed_raw['datetime'])

# Filter the dates using .loc()
temp = temp_raw.loc[(temp_raw['datetime'] >= '2016-01-01') & (temp_raw['datetime'] < '2018-01-01')]
humidity = humidity_raw.loc[(humidity_raw['datetime'] >= '2016-01-01') & (humidity_raw['datetime'] < '2018-01-01')]
wind_speed = wind_speed_raw.loc[(wind_speed_raw['datetime'] >= '2016-01-01') & (wind_speed_raw['datetime'] < '2018-01-01')]

# Reset indexes
temp = temp.reset_index(drop=True)
humidity = humidity.reset_index(drop=True)
wind_speed = wind_speed.reset_index(drop=True)

# Melting for all the weather dataframes
temp_melted = pd.melt(temp, id_vars=['datetime'], var_name='State', value_name='Temperature')
humidity_melted = pd.melt(humidity, id_vars=['datetime'], var_name='State', value_name='Humidity')
wind_speed_melted = pd.melt(wind_speed, id_vars=['datetime'], var_name='State', value_name='Wind_Speed')

# Converting beaufort windspeed to km/h
beaufort_scale = {
    0: (0, 1),
    1: (1, 5),
    2: (6, 11),
    3: (12, 19),
    4: (20, 28),
    5: (29, 38),
    6: (39, 49),
    7: (50, 61),
    8: (62, 74),
    9: (75, 88),
    10: (89, 102),
    11: (103, 117),
    12: (118, 133),
    13: (134, 149),
    14: (150, 166),
    15: (167, 183),
    16: (184, 201),
    17: (202, 220)
}

# Calculate the mean wind speed for each Beaufort scale number
beaufort_mean_speeds = {b: (rng[0] + rng[1]) / 2 for b, rng in beaufort_scale.items()}

# Map the Beaufort scale values to mean km/h values
wind_speed_melted['Wind_Speed_km'] = wind_speed_melted['Wind_Speed'].map(beaufort_mean_speeds)
wind_speed_melted = wind_speed_melted.drop(columns=['Wind_Speed'])

# Merge all three weather dataframes with inner join
weather = pd.merge(temp_melted, humidity_melted,on=['datetime','State'], how='inner')
weather = pd.merge(weather, wind_speed_melted,on=['datetime','State'], how='inner')

# Convert datetime to date
weather['Date'] = weather['datetime'].dt.date
weather = weather.drop(columns=['datetime'])

# Group on day and state
weather = weather.groupby(['Date', 'State']).mean()

# Merge the weather and accident dataframes
weather_accidents = pd.merge(weather, accidents, left_on=['Date', 'State'], right_on=['Date', 'City'], how='inner')

def norm(data):
    min_val = min(data)
    max_val = max(data)
    normalized_data = ((data - min_val) / (max_val - min_val))
    return normalized_data
def parabool(data):
    min_val = min(data)
    max_val = max(data)
    avg = (min_val + max_val)/2
    out_data = abs(data - avg)
    return norm(out_data)

weather_accidents['Wind_Speed_km_norm'] = norm(weather_accidents['Wind_Speed_km'])
weather_accidents['Temp_norm'] = parabool(weather_accidents['Temperature'])
weather_accidents['Humid_norm'] = norm(weather_accidents['Humidity'])

weather_accidents['weather_score'] = weather_accidents['Wind_Speed_km_norm'] + weather_accidents['Humid_norm'] + weather_accidents['Temp_norm']
display(weather_accidents)

weather_accidents.to_csv('../../resources/dataset_weather/weather_accidents.csv',index=False)
```
