#!/usr/bin/env python
# coding: utf-8

# 21 Days lockdown pollution analysis with python
# 
# Author : Prajjwal Pathak
# 
# * Data here is based on  (CPCB - India Central Pollution Control Board) as well as the World Air Quality Index Project.
# 
# Youtube : pyGuru

# # Realtime pollution analysis

# api : http://api.waqi.info/
# 
# Get your api key from here : https://aqicn.org/data-platform/token/#/

# Getting data

# In[ ]:


import requests


# In[ ]:


city = 'Hyderabad'
url = 'http://api.waqi.info/feed/' + city + '/?token='
api_key = '5c14bf7e236da8d9fc59c599d5b4d2739e8fa650'

main_url = url + api_key
r = requests.get(main_url)
data = r.json()['data']
data


# Extracting air quality information

# In[ ]:


aqi = data['aqi']
iaqi = data['iaqi']

del iaqi['p']

for i in iaqi.items():
    print(i[0],':',i[1]['v'])


# In[ ]:


dew = iaqi.get('dew','Nil')
no2 = iaqi.get('no2','Nil')
o3 = iaqi.get('o3','Nil')
so2 = iaqi.get('so2','Nil')
pm10 = iaqi.get('pm10','Nil')
pm25 = iaqi.get('pm25','Nil')

print(f'{city} AQI :',aqi,'\n')
print('Individual Air quality')
print('Dew :',dew)
print('no2 :',no2)
print('Ozone :',o3)
print('sulphur :',so2)
print('pm10 :',so2)
print('pm25 :',pm25)


# Plotting pollutants graph
# 

# In[ ]:


import matplotlib.pyplot as plt

pollutants = [i for i in iaqi]
values = [i['v'] for i in iaqi.values()]


# Exploding the first slice
explode = [0 for i in pollutants]
mx = values.index(max(values))  # explode 1st slice
explode[mx] = 0.1

# Plot a pie chart
plt.figure(figsize=(8,6))
plt.pie(values, labels=pollutants,explode=explode,autopct='%1.1f%%', shadow=True)

plt.title('Air pollutants and their probable amount in atmosphere [kanpur]')

plt.axis('equal')
plt.show()


# Plotting location on the map using cartopy

# Installing cartopy in colab

# In[ ]:


get_ipython().system('apt-get install libproj-dev proj-data proj-bin')
get_ipython().system('apt-get install libgeos-dev')
get_ipython().system('pip install cython')
get_ipython().system('pip install cartopy')


# In[ ]:


get_ipython().system('pip uninstall shapely')
get_ipython().system('pip install shapely --no-binary shapely')


# Installing cartopy in normal python / anaconda
# 
# 
# watch installation tutorial : [Installing Cartopy](https://youtu.be/qxSCoR9BO6A)

# In[ ]:


conda install -c conda-forge cartopy


# Plotting a map of the city

# In[ ]:


import cartopy.crs as ccrs

geo = data['city']['geo']

fig = plt.figure(figsize=(10,8))
ax = plt.axes(projection=ccrs.PlateCarree())
ax.stock_img()

plt.scatter(geo[1],geo[0],color='blue')
plt.text(geo[1] + 3,geo[0]-2,f'{city} AQI \n    {aqi}',color='red')

plt.show()


# # Historical data analysis

# dataset : http://aqicn.org/data-platform/register/

# Read csv files into a dataframe

# In[ ]:


import pandas as pd


csv_path = '/content/drive/My Drive/Colab Notebooks/Data and Visulization/Air pollution/nehru-nagar, kanpur-air-quality.csv'

df = pd.read_csv(csv_path)
df = df.head(50)
print(df)


# Renaming column names 

# In[ ]:


df.columns

df= df.rename(columns = {" pm25": "pm25", 
                         " pm10":"pm10", 
                         " o3": "o3",
                         ' no2' : 'no2',
                         ' so2' : 'so2',
                         ' co' : 'co'})

df.columns


# Extract dates of lockdown

# In[ ]:


df['date'] = pd.to_datetime(df.date)

df21 = df.loc[df['date'] > '2020-03-24']
df21 = df21.sort_values(by = 'date')
df21


# Remove any extra date apart from 21 days

# In[ ]:


df21.drop(13, inplace=True)
df21


# Filling all the empty cells with 0

# In[ ]:


df21.replace(' ', '0', inplace=True)
df21


# Plotting the data

# In[ ]:


import matplotlib.pyplot as plt

dates = df21['date']
pm25 = df21['pm25']
pm25 = [int(i) for i in pm25]

plt.figure(figsize=(10,8))

length = len(dates)

plt.plot(dates,pm25)
plt.title('PM2.5 values in lockdown days')
plt.xlabel('Dates of lockdown')
plt.ylabel('PM2.5 values')
plt.show()


# Extracting past 21 days before lockdown

# In[ ]:


mask = (df['date'] >= '2020-03-05') & (df['date']  < '2020-03-25')

past21 = df.loc[mask]
past21


# Compairing the two

# In[ ]:


import matplotlib.pyplot as plt

dates = df21['date']
pm25_l = df21['pm25']
pm25_l = [int(i) for i in pm25]


pm25_n = past21['pm25']
pm25_n = [int(i) for i in pm25_n]

plt.figure(figsize=(10,8))

length = [i for i in range(1,len(dates)+1)]

plt.plot(length,pm25_l,color='blue',label='under lockdown')
plt.plot(length,pm25_n,color='red',label='before lockdown')
plt.legend()
plt.title('Comparision of before lockdown vs under lockdown pm2.5 values')
plt.show()


# Finding solutions to several questions

# 1> On which date pm2.5 value was minimum in kanpur under lockdown

# In[ ]:


df21['pm25'] = [int(i) for i in df21['pm25']]
print(df21[df21.pm25 == df21.pm25.min()]) 


# 2> On which date o3 value was maximum in kanpur under lockdown

# In[ ]:


df21['o3'] = [int(i) for i in df21['o3']]
print(df21[df21.o3 == df21.o3.max()]) 


# 3> What is the average value of so2 in the lockdown 

# In[ ]:


df21['so2'] = [int(i) for i in df21['so2']]
avgSo2 = df21['so2'].mean()
print('The average value of so2 :',avgSo2)

