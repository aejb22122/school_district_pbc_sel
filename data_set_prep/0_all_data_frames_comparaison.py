#!/usr/bin/env python
# coding: utf-8

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

import os

# pd.set_option('display.max_columns', None)
# pd.set_option('display.max_rows', None)
#sns.set_style("darkgrid")
sns.set(style="whitegrid")

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

# =============================================================================
# List files in the raw data folder 
os.listdir()


# -----------------------------------------------------------------------------
# Let's start by importing all the datasets
# The data is the SEL information collected by the School district of PBC. 
df0 = pd.read_excel("SELWEB_PBC_EE_2018_19.xlsx")
df1 = pd.read_excel('SELWEB_PBC_LE_2018_19.xlsx')
df2 = pd.read_excel("FINAL_DISCIPLINE.xlsx") # ok
df3 = pd.read_excel("FINAL_K-5_SEL.xlsx") # ok
df4 = pd.read_excel('FINAL_GRADES.xlsx') # ok
df5 = pd.read_excel('FINAL_6-12_SEL.xlsx') # ok
#df6 = pd.read_excel('FINAL_DEMOGRAPHICS.xlsx') # ok
df6 = pd.read_excel('FINAL_DEMOGRAPHICS_UPDATE.xlsx') # ok
df7 = pd.read_excel('FINAL_FSAELA.xlsx') # ok
df8 = pd.read_excel('FINAL_FSAMATH.xlsx') # ok
df9 = pd.read_excel('FINAL_IREADY_ELA_DEM.xlsx') # ok
df10 = pd.read_excel('FINAL_IREADY_MATH_DEM.xlsx') # ok

# -----------------------------------------------------------------------------
print('As a reminder :')
print('SELWEB_PBC_EE_2018_19 : df0 = ', len(df0), 'obervations') 
print('SELWEB_PBC_LE_2018_19 : df1 =', len(df1), 'obervations') 
print('FINAL_DISCIPLINE : df2 =', len(df2), 'obervations') 
print('FINAL_K-5_SEL : df3 =', len(df3), 'obervations') 
print('FINAL_GRADES : df4 =', len(df4), 'obervations') 
print('FINAL_6-12_SEL : df5 =', len(df5), 'obervations') 
print('FINAL_DEMOGRAPHICS : df6 =', len(df6), 'obervations') 
print('FINAL_FSAELA : df7 = ', len(df7), 'obervations') 
print('FINAL_FSAMATH : df8 =', len(df8), 'obervations') 
print('FINAL_IREADY_ELA_DEM :df9 =', len(df9), 'obervations') 
print('FINAL_IREADY_MATH_DEM : df10 =', len(df10), 'obervations') 

# -----------------------------------------------------------------------------
# Print the columns
print(df0.columns)
print(df1.columns)
print(df2.columns)
print(df3.columns)
print(df4.columns)
print(df5.columns)
print(df6.columns)
print(df7.columns)
print(df8.columns)
print(df9.columns)
print(df10.columns)

# -----------------------------------------------------------------------------
# Renaiming the columns
df0 = df0.rename(columns={"PseudoID": "ID"})
df1 = df1.rename(columns={"PsuedoID": "ID"})
df2 = df2.rename(columns={'PSUEDOID': "ID"})
df3 = df3.rename(columns={'PSUEDOID': "ID"})
df4 = df4.rename(columns={'PSEUDOID': "ID"})
df5 = df5.rename(columns = {'PSUEDOID': "ID"})
df6 = df6.rename(columns={'PSEUDOID': "ID"})
df7 = df7.rename(columns = {'PSUEDOID': 'ID'})
df8 = df8.rename(columns={'PSUEDOID': "ID"})
df9 = df9.rename(columns={'PSUEDOID': "ID"})
df10 = df10.rename(columns={'PSUEDOID': "ID"})

# -----------------------------------------------------------------------------
# Removing the NaN
# df0 = df0.dropna(axis = 0)
# df1 = df1.dropna(axis = 0)
# df2 = df2.dropna(axis = 0)
# df3 = df3.dropna(axis = 0)
# df4 = df4.dropna(axis = 0)
# df5 = df5.dropna(axis = 0)
# df6 = df6.dropna(axis = 0)
# df7 = df7.dropna(axis = 0)
# df8 = df8.dropna(axis = 0)
# df9 = df9.dropna(axis = 0)
# df10 = df10.dropna(axis = 0)


