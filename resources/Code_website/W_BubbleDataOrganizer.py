import pandas as pd
import numpy as np

def files_ordered(file, output):
    x = pd.read_csv(file)
    date_format = "%Y-%m-%d %H:%M:%S"
    x['datetime'] = pd.to_datetime(x['datetime'],format=date_format, errors='coerce')
    new_data = x[(x['datetime'].dt.year == 2016) | (x['datetime'].dt.year == 2017)]
    new_data.to_csv(output, index=False)
#files_ordered('humidity.csv', 'W_HUMData.csv')
#files_ordered('temperature.csv', 'W_TEMPData.csv')
#files_ordered('wind_speed.csv','W_WINData.csv')


#goeie shit die niet files ordered:)


df = pd.read_csv('A_CityLocation.csv')
pf = pd.read_csv('A_AccidentsNewData.csv')

steden = []
weersteden = df['City'].tolist()
alle_steden = pf['City'].tolist()

for i in weersteden:
    if i in alle_steden:
        steden.append(i)

#Weather score sahbi's
gegevens_steden = []

hum = pd.read_csv('W_HUMData.csv')
win = pd.read_csv('W_WINData.csv')
temp = pd.read_csv('W_TEMPData.csv')


def norm(data):
    min_val = np.min(data)
    max_val = np.max(data)
    normalized_data = ((data - min_val) / (max_val - min_val))
    return normalized_data
def parabool(data):
    min_val = np.min(data)
    max_val = np.max(data)
    avg = (min_val + max_val)/2
    out_data = abs(data - avg)
    return norm(out_data)

hum['datetime'] = pd.to_datetime(hum['datetime'])
win['datetime'] = pd.to_datetime(win['datetime'])
temp['datetime'] = pd.to_datetime(temp['datetime'])

scores = []

filtered_hum = hum[
    ((hum['datetime'].dt.month == 1) | 
    (hum['datetime'].dt.month == 4) |   
    (hum['datetime'].dt.month == 7) |   
    (hum['datetime'].dt.month == 10)) &
    ((hum['datetime'].dt.year == 2016) |
    (hum['datetime'].dt.year == 2017)) 
    ]
    
filtered_win = win[
    ((win['datetime'].dt.month == 1) | 
    (win['datetime'].dt.month == 4) |   
    (win['datetime'].dt.month == 7) |   
    (win['datetime'].dt.month == 10)) &
    ((win['datetime'].dt.year == 2016) |
    (win['datetime'].dt.year == 2017)) 
    ]
    
filtered_temp = temp[
    ((temp['datetime'].dt.month == 1) | 
    (temp['datetime'].dt.month == 4) |   
    (temp['datetime'].dt.month == 7) |   
    (temp['datetime'].dt.month == 10)) &
    ((temp['datetime'].dt.year == 2016) |
    (temp['datetime'].dt.year == 2017))]

dates = filtered_temp['datetime'].dt.date.unique()

hum_grouped = filtered_hum.groupby([filtered_hum['datetime'].dt.year, filtered_hum['datetime'].dt.month])
win_grouped = filtered_win.groupby([filtered_win['datetime'].dt.year, filtered_win['datetime'].dt.month])
temp_grouped = filtered_temp.groupby([filtered_temp['datetime'].dt.year, filtered_temp['datetime'].dt.month])

gegevens_steden = []

for (year, month), hum_group in hum_grouped:
    win_group = win_grouped.get_group((year, month))
    temp_group = temp_grouped.get_group((year, month))
    for city in steden:
        if city not in [item['city'] for item in gegevens_steden if item['date'] == f'{year}-{month}']:
            hum_row = hum_group[city]
            win_row = win_group[city]
            temp_row = temp_group[city]

            norm_hum = norm(hum_row).mean()
            norm_win = norm(win_row).mean()
            norm_temp = parabool(temp_row).mean()

            city_info = df[df['City'] == city].iloc[0]
            gegevens_steden.append({
                'city': city,
                'score': norm_hum + norm_temp + norm_win,
                'lat': city_info['Latitude'],
                'lng': city_info['Longitude'],
                'date': f'{year}-{month:02}',
            })

ongelukken_df = pd.DataFrame(gegevens_steden)
#ongelukken_df.to_csv('W_WeatherDataBest.csv', index=False)

## Data voor choropleth
dataw = pd.read_csv('W_WeatherDataBest.csv')
datac = pd.read_csv('F_StatesAndCities.csv')

maanden = ['2016-01', '2016-04', '2016-07', '2016-10', '2017-01', '2017-04', '2017-07', '2017-10']

unique = datac[['City', 'State']].drop_duplicates()
result = []
for maand in maanden:
    dataw_maand = dataw[dataw['date'] == maand]
    dataw_maand = dataw_maand.merge(unique, left_on='city', right_on='City', how='left')
    state_scores = dataw_maand.groupby('State')['score'].mean().reset_index()
    state_scores['Date'] = maand
    result.append(state_scores)
reresult = pd.concat(result)
#reresult.to_csv('W_PlotData.csv', index=False)


