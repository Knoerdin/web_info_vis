import pandas as pd
import numpy as np

"""
df = pd.read_csv('US_Accidents_March23.csv')
ef = pd.read_csv('city_attributes.csv')
pf = pd.read_csv('BubbleMapData.csv')
stedenn = []
weersteden = ef['City'].tolist()
alle_steden = pf['City'].tolist()

for i in weersteden:
    if i in alle_steden:
        stedenn.append(i)


steden = list(set(ef['City']).intersection(set(pf['City'])))

vars_nodig_usa = ['Severity', 'Start_Time', 'City', 'State']
months_to_keep = [1, 4, 7, 10]
years_to_keep = [2016, 2017]

df['Start_Time'] = pd.to_datetime(df['Start_Time'], format="%Y-%m-%d %H:%M:%S", errors='coerce')

filtered_data = df[df['City'].isin(steden) & df['Start_Time'].dt.year.isin(years_to_keep)]
filtered_data['Start_Time'] = filtered_data['Start_Time'].dt.date

average_severity_df = filtered_data.groupby(['Start_Time', 'City', 'State'])['Severity'].mean().reset_index()
average_severity_df.rename(columns={'Severity': 'Average_Severity'}, inplace=True)

average_severity_df['Year'] = pd.to_datetime(average_severity_df['Start_Time']).dt.year
average_severity_df['Month'] = pd.to_datetime(average_severity_df['Start_Time']).dt.month

filtered_df = average_severity_df[
    (average_severity_df['Year'].isin(years_to_keep)) &
    (average_severity_df['Month'].isin(months_to_keep))
]

filtered_df.drop(columns=['Year', 'Month'], inplace=True)

#filtered_df.to_csv('F_StatesAndCities.csv', index=False)
"""



###### Per datum ongeluk severity en stad ophalen(later weather score aan stad voor die datum koppelen)
# Totale csv file komt dan: Severity, Time_Start(Date), City, Weather-score

#csv file met alle weatherscores per stad per dag(van Jan Apr July Oct, van 2016 en 2017).

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


def dater(hum, win, temp, stedenn):
    hum['datetime'] = pd.to_datetime(hum['datetime'])
    win['datetime'] = pd.to_datetime(win['datetime'])
    temp['datetime'] = pd.to_datetime(temp['datetime'])

    scores = []

    filtered_hum = hum[
        ((hum['datetime'].dt.month.isin([1, 4, 7, 10])) &
        (hum['datetime'].dt.year.isin([2016, 2017])))
    ]
    
    filtered_win = win[
        ((win['datetime'].dt.month.isin([1, 4, 7, 10])) &
        (win['datetime'].dt.year.isin([2016, 2017])))
    ]
    
    filtered_temp = temp[
        ((temp['datetime'].dt.month.isin([1, 4, 7, 10])) &
        (temp['datetime'].dt.year.isin([2016, 2017])))
    ]
    
    dates = filtered_temp['datetime'].dt.date.unique()
    
    for date in dates:
        for city in stedenn:
            hum_row = filtered_hum[filtered_hum['datetime'].dt.date == date][city]
            win_row = filtered_win[filtered_win['datetime'].dt.date == date][city]
            temp_row = filtered_temp[filtered_temp['datetime'].dt.date == date][city]

            if not hum_row.empty and not win_row.empty and not temp_row.empty:
                norm_hum = norm(hum_row).mean()
                norm_win = norm(win_row).mean()
                norm_temp = parabool(temp_row).mean()

                score = norm_hum + norm_temp + norm_win

                scores.append({
                    'City': city,
                    'Date': date,
                    'Score': score
                })
    
    jippie = pd.DataFrame(scores)
    jippie = jippie.sort_values(by=['Date', 'City'])
    jippie.to_csv('FFF_WeatherData.csv', index=False)

# Load data
hum = pd.read_csv('W_HUMData.csv')
win = pd.read_csv('W_WINData.csv')
temp = pd.read_csv('W_TEMPData.csv')
df = pd.read_csv('F_StatesAndCities.csv')
pf = pd.read_csv('A_AccidentsNewData.csv')

# Filter cities
ene = df['City'].unique().tolist()
andere = pf['City'].unique().tolist()
steden = [i for i in ene if i in andere]

# Execute main function
#dater(hum, win, temp, steden)

### Laatste CSV, ik beloof t (denk ik...)

k = pd.read_csv('F_StatesAndCities.csv')
kk = pd.read_csv('F_WeatherData.csv')

datess = k['Start_Time'].unique()

einde_is_in_zicht = []

for da in datess:
    steden_op_datum = k[k['Start_Time'] == da]['City']
    for steed in steden_op_datum:
        gemiddelde_severity = k[(k['Start_Time'] == da) & (k['City'] == steed)]['Average_Severity'].values[0]
        state = k[(k['Start_Time'] == da) & (k['City'] == steed)]['State'].values[0]
        weatherscore = kk[(kk['Date'] == da) & (kk['City'] == steed)]['Score'].values[0]
        einde_is_in_zicht.append({
            'Date': da,
            'City' : steed,
            'State' : state,
            'Weather_Score' : weatherscore,
            'Average_Severity' : gemiddelde_severity
        })

ehm = pd.DataFrame(einde_is_in_zicht)
sorted_ehm = ehm.sort_values(by=['Date', 'State']).reset_index(drop=True)
#sorted_ehm.to_csv('F_StatesEnAl.csv', index=False)


#states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire', 'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio','Oklahoma', 'Oregon', 'Pennsylvania',  'Rhode Island', 'South Carolina', 'South Dakota', 'Tennessee', 'Texas','Utah', 'Vermont',  'Virginia', 'Washington', 'West Virginia', 'Wisconsin','Wyoming']
readread = pd.read_csv('F_StatesEnAl.csv')

regions = {
    'South': ['AR','LA','MS','AL','TN','KY','WV','GA','FL','SC','NC','VA'],
    'New England': ['ME','VT','NH','MA','CT','RI'],
    'Great Plains' : ['ND','SD','NE','KS','OK'],
    'Rocky Mountains': ['MT','ID','WY','UT','CO'],
    'Mid Atlantic': ['NY','PA','NJ','DE','MD','DC'],
    'West Coast': ['CA','OR','WA'],
    'Mid West': ['MN','IA','WI','MO','IL','IN','MI','OH'],
    'South West': ['NV','TX','AZ','NM'],
    'Alaska Hawaii': ['AK','HI'],
}
def get_region(state):
    for region, states in regions.items():
        if state in states:
            return region
    return None

def process_data(df):
    finale = []
    
    for _, row in df.iterrows():
        state = row['State']
        region = get_region(state)
        severity = row['Average_Severity']
        wscore = row['Weather_Score']
        date = row['Date']
        
        finale.append({
            'Date': date,
            'Region': region,
            'Weather_Score': wscore,
            'Average_Severity': severity
        })
    
    return pd.DataFrame(finale)  

kaas = process_data(readread)
#kaas.to_csv('F_PlotData.csv', index=False)