# =============================================================================
# Creating a data frame with only the IDs for all the datasets 
# =============================================================================
ID_df0 = df0['ID']
ID_df1 = df1['ID']
ID_df2 = df2['ID']
ID_df3 = df3['ID']
ID_df4 = df4['ID']
ID_df5 = df5['ID']
ID_df6 = df6['ID']
ID_df7 = df7['ID']
ID_df8 = df8['ID']
ID_df9 = df9['ID']
ID_df10 = df10['ID']

# =============================================================================
# Transforming the series into a dataframe
ID_df0 = pd.DataFrame(ID_df0)
ID_df1 = pd.DataFrame(ID_df1)
ID_df2 = pd.DataFrame(ID_df2)
ID_df3 = pd.DataFrame(ID_df3)
ID_df4 = pd.DataFrame(ID_df4)
ID_df5 = pd.DataFrame(ID_df5)
ID_df6 = pd.DataFrame(ID_df6)
ID_df7 = pd.DataFrame(ID_df7)
ID_df8 = pd.DataFrame(ID_df8)
ID_df9 = pd.DataFrame(ID_df9)
ID_df10 = pd.DataFrame(ID_df10)


# ID_df0 = pd.DataFrame(df0['ID'].value_counts(sort = True, dropna = False))
# ID_df1 = pd.DataFrame(df1['ID'].value_counts(sort = True, dropna = False))
# ID_df2 = pd.DataFrame(df2['ID'].value_counts(sort = True, dropna = False))
# ID_df3 = pd.DataFrame(df3['ID'].value_counts(sort = True, dropna = False))
# ID_df4 = pd.DataFrame(df4['ID'].value_counts(sort = True, dropna = False))
# ID_df5 = pd.DataFrame(df5['ID'].value_counts(sort = True, dropna = False))
# ID_df6 = pd.DataFrame(df6['ID'].value_counts(sort = True, dropna = False))
# ID_df7 = pd.DataFrame(df7['ID'].value_counts(sort = True, dropna = False))
# ID_df8 = pd.DataFrame(df8['ID'].value_counts(sort = True, dropna = False))
# ID_df9 = pd.DataFrame(df9['ID'].value_counts(sort = True, dropna = False))
# ID_df10 = pd.DataFrame(df10['ID'].value_counts(sort = True, dropna = False))



# =============================================================================
# Demographic versus all others - versus each dataframe
# =============================================================================
# Demographic versus all others
# df6 = pd.read_excel('FINAL_DEMOGRAPHICS.xlsx')
# The final demographis is the file to link all others
# SEL LE and EE or the other way arround- have stacked and not merged

print('FINAL_DEMOGRAPHICS : df6 =', len(df6), 'obervations') 

print('FINAL_DEMOGRAPHICS : df6 Vs SELWEB_PBC_LE_2018_19 : df1') 
print('Comparing FINAL_DEMOGRAPHICS with SELWEB_PBC_LE_2018_19 : 2.29 % acc')
print("Comparing FINAL_DEMOGRAPHICS_UPDATE with SELWEB_PBC_LE_2018_19 : 2.29 % acc'")
ID_df6['ID'].isin(ID_df1['ID'])
ID_df6['ID'].isin(ID_df1['ID']).value_counts(sort = True, dropna = False)
ID_df6['ID'].isin(ID_df1['ID']).value_counts(sort = True, normalize = True, dropna = False)


