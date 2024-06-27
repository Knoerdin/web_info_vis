
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

df = pd.read_csv('A_SeverityCity.csv')
pf = pd.read_csv('A_CityLocation.csv')
pf_unique = pf.drop_duplicates(subset=['City'])

df['Start_Time'] = pd.to_datetime(df['Start_Time'])

specific_months = [(1, 2016), (4, 2016), (7, 2016), (10, 2016), 
                   (1, 2017), (4, 2017), (7, 2017), (10, 2017)]

filtered_df = pd.DataFrame()
for month, year in specific_months:
    temp_df = df[(df['Start_Time'].dt.month == month) & (df['Start_Time'].dt.year == year)]
    filtered_df = pd.concat([filtered_df, temp_df])

filtered_df['Month_Year'] = filtered_df['Start_Time'].dt.to_period('M')
data = filtered_df.groupby(['Month_Year', 'City']).size().reset_index(name='Accidents')
data = data.sort_values(by=['Month_Year', 'Accidents'], ascending=[True, False])


ongelukken_df = pd.DataFrame(data)
#ongelukken_df.to_csv('AA_AccidentsData.csv', index=False)

result = pd.read_csv('AA_AccidentsData.csv')

merged_df = pd.merge(data, pf_unique[['City','lat', 'lng']], 
                     left_on='City', right_on='City', how='left', indicator=True)
accidents_per_month_city_with_loc = merged_df[merged_df['_merge'] == 'both']
accidents_per_month_city_with_loc = accidents_per_month_city_with_loc[['Month_Year', 'City', 'Accidents', 'lat', 'lng']]
#accidents_per_month_city_with_loc.to_csv('A_AccidentsNewData.csv', index=False)
