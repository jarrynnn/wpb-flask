#!/usr/bin/env python
# coding: utf-8

# In[2]:


import pandas as pd
import seaborn as sns
import matplotlib as plt
import numpy as np


# # Join data

# In[3]:


df = pd.read_csv('C:\\Users\\Buster\\Documents\\MSc\\Project\\Flask_App_WPB\\wpb-flask\\Modelling\\countries.csv', encoding='latin-1')


# In[4]:


df.head()


# In[9]:


df['countryref_id'] = df['id']


# In[10]:


df.shape


# In[7]:



df_data = pd.read_csv(r'C:\Users\Buster\Documents\MSc\Project\Flask_App_WPB\wpb-flask\Modelling\\country_datas.csv', encoding='latin-1')

df_data.tail()


# In[6]:


df_data.shape


# In[12]:


all_metrics = df_data.merge(df, on = 'countryref_id', how = 'left')


# In[13]:


all_metrics.describe()


# In[14]:


all_metrics.shape


# In[16]:


all_metrics


# In[17]:


all_metrics.isna().sum()


# # Descriptive Statistics

# In[38]:


#separate dfs for each of the metrics

ppt = all_metrics[all_metrics.metric_id ==1]
ppt = ppt[ppt.value.notna()]

ppr = all_metrics[all_metrics.metric_id ==2]
ppr = ppr[ppr.value.notna()]

remand = all_metrics[all_metrics.metric_id ==3]
remand = remand[remand.value.notna()]

fem = all_metrics[all_metrics.metric_id ==4]
fem = fem[fem.value.notna()]

foreign = all_metrics[all_metrics.metric_id ==5]
foreign = foreign[foreign.value.notna()]

occ = all_metrics[all_metrics.metric_id ==6]
occ = occ[occ.value.notna()]


# In[39]:


occ.shape


# In[ ]:


g = sns.pairplot(ppt)


# In[ ]:


columns = ['']


# In[ ]:


correlation = data.corr(method='pearson')
columns = ppt.columns
columns


# In[ ]:



correlation_map = np.corrcoef(data[columns].values.T)
sns.set(font_scale=1.0)
heatmap = sns.heatmap(correlation_map, cbar=True, annot=True, square=True, fmt='.2f', yticklabels=columns.values, xticklabels=columns.values)

plt.show()