print('FINAL_DEMOGRAPHICS : df6 Vs FINAL_DISCIPLINE : df2') 
print('Comparing FINAL_DEMOGRAPHICS with FINAL_DISCIPLINE : 9.28% acc')
print("Comparing FINAL_DEMOGRAPHICS_UPDATE with FINAL_DISCIPLINE : 9.28")
ID_df6['ID'].isin(ID_df2['ID'])
ID_df6['ID'].isin(ID_df2['ID']).value_counts(sort = True, dropna = False)
ID_df6['ID'].isin(ID_df2['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('FINAL_DEMOGRAPHICS : df6 Vs FINAL_K-5_SEL : df3')
print('Comparing FINAL_DEMOGRAPHICS with FINAL_K-5_SEL : 74.6% acc')
print("Comparing FINAL_DEMOGRAPHICS_UPDATE with FINAL_K-5_SEL : 74.61 % acc'")
ID_df6['ID'].isin(ID_df3['ID'])
ID_df6['ID'].isin(ID_df3['ID']).value_counts(sort = True, dropna = False)
ID_df6['ID'].isin(ID_df3['ID']).value_counts(sort = True, normalize = True, dropna = False)*100


print('FINAL_DEMOGRAPHICS : df6 Vs FINAL_GRADES')
print('Comparing FINAL_DEMOGRAPHICS with FINAL_GRADES : 24.9% acc')
print("Comparing FINAL_DEMOGRAPHICS_UPDATE with FINAL_GRADES  : 24.94 % acc'")
ID_df6['ID'].isin(ID_df4['ID'])
ID_df6['ID'].isin(ID_df4['ID']).value_counts(sort = True, dropna = False)
ID_df6['ID'].isin(ID_df4['ID']).value_counts(sort = True, normalize = True, dropna = False)*100


print('FINAL_DEMOGRAPHICS : df6 Vs FINAL_6-12_SEL')
print('Comparing FINAL_DEMOGRAPHICS with FINAL_6-12_SEL : 24.47% acc')
print("Comparing FINAL_DEMOGRAPHICS_UPDATE with FINAL_6-12_SEL : 24.48 % acc'")
ID_df6['ID'].isin(ID_df5['ID'])
ID_df6['ID'].isin(ID_df5['ID']).value_counts(sort = True, dropna = False)
ID_df6['ID'].isin(ID_df5['ID']).value_counts(sort = True, normalize = True, dropna = False)*100


print('FINAL_DEMOGRAPHICS : df6 Vs FINAL_FSAELA : df7')
print('Comparing FINAL_DEMOGRAPHICS with FINAL_FSAELA : 59.5% acc')
print('Comparing FINAL_DEMOGRAPHICS_UPDATE with FINAL_FSAELA : 59.6 % acc')
ID_df6['ID'].isin(ID_df7['ID'])
ID_df6['ID'].isin(ID_df7['ID']).value_counts(sort = True, dropna = False)
ID_df6['ID'].isin(ID_df7['ID']).value_counts(sort = True, normalize = True, dropna = False)*100


print('FINAL_DEMOGRAPHICS : df6 Vs FINAL_FSAMATH  : df8')
print('Comparing FINAL_DEMOGRAPHICS with FINAL_FSAMATH : 56.3% acc')
print('Comparing FINAL_DEMOGRAPHICS_UPDATE with FINAL_FSAMATH : 56.34 % acc')
ID_df6['ID'].isin(ID_df8['ID'])
ID_df6['ID'].isin(ID_df8['ID']).value_counts(sort = True, dropna = False)
ID_df6['ID'].isin(ID_df8['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('FINAL_DEMOGRAPHICS : df6 Vs FINAL_IREADY_ELA_DEM :df9')
print('Comparing FINAL_DEMOGRAPHICS with FINAL_IREADY_ELA_DEM : 73.38% acc')
print('Comparing FINAL_DEMOGRAPHICS_UPDATE with FINAL_IREADY_ELA_DEM : 73.39 % acc')
ID_df6['ID'].isin(ID_df9['ID'])
ID_df6['ID'].isin(ID_df9['ID']).value_counts(sort = True, dropna = False)
ID_df6['ID'].isin(ID_df9['ID']).value_counts(sort = True, normalize = True, dropna = False)*100


print('FINAL_DEMOGRAPHICS : df6 Vs FINAL_IREADY_MATH_DEM : df10')
print('Comparing FINAL_DEMOGRAPHICS with FINAL_IREADY_MATH_DEM : 74.41% acc')
print('Comparing FINAL_DEMOGRAPHICS_UPDATE with FINAL_IREADY_MATH_DEM : 74.41  % acc')
ID_df6['ID'].isin(ID_df10['ID'])
ID_df6['ID'].isin(ID_df10['ID']).value_counts(sort = True, dropna = False)
ID_df6['ID'].isin(ID_df10['ID']).value_counts(sort = True, normalize = True, dropna = False)*100






# =============================================================================
# Verify that the pseudo ID of SELWEB PBC EE versus each dataframe
# =============================================================================






print('1) SELWEB PBC versus all other datasets')

# Is the ID in ID_df0 in ID_df1?
print('SELWEB_PBC_EE_2018_19 : df0 = ', len(df0), 'obervations') 

print('This is for verification only')
ID_df0['ID'].isin(ID_df0['ID']) # All the IDs compared
ID_df0['ID'].isin(ID_df0['ID']).value_counts(sort = True, dropna = False) # Count of the common IDs
ID_df0['ID'].isin(ID_df0['ID']).value_counts(sort = True, normalize = True, dropna = False) # Count of the common IDs

# -----------------------------------------------------------------------------
print('SELWEB_PBC_LE_2018_19 : df1 =', len(df1), 'obervations') 
print('Acc = 0%')
ID_df0['ID'].isin(ID_df1['ID']) # All the IDs and the counts :
ID_df0['ID'].isin(ID_df1['ID']).value_counts(sort = True, dropna = False) # Count of the common IDs
ID_df0['ID'].isin(ID_df1['ID']).value_counts(sort = True, normalize = True, dropna = False) # Count of the common IDs


# -----------------------------------------------------------------------------
print('FINAL_DISCIPLINE : df2 =', len(df2), 'obervations') 
print('Acc = 8.49%')
ID_df0['ID'].isin(ID_df2['ID']) # All the IDs compared
ID_df0['ID'].isin(ID_df2['ID']).value_counts(sort = True, dropna = False) # Count of the common IDs
ID_df0['ID'].isin(ID_df2['ID']).value_counts(sort = True, normalize = True, dropna = False) # Count of the common IDs


# -----------------------------------------------------------------------------
print('FINAL_K-5_SEL : df3 =', len(df3), 'obervations') 
print('Acc = 100%')
ID_df0['ID'].isin(ID_df3['ID']) # All the IDs compared
ID_df0['ID'].isin(ID_df3['ID']).value_counts(sort = True, dropna = False) # Count of the common IDs
ID_df0['ID'].isin(ID_df3['ID']).value_counts(sort = True, normalize = True, dropna = False) # Count of the common IDs


# -----------------------------------------------------------------------------
print('FINAL_GRADES : df4 =', len(df4), 'obervations') 
print('Acc = 0%')
ID_df0['ID'].isin(ID_df4['ID']) # all the IDs compared
ID_df0['ID'].isin(ID_df4['ID']).value_counts(sort = True, dropna = False)
ID_df0['ID'].isin(ID_df4['ID']).value_counts(sort = True, normalize = True, dropna = False)


# -----------------------------------------------------------------------------
print('FINAL_6-12_SEL : df5 =', len(df5), 'obervations')
print('Acc = 0%') 
ID_df0['ID'].isin(ID_df5['ID'])
ID_df0['ID'].isin(ID_df5['ID']).value_counts(sort = True, dropna = False)
ID_df0['ID'].isin(ID_df5['ID']).value_counts(sort = True, normalize = True, dropna = False)

# -----------------------------------------------------------------------------
print('FINAL_DEMOGRAPHICS : df6 =', len(df6), 'obervations') 
print('Acc = 100%')
ID_df0['ID'].isin(ID_df6['ID'])
ID_df0['ID'].isin(ID_df6['ID']).value_counts(sort = True, dropna = False)
ID_df0['ID'].isin(ID_df6['ID']).value_counts(sort = True, normalize = True, dropna = False)

# -----------------------------------------------------------------------------
print('FINAL_FSAELA : df7 = ', len(df7), 'obervations')
print('Acc = 24.05%')
ID_df0['ID'].isin(ID_df7['ID'])
ID_df0['ID'].isin(ID_df7['ID']).value_counts(sort = True, dropna = False)
ID_df0['ID'].isin(ID_df7['ID']).value_counts(sort = True, normalize = True, dropna = False)

# -----------------------------------------------------------------------------
print('FINAL_FSAMATH : df8 =', len(df8), 'obervations') 
print('Acc = 24.12%')
ID_df0['ID'].isin(ID_df8['ID'])
ID_df0['ID'].isin(ID_df8['ID']).value_counts(sort = True, dropna = False)
ID_df0['ID'].isin(ID_df8['ID']).value_counts(sort = True, normalize = True, dropna = False)

# -----------------------------------------------------------------------------
print('FINAL_IREADY_ELA_DEM :df9 =', len(df9), 'obervations') 
print('Acc = 98.5%')
ID_df0['ID'].isin(ID_df9['ID'])
ID_df0['ID'].isin(ID_df9['ID']).value_counts(sort = True, dropna = False)
ID_df0['ID'].isin(ID_df9['ID']).value_counts(sort = True, normalize = True, dropna = False)

# -----------------------------------------------------------------------------
print('FINAL_IREADY_MATH_DEM : df10 =', len(df10), 'obervations')
print('Acc = 99.6%')
ID_df0['ID'].isin(ID_df10['ID'])
ID_df0['ID'].isin(ID_df10['ID']).value_counts(sort = True, dropna = False)
ID_df0['ID'].isin(ID_df10['ID']).value_counts(sort = True, normalize = True, dropna = False)


# =============================================================================
# Verify that the pseudo ID of SELWEB PBC LE - versus each dataframe
# =============================================================================
print('Is the ID in ID_df_df1 in all the other IDs?')
print('SELWEB_PBC_LE_2018_19 versus all others datasets')


# -----------------------------------------------------------------------------
print('SELWEB_PBC_LE_2018_19 : df1 =', len(df1), 'obervations')
print('This is for verifications purposes only.') 
ID_df1['ID'].isin(ID_df1['ID']) # All the IDs and the counts :
ID_df1['ID'].isin(ID_df1['ID']).value_counts(sort = True, dropna = False) # Count of the common IDs
ID_df1['ID'].isin(ID_df1['ID']).value_counts(sort = True, normalize = True, dropna = False) # Count of the common IDs

print('SELWEB_PBC_LE_2018_19 : df1 =', len(df1), 'obervations') 
print('Accuracy : 0%')
ID_df1['ID'].isin(ID_df0['ID']) # All the IDs compared
ID_df1['ID'].isin(ID_df0['ID']).value_counts(sort = True, dropna = False) # Count of the common IDs
ID_df1['ID'].isin(ID_df0['ID']).value_counts(sort = True, normalize = True, dropna = False) # Count of the common IDs

# -----------------------------------------------------------------------------
print('FINAL_DISCIPLINE : df2 =', len(df2), 'obervations')
print('Acc = 8.86%')
ID_df1['ID'].isin(ID_df2['ID']) # All the IDs compared
ID_df1['ID'].isin(ID_df2['ID']).value_counts(sort = True, dropna = False) # Count of the common IDs
ID_df1['ID'].isin(ID_df2['ID']).value_counts(sort = True, normalize = True, dropna = False) # Count of the common IDs


# -----------------------------------------------------------------------------
print('FINAL_K-5_SEL : df3 =', len(df3), 'obervations') 
print('This 100% accurate')
ID_df1['ID'].isin(ID_df3['ID']) # All the IDs compared
ID_df1['ID'].isin(ID_df3['ID']).value_counts(sort = True, dropna = False) # Count of the common IDs
ID_df1['ID'].isin(ID_df3['ID']).value_counts(sort = True, normalize = True, dropna = False) # Count of the common IDs


# -----------------------------------------------------------------------------
print('FINAL_GRADES : df4 =', len(df4), 'obervations')
print('accuracy :0.14%')
ID_df1['ID'].isin(ID_df4['ID']) # all the IDs compared
ID_df1['ID'].isin(ID_df4['ID']).value_counts(sort = True, dropna = False)
ID_df1['ID'].isin(ID_df4['ID']).value_counts(sort = True, normalize = True, dropna = False)


# -----------------------------------------------------------------------------
print('FINAL_6-12_SEL : df5 =', len(df5), 'obervations') 
print('accuracy : 0% acc')
ID_df1['ID'].isin(ID_df5['ID'])
ID_df1['ID'].isin(ID_df5['ID']).value_counts(sort = True, dropna = False)
ID_df1['ID'].isin(ID_df5['ID']).value_counts(sort = True, normalize = True, dropna = False)

# -----------------------------------------------------------------------------
print('FINAL_DEMOGRAPHICS : df6 =', len(df6), 'obervations') 
print('This is accurate')
ID_df1['ID'].isin(ID_df6['ID'])
ID_df1['ID'].isin(ID_df6['ID']).value_counts(sort = True, dropna = False)
ID_df1['ID'].isin(ID_df6['ID']).value_counts(sort = True, normalize = True, dropna = False)

# -----------------------------------------------------------------------------
print('FINAL_FSAELA : df7 = ', len(df7), 'obervations')
print('Comparing IDs SEL WEB LE with FINAL_FSAELA? 97.6%')
ID_df1['ID'].isin(ID_df7['ID']).iloc[0:50]
ID_df1['ID'].isin(ID_df7['ID']).value_counts(sort = True, dropna = False)
ID_df1['ID'].isin(ID_df7['ID']).value_counts(sort = True, normalize = True, dropna = False)

# -----------------------------------------------------------------------------
print('FINAL_FSAMATH : df8 =', len(df8), 'obervations') 
print('Comparing IDs SEL WEB LE with Final Math? 97.9% acc')
ID_df1['ID'].isin(ID_df8['ID']).iloc[0:50]
ID_df1['ID'].isin(ID_df8['ID']).value_counts(sort = True, dropna = False)
ID_df1['ID'].isin(ID_df8['ID']).value_counts(sort = True, normalize = True, dropna = False)

# -----------------------------------------------------------------------------
print('FINAL_IREADY_ELA_DEM :df9 =', len(df9), 'obervations') 
print('Comparing SEL WEB LE IDs with FINAL_IREADY_ELA_DEM ? 99.11% acc')
ID_df1['ID'].isin(ID_df9['ID'])
ID_df1['ID'].isin(ID_df9['ID']).value_counts(sort = True, dropna = False)
ID_df1['ID'].isin(ID_df9['ID']).value_counts(sort = True, normalize = True, dropna = False)

# -----------------------------------------------------------------------------
print('FINAL_IREADY_MATH_DEM : df10 =', len(df10), 'obervations')
print('Comparing SEL WEB LE IDs with FINAL_IREADY_MATH_DEM : 99.7% acc')
ID_df1['ID'].isin(ID_df10['ID'])
ID_df1['ID'].isin(ID_df10['ID']).value_counts(sort = True, dropna = False)
ID_df1['ID'].isin(ID_df10['ID']).value_counts(sort = True, normalize = True, dropna = False)


# =============================================================================
# 'FINAL_DISCIPLINE : df2 versus all others - versus each dataframe
# =============================================================================

# FINAL_DISCIPLINE versus all other
print('acc = 0%') 
ID_df2['ID'].isin(ID_df0['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 1.64%') 
ID_df2['ID'].isin(ID_df1['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 37.88%')
ID_df2['ID'].isin(ID_df3['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 61.36%')
ID_df2['ID'].isin(ID_df4['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 62.01%')
ID_df2['ID'].isin(ID_df5['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 100%')
ID_df2['ID'].isin(ID_df6['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 75.80%')
ID_df2['ID'].isin(ID_df7['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 73.13%')
ID_df2['ID'].isin(ID_df8['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 37.97%') 
ID_df2['ID'].isin(ID_df9['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc =41.10%') 
ID_df2['ID'].isin(ID_df10['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

# =============================================================================
# FINAL_K-5_SEL : df3 versus all others - versus each dataframe
# =============================================================================
# FINAL_K-5_SEL  versus all other

print('acc = 0%') 
ID_df3['ID'].isin(ID_df0['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 3.07%') 
ID_df3['ID'].isin(ID_df1['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 100%')
ID_df3['ID'].isin(ID_df3['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 1.15%')
ID_df3['ID'].isin(ID_df4['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 0%')
ID_df3['ID'].isin(ID_df5['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 100%')
ID_df3['ID'].isin(ID_df6['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 48.62%')
ID_df3['ID'].isin(ID_df7['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 48.66%')
ID_df3['ID'].isin(ID_df8['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 97.81%') 
ID_df3['ID'].isin(ID_df9['ID']).value_counts(sort = True, normalize = True, dropna = False)*100

print('acc = 98.02%') 
ID_df3['ID'].isin(ID_df10['ID']).value_counts(sort = True, normalize = True, dropna = False)*100
















ID_df2.isin(ID_df3)
ID_df2.isin(ID_df4)
ID_df2.isin(ID_df5)
ID_df2.isin(ID_df6)
ID_df2.isin(ID_df7)
ID_df2.isin(ID_df8)
ID_df2.isin(ID_df9)
ID_df2.isin(ID_df10)

