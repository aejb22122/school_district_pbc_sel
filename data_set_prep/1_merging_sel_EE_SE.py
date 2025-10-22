# -*- coding: utf-8 -*-
"""
Created on Fri Jul 10 14:11:07 2020

@author: ajeanbaptiste
"""


import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style="whitegrid")


# In[2]:

"""
SELWEB_PBC_EE_2018_19
SELweb EE scores for SEL Assessment for grades K-3.
SELWEB_PBC_LE_2018_19
SELweb LE scores for SEL Assessment for grades 4-6.

"""
# Importing all the variables
# The data is the SEL information collected by the School district of PBC. 
sel_data_k3 = pd.read_excel("SELWEB_PBC_EE_2018_19.xlsx")
sel_data_4_6 = pd.read_excel('SELWEB_PBC_LE_2018_19.xlsx')

demographics = pd.read_excel('FINAL_DEMOGRAPHICS.xlsx') # ok


# Renaming
sel_data_k3 = sel_data_k3.rename(columns={'PseudoID':'PSEUDOID'})
sel_data_4_6 = sel_data_4_6.rename(columns={'PsuedoID':'PSEUDOID'})



# Deleting un-necessary columns
sel_data_k3 = sel_data_k3.drop(['Last Login', 'selweb_sr_duration', 'sr_duration', 'selweb_duration'], axis = 1)
sel_data_4_6 = sel_data_4_6.drop(['selweb_sr_duration', 'sr_duration', 'selweb_duration', 'Last Login'], axis = 1)

# Stacking the dataframes
SEL = pd.concat([sel_data_k3, sel_data_4_6])

# Verifying the IDs
demographics['PSEUDOID'].isin(SEL['PSEUDOID']) # All the IDs and the counts :
demographics['PSEUDOID'].isin(SEL['PSEUDOID']).value_counts(sort = True, dropna = False) # Count of the common IDs
demographics['PSEUDOID'].isin(SEL['PSEUDOID']).value_counts(sort = True, normalize = True, dropna = False)*100 # Count of the common IDs

# Verifying the IDs
SEL['PSEUDOID'].isin(demographics['PSEUDOID']) # All the IDs and the counts :
SEL['PSEUDOID'].isin(demographics['PSEUDOID']).value_counts(sort = True, dropna = False) # Count of the common IDs
SEL['PSEUDOID'].isin(demographics['PSEUDOID']).value_counts(sort = True, normalize = True, dropna = False) # Count of the common IDs

# In[]
# Exporting the staked data frame
SEL.to_excel('2020_08_25_Stacked_SELweb.xlsx')
