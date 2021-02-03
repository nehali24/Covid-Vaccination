#!/usr/bin/env python
# coding: utf-8

# This a dataset that has been acquired from kaggle. This dataset deals with data of vaccination around the world.

# In[42]:


import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import os
import plotly.express as px
import plotly.graph_objects as go
sns.set()


# In[19]:


vc = pd.read_csv("country_vaccinations.csv")


# In[20]:


vc


# In[21]:


vc.head()


# Dropping irrelevamt fields like "source name" and "source website"

# In[22]:


vc.drop(['source_name', 'source_website'], axis = 1, inplace = True)
vc.head()


# Removing null values from the dataset. 

# In[23]:


vc.isnull().sum(axis = 0 )


# In[24]:


vc


# To find what vaccines are used in different countries. 

# In[25]:


countries = vc['country'].unique()
countries


# In[26]:


d = {}
for i in vc.values:
    d[i[0]] = d.get(i[0], [])
    if i[12] not in d[i[0]]:
        d[i[0]].append(i[12])
for i, j in d.items():
    print(i, " : ", j)
                      
                        


# Maximum people vaccinated in different countries. Here we can see United States has gone through maximum vaccination.

# In[27]:


vc_country = vc.groupby(['country'])['people_vaccinated'].max()
vc_country = vc_country.sort_values(ascending = False)[:10]
plt.bar(vc_country.index, vc_country.values)
plt.xticks(rotation = 90)
plt.show()


# Israel is the country where a huge percentage of population has been vaccinated. 

# In[28]:


vc_country = vc.groupby(['country'])['people_fully_vaccinated_per_hundred'].max()
vc_country = vc_country.sort_values(ascending = False)[:10]
plt.bar(vc_country.index, vc_country.values, color = 'violet')
plt.xticks(rotation = 90)
plt.show()


# Daily vaccination per million is max in Gibraltar, Israel in on second max. 

# In[29]:


vc_country = vc.groupby(['country'])['daily_vaccinations_per_million'].max()
vc_country = vc_country.sort_values(ascending = False)[:10]
plt.bar(vc_country.index, vc_country.values, color = 'green')
plt.xticks(rotation = 90)
plt.show()


# Vaccination per day: Max vaccination around 21s dec 2020. 

# In[30]:


vc_date = vc.groupby('date')['total_vaccinations'].sum()
vc_date = vc_date.sort_values()[:10]
plt.plot(vc_date.index, vc_date.values)
plt.xticks(rotation = 90)
plt.show()


# Vaccination per day country wise. Maximum vaccination per day is taking place in U.S. then China and U.K. 

# In[32]:


vc_country = vc.groupby(['country'])['total_vaccinations'].max()
vc_country = vc_country.sort_values(ascending = False)[:10]
plt.bar(vc_country.index, vc_country.values, color = 'red')
plt.xticks(rotation = 90)
plt.show()


# Total vaccines received according to dataset: U.S. : 31.1233 mln, China: 22.767 mln, 
# U.K. : 9.468382 mln, England: 8.25 mln, Israel: 4.736 mln,India: 3.744 mln 

# In[33]:


vc_country
fig = px.bar(x = vc_country.index, y = vc_country.values, color = vc_country.index, labels = {"x": "country", "y": "total vaccinations"},
            color_discrete_sequence = px.colors.sequential.Plasma)
fig.show()


# In[34]:


vc_country


# In[ ]:





# In[ ]:


vc


# In[35]:


total_vaccinations = vc.groupby(['country']).max()[["total_vaccinations", "vaccines"]].reset_index()
total_vaccinations


# In[36]:


fig = px.choropleth(total_vaccinations, locations = 'country',locationmode = 'country names',color = 'vaccines',
                   title = 'Vaccines used for each country',hover_data= ['total_vaccinations'],
                   color_discrete_map=dict(zip(total_vaccinations['vaccines'], px.colors.sequential.Viridis)),
                   labels={'vaccines': 'Name of vaccine', 'country': 'Country', 'total_vaccinations': 'Number of vaccinations'})
fig.update_geos(
    visible=True, 
    resolution=50,
    showcountries=True, 
    countrycolor="darkgrey"
    )
