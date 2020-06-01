#!/usr/bin/env python
# coding: utf-8

# ### Importing  library

# In[50]:


import os
import glob
import pandas as pd
import numpy as np


# ### combing csv's

# In[3]:


os.chdir("C:/Users/chandrakanth/Desktop/test")


# In[4]:


extension = 'csv'
all_filenames = [i for i in glob.glob('*.{}'.format(extension))]


# In[5]:


#combine all files in the list
combined_csv = pd.concat([pd.read_csv(f) for f in all_filenames ])
#export to csv
combined_csv.to_csv( "combined_csv.csv", index=False, encoding='utf-8-sig')


# In[6]:


combined_csv.head(10) # head of data


# In[7]:


combined_csv.shape # shape of data


# In[8]:


combined_csv.dtypes # types of data


# ### Deleting un wanted columns

# In[9]:


data_after_removing_un_wanted_colums = combined_csv.drop(['location','country','unit','utc','attribution'], axis = 1)


# In[10]:


data_after_removing_un_wanted_colums.head(10)


# In[11]:


data_after_removing_un_wanted_colums.shape


# In[12]:


data_after_removing_un_wanted_colums.isnull().sum() # cheaking nan's


# In[13]:


data_after_removing_un_wanted_colums.dtypes # cheaking col types 


# In[14]:


data_after_removing_un_wanted_colums.parameter.describe() #checking unique values in parameter column


# In[16]:


data_after_removing_un_wanted_colums.describe() 


# ### grouping the data on parameter column

# In[15]:


data_after_removing_un_wanted_colums.groupby("parameter").count() # count of unique in parameter column


# In[17]:


data_after_removing_un_wanted_colums.parameter.unique()


# In[18]:


data_unique_values = data_after_removing_un_wanted_colums.copy()


# In[19]:


names = data_after_removing_un_wanted_colums['parameter'].unique().tolist()
#find unique values
store0=data_unique_values[data_unique_values['parameter']==names[0]]
store1=data_unique_values[data_unique_values['parameter']==names[1]]
store2=data_unique_values[data_unique_values['parameter']==names[2]]
store3=data_unique_values[data_unique_values['parameter']==names[3]]
store4=data_unique_values[data_unique_values['parameter']==names[4]]
store5=data_unique_values[data_unique_values['parameter']==names[5]]


# ### Removing parameter column and rename value column with parameter name 
# 

# In[20]:


data_main = store0.rename(columns = {"value": "pm25"})
dataset_main_droped = data_main.drop("parameter",axis=1)
print(dataset_main_droped.head()) #pm25
#'o3'
data_main1 = store1.rename(columns = {"value": "o3"})
dataset_main_droped1 = data_main1.drop("parameter",axis=1)
print(dataset_main_droped1.head())
#'co'
data_main2 = store2.rename(columns = {"value": "co"})
dataset_main_droped2 = data_main2.drop("parameter",axis=1)
print(dataset_main_droped2.head())
#'so2'
data_main3 = store3.rename(columns = {"value": "so2"})
dataset_main_droped3 = data_main3.drop("parameter",axis=1)
print(dataset_main_droped3.head())
# 'no2'
data_main4 = store4.rename(columns = {"value": "no2"})
dataset_main_droped4 = data_main4.drop("parameter",axis=1)
print(dataset_main_droped4.head())
#'pm10'
data_main5 = store5.rename(columns = {"value": "pm10"})
dataset_main_droped5 = data_main5.drop("parameter",axis=1)
print(dataset_main_droped5.head())


# In[21]:


dataset_main_droped.head()


# In[ ]:


# saving to csv cheack point


# In[23]:



dataset_main_droped.to_csv( "dataset_main_droped0.csv", index=False, encoding='utf-8-sig')
dataset_main_droped1.to_csv( "dataset_main_droped1.csv", index=False, encoding='utf-8-sig')
dataset_main_droped2.to_csv( "dataset_main_droped2.csv", index=False, encoding='utf-8-sig')
dataset_main_droped3.to_csv( "dataset_main_droped3.csv", index=False, encoding='utf-8-sig')
dataset_main_droped4.to_csv( "dataset_main_droped4.csv", index=False, encoding='utf-8-sig')
dataset_main_droped5.to_csv( "dataset_main_droped5.csv", index=False, encoding='utf-8-sig')


# In[24]:


df = pd.read_csv("dataset_main_droped0.csv") #reading data sets
df1 = pd.read_csv("dataset_main_droped1.csv")
df2 = pd.read_csv("dataset_main_droped2.csv")
df3 = pd.read_csv("dataset_main_droped3.csv")
df4 = pd.read_csv("dataset_main_droped4.csv")
df5 = pd.read_csv("dataset_main_droped5.csv")


# In[25]:


df.shape
df1.shape


# ### Mergeing datasets on column of city, local latitude, longitude

# In[26]:


result = pd.merge(df,df1, how='outer', on=['city','local', 'latitude','longitude'])


# In[27]:


result.count()


# In[28]:


result = pd.merge(result,df2, how='outer', on=['city','local', 'latitude','longitude'])
result.count()


# In[29]:


result = pd.merge(result,df3, how='outer', on=['city','local', 'latitude','longitude'])
result.count()


# In[30]:


result = pd.merge(result,df5, how='outer', on=['city','local', 'latitude','longitude'])
result.count()


# In[31]:


result = pd.merge(result,df4, how='outer', on=['city','local', 'latitude','longitude'])
result.count()


# In[32]:


result


# In[33]:


result.isnull().sum() #cheacking nan's


# In[34]:


result_without_nan =result.dropna() #droping nan's (due nan's lessthan 12% )


# In[35]:


result_without_nan.isnull().sum()


# In[36]:


result_without_nan.count() 


# In[37]:


result.describe()


# In[38]:


result_without_nan.to_csv( "result_without_nan.csv", index=False, encoding='utf-8-sig') #cheackpoint


# ### visualization

# In[112]:


data=pd.read_csv("C:/Users/chandrakanth/Desktop/test/result_without_nan.csv")


# In[113]:


data.head()


# In[114]:


data.tail()


# In[115]:


data.info()


# In[116]:


data.describe()


# In[117]:


data.isnull().count()


# ## we are analyzing in 3 categories 
# 1. Before covid -19
# 2. IN covid -19
# 3. After Covid -19

# In[118]:


# Before covid-19


# In[119]:


# Setting timestamp as index


# In[120]:


data[' Timestamp'] = pd.to_datetime(data[' Timestamp'],format='%d-%m-%Y %H:%M')

data.info()


# In[146]:


data


# In[121]:


data.set_index(' Timestamp', inplace=True) 
data.sort_index(inplace=True)


# In[122]:


data.head()


# In[123]:


data.tail()


# In[124]:


data.describe()