fig.update_layout(
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='equirectangular'
    ),
)
fig.show()


# Vaccines used by each country: U.S. , Canada, Spain, Germany, Bulgaria Morderna, Pfizer/ BioNTech is being used. In India: Covaxin is beign used. 

# In[39]:


vc


# In[43]:


fig = go.Figure()
title = "Total vaccinations by vaccines"
for vaccine in vc['vaccines'].unique():
    dv = vc[vc['vaccines'] == vaccine]
    fig.add_trace(go.Scatter(x = dv['date'],
                            y = dv['total_vaccinations'],
                            name = vaccine,
                            mode = "lines+markers",
                            hovertemplate = "Date: %{x}<br>Value: %{y}"))
fig.update_layout(title={"text": title})
fig.show()


# In[38]:


total_vac_hundred = vc[['country', 'iso_code', 'total_vaccinations_per_hundred']]
total_vac_hundred['total_vaccinations_per_hundred'] = total_vac_hundred['total_vaccinations_per_hundred'].fillna(0)
total_vac_hundred = total_vac_hundred.groupby(['country', 'iso_code']).max().reset_index()


# In[44]:


def create_choropleth(loc, z, text, title):
    fig = go.Figure(data=go.Choropleth(
        locations = loc,
        z = z,
        text = text,
        colorscale = px.colors.sequential.speed[::-1][::2][1:5],
        autocolorscale=False,
        reversescale=True,
        marker_line_color='darkgray',
        marker_line_width=0.5,
    ))
    
    fig.update_geos(
        visible=True, 
        resolution=50,
        showcountries=True, 
        countrycolor="darkgrey"
        )

    fig.update_layout(
        title_text=title,
        geo=dict(
            showframe=False,
            showcoastlines=False,
            projection_type='equirectangular'
        )
    )

    fig.show()


# In[45]:


create_choropleth(total_vac_hundred['iso_code'], 
                  total_vac_hundred['total_vaccinations_per_hundred'], 
                  total_vac_hundred['country'], 
                  'Total vaccinations per hundred')


# Total people fully vaccinated per hundred is quite low in this dataset.

# In[46]:


fully_vaccinated_hundred = vc[["country", "iso_code","people_fully_vaccinated_per_hundred" ]]
fully_vaccinated_hundred["people_fully_vaccinated_per_hundred"] = fully_vaccinated_hundred["people_fully_vaccinated_per_hundred"].fillna(0)
fully_vaccinated_hundred = fully_vaccinated_hundred.groupby(["country", "iso_code"]).max().reset_index()


# In[47]:


create_choropleth(fully_vaccinated_hundred['iso_code'], 
                  fully_vaccinated_hundred['people_fully_vaccinated_per_hundred'], 
                  fully_vaccinated_hundred['country'], 
                  'People fully vaccinated per hundred')


# In[48]:


daily_vac_million = vc[["country", "iso_code","daily_vaccinations_per_million"]]
daily_vac_million["daily_vaccinations_per_million"] = daily_vac_million["daily_vaccinations_per_million"].fillna(0)
daily_vac_million = daily_vac_million.groupby(["country", "iso_code"]).max().reset_index()


# Daily vaccination per million: U.S.: 4003, China: 771, Israel: 21.07k, UAE: 12.225k.

# In[49]:


create_choropleth(daily_vac_million["iso_code"],
                 daily_vac_million["daily_vaccinations_per_million"],
                 daily_vac_million["country"],
                 "Daily vaccinations per million")


# In[50]:


daily_vac = vc[["country", "iso_code", "daily_vaccinations"]]
daily_vac["daily_vaccinations"] = daily_vac["daily_vaccinations"].fillna(0)
daily_vac = daily_vac.groupby(["country","iso_code"]).max().reset_index()


# Daily vaccinations in Total:U.S. : 1.3249 mln, China: 1.10957 mln, India: 308000.
#     
#     

# In[51]:


create_choropleth(daily_vac['iso_code'], 
                  daily_vac['daily_vaccinations'], 
                  daily_vac['country'], 
                  'Daily vaccinations')


# In[ ]:





# In[ ]:




