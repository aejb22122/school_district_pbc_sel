
# -*- coding: utf-8 -*-
"""
Created on Fri Feb 17 15:29:03 2023

@author: ajeanbaptiste
"""

#!/usr/bin/env python
# coding: utf-8

# # 2022 PT District data - data management
# 
# ## First part of the data management :
# * the aggreation of the variables 
# * Standardization of the variables
# * grouped by Programs 
# * and exported to excel.
# 
# 
# This is the new data management processs based on the recommandations of Stephen Peck <link@umich.edu> the PT consultant.


# In[2]:
import numpy as np
import pandas as pd
from pandas import Series, DataFrame
import seaborn as sns  # for plots
import matplotlib.pyplot as plt  # for plots
import statsmodels.formula.api as smf  # statsmodels
import statsmodels.stats.multicomp as multi  # statsmodels and posthoc test
import statsmodels.api as sm  # Statsmodel for the qqplots
import scipy.stats  # For the Chi-Square test of independance

import statsmodels.api as sm
from statsmodels.formula.api import ols

# Machine learning libraries

# For the LASSO and PCA
from sklearn import preprocessing
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.linear_model import LassoLarsCV

import os
#sns.set(style="darkgrid")
sns.set_theme(style="whitegrid")

from datetime import datetime

# In[3]:


# Suppress scientific notation
np.set_printoptions(suppress=True)

# Display all the rows and columns
pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)

#pd.options.display.float_format = '{:.00f}'.format

# # Final demographics data 
# We are using the updated version of the democraphics data provided by the SD 3/24/2022
# 
# We are also using the list from Thu 4/21/2022 3:11 PM. For any program that is NOT highlighted, their youth should be removed from the dataset.

# In[4]:

df = pd.read_excel('FINAL_DEMOGRAPHICS_UPDATE - Copy.xlsx') 


# In[5]:


len(df)
df['STU_GENDER'].value_counts(sort=True, dropna = False)
df['STU_GENDER'].value_counts(sort=True, dropna = False, normalize=True)

# In[8]:


df['SiteName'].value_counts(sort = True, dropna=False)

# In[9]:

# =============================================================================
# 
# # FINAL_GRADES
# # 
# # This file contains final course grades for students. Join this file to the FINAL_DEMOGRAPHICS file to identify individual students. This file is not one to one.
# 
# =============================================================================

# Importing dataset
final_grades = pd.read_excel('FINAL_GRADES.xlsx')


# In[10]:


final_grades.head()


# In[11]:


final_grades.columns


# In[12]:


len(final_grades)


# ###  !We will merge the final grades data with the demographics here before the aggregations to keep the PSEUDOIDs unchanged.

# In[13]:


df[['PSEUDOID', 'SiteName', 'District Site']].groupby('District Site').count()


# # Merging Final grades with demographics data using the PSEUDOIDs

# In[14]:


final_grades['PSEUDOID'].isin(df['PSEUDOID']).value_counts(sort = True, normalize = True, dropna = False)*100


# In[15]:


df['PSEUDOID'].isin(final_grades['PSEUDOID']).value_counts(sort = True, normalize = True, dropna = False)*100


# In[16]:
# -----------------------------------------------------------------------------
print('FINAL_DEMOGRAPHICS_UPDATE : df =', len(df), 'obervations')
print("Final grades  =", len(final_grades), "observations") 
print('Acc = 24.94% of demographics is in the final grades data.')
print('Acc = 100 % of final grades data is in the demographics data.')

print("This is an exemple of a many-to-one join : the data in df and final_grades have multiple PseudoID with the same ids.")


# In[17]:


#final_grades_with_programs  = final_grades.merge(df, how ='outer', on = ['PSEUDOID'], indicator=True) # It's the same thing, but we just what to identify the left and right datasets in the indicators column.
#final_grades_with_programs  = pd.merge(final_grades, df, how = 'outer', on = ['PSEUDOID'], indicator = True)

final_grades_with_programs  = pd.merge(df, final_grades,  how = 'outer', on = ['PSEUDOID'], indicator = True)
print("The 'outer' join use all key combinations observed in both tables together; for Final demographics U Final grades.")


# -----------------------------------------------------------

# ## Cleaning un used defined variables to save space

# In[18]:


del final_grades 
del df


# -------------------------------------

# In[20]:


len(final_grades_with_programs)
final_grades_with_programs.columns

final_grades_with_programs['_merge'].value_counts(sort = True, dropna = False)

# In[21]:


final_grades_with_programs.head()


# In[22]:

final_grades_with_programs['_merge'].value_counts(sort=True, dropna=False)

# In[23]:


# len(final_grades)+len(df)


# In[24]:


final_grades_with_programs.describe()


# In[25]:


final_grades_with_programs.columns


# In[26]:


final_grades_with_programs['District Site'].value_counts(sort=True, dropna=False)


# In[27]:


final_grades_with_programs['FNL_GRD'].value_counts(sort=True, dropna=False)


# ## Transforming the letter Grades to Grade Point Equivalents
# 

# In[28]:


def final_grades(row):
  """
  This is to convert the grades
  """
    if row['FNL_GRD'] == 'A':
        return 4.0
    if row['FNL_GRD'] == 'B':
        return 3.0
    if row['FNL_GRD'] == "C":
        return 2.0
    if row['FNL_GRD'] == "D":
        return 1
    if row['FNL_GRD'] == "F":
        return 0
    else:
        return np.nan

#%%

final_grades_with_programs['final_grades'] = final_grades_with_programs.apply(lambda row: final_grades(row), axis = 1) # type: ignore


# In[30]:


final_grades_with_programs['final_grades'].value_counts(sort = True, dropna = False)

final_grades_with_programs['SiteName'].value_counts(sort = True, dropna = False)

# In[31]:

final_grades_with_programs.columns
final_grades_with_programs.tail()


# ### Cleaning the site names
# **Cleaning ... We will remove the extra spaces in all the SiteNames to permit the siteName to be converted to OrgID later ...**

# In[32]:


final_grades_with_programs['SiteName'][6498]


# In[33]:


# Using string assessors - right strip on the series
column_to_strip = final_grades_with_programs['SiteName'].str.rstrip()


# In[34]:


final_grades_with_programs['SiteName'] = final_grades_with_programs['SiteName'].str.rstrip()


# In[35]:


# Verifications ...
final_grades_with_programs['SiteName'][6498]


# In[36]:


final_grades_with_programs['SiteName'].value_counts(sort=True, dropna=False)


# **Getting the orgID from the siteNames :**

# In[37]:


# These are from the list confirmed in the email (From: Celine Provini <cprovini@primetimepbc.org>
#Sent: Thursday, April 21, 2022 3:11 PM
#To: Annick Eudes Jean-Baptiste <ajeanbaptiste@primetimepbc.org>
#Subject: list of programs for district analysis)

def orgID_final_grades_with_programs(row):
    if row['SiteName'] == 'Bak Middle School Of The Arts':
        return 'ORG-00141'      
    if row['SiteName'] == 'Sunset Palms Elementary':
        return 'ORG-00476'
    if row['SiteName'] == 'Verde Elementary':
        return 'ORG-00408' # Is refered to Verde K-8 Afterschool Program in salesforce
    if row['SiteName'] == 'Morikami Park Elementary':
        return 'ORG-00392' # Is called Morikami Park Elementary Afterschool Program in salesforce
    if row['SiteName'] == 'Citrus Cove Elementary':
        return 'ORG-00473'
    if row['SiteName'] == 'Berkshire Elementary':
        return 'ORG-00049'
    if row['SiteName'] == 'Discovery Key Elementary':
        return 'ORG-00257'
    if row['SiteName'] == 'Beacon Cove Intermediate':
        return 'ORG-00107'
    if row['SiteName'] == 'The Conservatory School North':
        return 'ORG-00286'
    if row['SiteName'] == 'Del Prado Elementary':
        return 'ORG-00450'
    if row['SiteName'] == 'Boys & Girls Club - Max M Fisher':
        return 'ORG-00463'
    if row['SiteName'] == 'Everglades Preparatory Academy':
        return np.nan # Removed Is refered to Everglades Elementary Afterschool Program in salesforce 'ORG-00290'
    if row['SiteName'] == 'J C Mitchell Elementary':
        return 'ORG-00198' # Is refered to J.C. Mitchell Elementary Afterschool Program
    if row['SiteName'] == 'Palm Beach Gardens Elementary':
        return 'ORG-00035' # Is refered to Palm Beach Gardens Elementary Afterschool Program in salesforce
    if row['SiteName'] == 'Crystal Lakes Community Elem':
        return 'ORG-00390' # Is refered to Crystal Lakes Elementary Afterschool Program. Maybe I will remove it later ... ?
    if row['SiteName'] == 'Royal Palm Beach Elementary':
        return 'ORG-00071'
    if row['SiteName'] == 'H L Johnson Elementary':
        return 'ORG-00033'
    if row['SiteName'] == 'Sunrise Park Elementary':
        return 'ORG-00157'
    if row['SiteName'] == 'Allamanda Elementary':
        return 'ORG-00043' # Is refered to Allamanda Elementary Afterschool Program
    if row['SiteName'] == "Faith's Place Center for Arts Education, Inc.":
        return 'ORG-00539'
    if row['SiteName'] == 'Grassy Waters Elementary':
        return 'ORG-00258' # is refered to Grassy Waters Elementary Afterschool Program in salesforce
    if row['SiteName'] == 'Palm Beach Public':
        return 'ORG-00190' # Is refered to Palm Beach Public Afterschool Program in salesforce
    if row['SiteName'] == 'Boys & Girls Club - Marjorie S. Fisher':
        return 'ORG-00462'
    if row['SiteName'] == 'Freedom Shores Elementary':
        return 'ORG-00250'
    if row['SiteName'] == 'Galaxy Elementary':
        return 'ORG-00138' # Is refered to Galaxy E3 Afterschool Enrichment Program in salesforce
    if row['SiteName'] == 'Boys & Girls Club - Florence DeGeorge':
        return 'ORG-00458'
    if row['SiteName'] == 'Golden Grove Elementary':
        return 'ORG-00379'
    if row['SiteName'] == 'Bright Futures Child Development Center, Inc.':
        return 'ORG-00484'
    if row['SiteName'] == 'C O Taylor Kirklane Elementary':
        return 'ORG-00304' # Clifford O. Taylor Kirklane Elementary Afterschool Program
    if row['SiteName'] == 'Hammock Pointe Elementary':
        return 'ORG-00474' # Hammock Pointe Elementary Afterschool Program
    if row['SiteName'] == 'New Horizons Elementary':
        return 'ORG-00100' # New Horizons Elementary Afterschool Program in salesforce
    if row['SiteName'] == 'City of West Palm Beach - Gaines Park Community Center':
        return 'ORG-00111'
    if row['SiteName'] == 'Frontier Elementary':
        return 'ORG-00414' # Frontier Elementary Afterschool Program in salesforce
    if row['SiteName'] == 'North Grade Elementary':
        return 'ORG-00470'
    if row['SiteName'] == 'All About Kids':
        return 'ORG-00544' # There are 3 All about kids in salesforce
    if row['SiteName'] == 'Little Dude Ranch Academy':
        return 'ORG-00338'
    if row['SiteName'] == 'Achievement Centers for Children and Families Morton Downey Family Resource Center':
        return 'ORG-00364'
    if row['SiteName'] == 'Diamond View Elementary':
        return 'ORG-00354' # Refered to Diamond View Elementary Afterschool Program in salesforce
    if row['SiteName'] == 'Poinciana Elementary':
        return 'ORG-00077' # Refered to Poinciana Elementary Afterschool Program
    if row['SiteName'] == 'Boys & Girls Club - Neil S. Hirsch Family':
        return 'ORG-00467'
    if row['SiteName'] == 'Cypress Trails Elementary':
        return 'ORG-00098' # Cypress Trails Elementary Afterschool Program
    if row['SiteName'] == 'Planet Kids - West Palm Beach':
        return 'ORG-00736'
    if row['SiteName'] == 'S D Spady Elementary':
        return 'ORG-00479'
    if row['SiteName'] == "Children's Academy of Lake Worth":
        return 'ORG-00376'
    if row['SiteName'] == "Seminole Trails Elementary":
        return 'ORG-00291'
    if row['SiteName'] == "Forest Hill Elementary":
        return 'ORG-00365'
    if row['SiteName'] == 'Achievement Centers for Children and Families Village Academy':
        return 'ORG-00284'
    if row['SiteName'] == 'Crosspointe Elementary':
        return 'ORG-00234'
    if row['SiteName'] == 'Egret Lake Community Elementar':
        return np.nan # REMOVED - Egret Lake Community Elementar 
    if row['SiteName'] == 'For The Children, Inc. at Barton Elementary':
        return 'ORG-00133'
    if row['SiteName'] == 'City of Greenacres Youth Programs - C.A.R.E.S.':
        return 'ORG-00335'
    if row['SiteName'] == 'Pahokee Youth Enrichment Academy':
        return 'ORG-00368'
    if row['SiteName'] == 'Plumosa School Of The Arts':
        return 'ORG-00200'
    if row['SiteName'] == 'U B Kinsey Palmview Elementary':
        return 'ORG-00451'
    if row['SiteName'] == 'Jupiter Elementary':
        return 'ORG-00163'
    if row['SiteName'] == 'Heritage Elementary':
        return 'ORG-00343'
    if row['SiteName'] == 'New Hope Charities, Inc.':
        return 'ORG-00440'
    if row['SiteName'] == 'Greenacres Elementary':
        return 'ORG-00288'
    if row['SiteName'] == 'Palm Beach Maritime Academy':
        return 'ORG-00445'
    if row['SiteName'] == 'South Olive Elementary':
        return 'ORG-00429'
    if row['SiteName'] == 'Boys & Girls Club - Gove Elementary':
        return 'ORG-00461'
    if row['SiteName'] == 'Dwight D Eisenhower Elementary':
        return 'ORG-00223'
    if row['SiteName'] == 'Cholee Lake Elementary':
        return 'ORG-00413'
    if row['SiteName'] == 'Kids-R-Kreative Learning Center Inc.':
        return 'ORG-00215'
    if row['SiteName'] == 'Starlight Cove Elementary':
        return 'ORG-00397' # Is refered to Starlight Cove Elementary Afterschool Program in salesforce
    if row['SiteName'] == 'Loxahatchee Groves Elementary':
        return 'ORG-00127'
    if row['SiteName'] == 'Boys & Girls Club - Belle Glade Elementary':
        return 'ORG-00454' # Verify if there are duplicates in the orgIDs
    if row['SiteName'] == 'Rolling Green Elementary':
        return 'ORG-00362' # Rolling Green Elementary Afterschool Program
    if row['SiteName'] == 'Kids at Work Learning Center':
        return 'ORG-00512'
    if row['SiteName'] == 'Boys & Girls Club - Belle Glade Teen Center':
        return 'ORG-00455' # is Boys & Girls Club - Smith & Moore Family Teen Center in salesforce
    if row['SiteName'] == 'FAU/Pine Jog Afterschool':
        return 'ORG-00399'
    if row['SiteName'] == 'Palm Springs Elementary':
        return 'ORG-00037' # is Palm Springs Elementary Afterschool Program in Salesforce
    if row['SiteName'] == 'Tiny Tikes Academy - Boynton Beach':
        return 'ORG-00815'
    if row['SiteName'] == 'West Jupiter Community Group, Inc.':
        return 'ORG-00433'
    if row['SiteName'] == 'The Salvation Army Northwest Community Center Afterschool Program':
        return 'ORG-00383'
    if row['SiteName'] == 'Florence Fuller Child Development Center - West':
        return 'ORG-00040'
    if row['SiteName'] == 'Hope Centennial Elementary':
        return 'ORG-00358' # Is Hope Centennial Elementary Afterschool Program in salesforce
    if row['SiteName'] == 'Lantana Elementary':
        return 'ORG-00428'
    if row['SiteName'] == 'Orthodox Zion Child Development Center':
        return 'ORG-00222'
    if row['SiteName'] == 'Lake Park Elementary':
        return 'ORG-00292'
    if row['SiteName'] == 'Pioneer Park Youth Enrichment Academy':
        return 'ORG-00277'
    if row['SiteName'] == 'South Grade Elementary':
        return 'ORG-00431' # Is South Grade Elementary Afterschool Program in Salesforce
    if row['SiteName'] == 'Forest Park Elementary':
        return 'ORG-00075' # Is Forest Park Elementary Afterschool Program in salesforce
    if row['SiteName'] == 'Boys & Girls Club - Naoma Donnelley Haggin':
        return 'ORG-00464'
    if row['SiteName'] == 'Benoist Farms Elementary':
        return 'ORG-00143' # Is Benoist Farms Elementary Afterschool Program
    if row['SiteName'] == 'Florence Fuller Child Development Center - East':
        return 'ORG-00162'
    if row['SiteName'] == 'Westward Elementary':
        return 'ORG-00056'
    if row['SiteName'] == 'Grove Park Elementary':
        return 'ORG-00472' # Is Grove Park Elementary Afterschool Program
    if row['SiteName'] == 'University Learning Academy':
        return 'ORG-00063'
    if row['SiteName'] == 'Belvedere Elementary':
        return 'ORG-00228' # Is Belvedere Elementary Afterschool Program
    if row['SiteName'] == 'Boca Raton Elementary':
        return 'ORG-00042' # Is Boca Raton Elementary Afterschool Program
    if row['SiteName'] == 'Adopt-A-Family of the Palm Beaches Inc. - Project Grow':
        return 'ORG-00137'
    if row['SiteName'] == 'Highland Elementary':
        return 'ORG-00331'
    if row['SiteName'] == "The King's Learning Center":
        return 'ORG-00038'
    if row['SiteName'] == 'The Guatemalan Maya Center Inc. - Highland':
        return 'ORG-00053'
    if row['SiteName'] == 'Renaissance Charter School at Wellington':
        return 'ORG-00703'
    if row['SiteName'] == 'Boys & Girls Club - Glade View Elementary':
        return 'ORG-00460'
    if row['SiteName'] == 'Indian Pines Elementary':
        return 'ORG-00386'
    if row['SiteName'] == 'City of West Palm Beach - South Olive Park Community Center':
        return 'ORG-00253'
    if row['SiteName'] == 'Pahokee Deliverance Christian Center':
        return 'ORG-00534'
    if row['SiteName'] == 'Kingswood Academy of Palm Springs':
        return 'ORG-00879'
    if row['SiteName'] == 'Safe Haven Community Resource Center':
        return 'ORG-00202'
    if row['SiteName'] == 'Orchard View Community Element':
        return np.nan
    if row['SiteName'] == 'Northmore Elementary':
        return 'ORG-00295'
    if row['SiteName'] == 'The Guatemalan Maya Center Inc. - South Grade':
        return 'ORG-00432'
    if row['SiteName'] == 'West Gate Elementary':
        return 'ORG-00115'
    if row['SiteName'] == 'Fannie Mae Tots Daycare Center':
        return 'ORG-00131'
    if row['SiteName'] == 'Creative Learning Experience':
        return 'ORG-00273'
    if row['SiteName'] == 'City of West Palm Beach Parks & Recreation - Howard Park Community Center':
        return 'ORG-00093'
    if row['SiteName'] == 'Boys & Girls Club - Boca Raton':
        return 'ORG-00456'
    if row['SiteName'] == 'Boys & Girls Club - Canal Point Elementary School':
        return 'ORG-00457'
    if row['SiteName'] == 'Milagro Center':
        return 'ORG-00249'
    if row['SiteName'] == 'Kingswood Academy of Greenacres':
        return 'ORG-00801'  
    if row['SiteName'] == 'Achievement Centers for Children and Families at Pine Grove Elementary School':
        return 'ORG-00680'
    if row['SiteName'] == 'Boca Raton Housing Authority - Pearl City CATS':
        return 'ORG-00099'
    if row['SiteName'] == 'Boys & Girls Club - Pioneer Park Elementary School':
        return 'ORG-00465'
    if row['SiteName'] == 'City of Pahokee Parks & Recreation Afterschool Program Middle School':
        return 'ORG-00784'
    if row['SiteName'] == 'Kingswood Academy of Lake Worth':
        return 'ORG-00985'
    if row['SiteName'] == 'Boys & Girls Club - Rosenwald/South Bay Elementary':
        return 'ORG-00466'
    if row['SiteName'] == 'City of West Palm Beach - Coleman Park Community Center':
        return 'ORG-00059' 
    if row['SiteName'] == 'Lincoln Elementary':
        return 'ORG-00067' # Is Lincoln Elementary Afterschool Program
    if row['SiteName'] == 'City of Delray Beach Parks & Recreation Department - Pompey Park':
        return 'ORG-00328' 
    if row['SiteName'] == 'Western Academy Charter School':
        return 'ORG-00731'
    if row['SiteName'] == 'Sacred Heart Afterschool Program':
        return 'ORG-00113'
    if row['SiteName'] == 'City of Delray Beach Parks & Recreation Department Community Center - Department of Out of School Programs':
        return 'ORG-00327'
    if row['SiteName'] == 'Faith Lutheran School':
        return 'ORG-00603'
    if row['SiteName'] == "Faith's Place Middle School":
        return 'ORG-00603'
    if row['SiteName'] == 'The Center for Youth Activity':
        return 'ORG-00488'
    if row['SiteName'] == 'Hidden Oaks Elementary':
        return 'ORG-00443' # Is Hidden Oaks Elementary Afterschool Program in Salesforce
    if row['SiteName'] == 'Urban Youth Impact - Elementary':
        return 'ORG-00513'
    if row['SiteName'] == 'Hagen Road Elementary':
        return 'ORG-00046'
    else:
        return np.nan
                                                                                                
#Western Academy Charter 


final_grades_with_programs['ORG_ID'] = final_grades_with_programs.apply(lambda row: orgID_final_grades_with_programs (row), axis= 1) # type: ignore

#%%
final_grades_with_programs['ORG_ID'].value_counts(sort=True, dropna = False)
final_grades_with_programs['SiteName'].value_counts(sort=True, dropna = False)
#%%
final_grades_with_programs['_merge'].value_counts(sort = True, dropna = False)


# In[41]:

# =============================================================================
#  Adding the standardized scores FINAL_FSAELA
# =============================================================================

# 
# This file contains scale scores and FSA levels for the FSAELA test. 
# Both enrolled grades and test grade levels are included in this file. Join this file to the FINAL_DEMOGRAPHICS file to identify individual students.

FINAL_FSAELA = pd.read_excel("FINAL_FSAELA.xlsx")


# In[42]:


## Merging
print(' This file contains scale scores and FSA levels for the FSAELA test =', len(FINAL_FSAELA), 'obervations')


# In[43]:


#FINAL_FSAELA.columns


# In[44]:


FINAL_FSAELA = FINAL_FSAELA.rename(columns={'PSUEDOID' : 'PSEUDOID'})


# In[45]:


#final_grades_with_programs.columns


# In[46]:


## Merging
#print('PQA data Prime Time : pqa =', len(pqa), 'obervations')
#print("Final grades + programs =", len(final_grades_with_programs), "observations") 
#print('Acc = 24.94% of demographics is in the final grades data.')
#print('Acc = 100 % of final grades data is in the demographics data.')


# In[47]:


#FINAL_FSAELA['PSEUDOID'].isin(final_grades_with_programs['PSEUDOID']).value_counts(sort = True, normalize = True, dropna = False)*100


# In[48]:


#final_grades_with_programs['PSEUDOID'].isin(FINAL_FSAELA['PSEUDOID']).value_counts(sort = True, normalize = True, dropna = False)*100


# In[49]:
# Let remove the indicator columns
final_grades_with_programs=final_grades_with_programs.drop(['_merge'], axis=1)
# MERGING ...
final_grades_with_programs_fsaela  = pd.merge(final_grades_with_programs, FINAL_FSAELA,  how = 'outer', on = ['PSEUDOID'], indicator=True)


# In[50]:


len(final_grades_with_programs_fsaela)


# In[51]:


final_grades_with_programs_fsaela['_merge'].value_counts(sort = True, dropna=False)


# # Cleaning ...

# In[52]:


# Let remove the indicator columns
final_grades_with_programs_fsaela=final_grades_with_programs_fsaela.drop(['_merge'], axis=1)

#%%
del column_to_strip
del final_grades # type function
del FINAL_FSAELA
del final_grades_with_programs
del orgID_final_grades_with_programs # type function


#%%
# =============================================================================
# Adding the FINAL_FSAMATH
# =============================================================================
# This file contains scale scores and FSA levels for the FSAMATH test. Both enrolled grades and test grade levels are included in this file. Join this file to the FINAL_DEMOGRAPHICS file to identify individual students.

FINAL_FSAMATH = pd.read_excel('FINAL_FSAMATH.xlsx')


# In[57]:


#FINAL_FSAMATH.columns


# In[58]:


FINAL_FSAMATH = FINAL_FSAMATH.rename(columns={'PSUEDOID' : 'PSEUDOID'})


# In[59]:


# FINAL_FSAMATH['PSEUDOID'].isin(final_grades_with_programs_fsaela['PSEUDOID']).value_counts(sort = True, normalize = True, dropna = False)*100

len(FINAL_FSAMATH)


# final_grades_with_programs_fsaela['PSEUDOID'].isin(FINAL_FSAMATH['PSEUDOID']).value_counts(sort = True, normalize = True, dropna = False)*100


# # In[61]:

# =============================================================================
# MERGING 
# =============================================================================

#final_grades_with_programs_fsaela  = pd.merge(final_grades_with_programs, FINAL_FSAELA,  how = 'outer', on = ['PSEUDOID'], indicator=True)
final_grades_with_programs_fsaela_fsamath = pd.merge(final_grades_with_programs_fsaela, FINAL_FSAMATH, how='outer', on=['PSEUDOID'], indicator=True)


# # In[62]:


len(final_grades_with_programs_fsaela_fsamath)


# # In[63]:


final_grades_with_programs_fsaela_fsamath['_merge'].value_counts(sort=True, dropna=False)


# # # Cleaning

# # In[64]:

del FINAL_FSAMATH
del final_grades_with_programs_fsaela


# # Adding the PQA scores
# In[39]:
    
# =============================================================================
#  Adding the PQA scores
# =============================================================================

# In[66]:
#pqa = pd.read_excel("2022_02_22_Program_ORGID_zipcode.xlsx")
pqa = pd.read_excel("2023_02_13_Program_ORGID_zipcodeREVISED.xlsx")


pqa.columns


# In[68]:


len(pqa)


# In[69]:


pqa.describe()


# In[70]:


pqa['Organization Need Level'].value_counts(sort = True, dropna = False)


# In[71]:


pqa['Organization Need Level'].value_counts(sort = True, dropna = False, normalize=True)


# In[72]:


pqa['Account Name'].value_counts(sort = True, dropna = False, normalize=True)


#%%
# Creating a filter for the pqa scores that are not null ...
not_empty_pqa_score = pqa['Form A Scale Score'].notna() # 

#%%
pqa = pqa[not_empty_pqa_score]


pqa['Organization Need Level'].value_counts(sort = True, dropna = False)



pqa['Organization Need Level'].value_counts(sort = True, dropna = False, normalize=True)




# In[75]:

pqa = pqa.rename(columns={'Organization ID Number': 'ORG_ID'})
#%%
# Program Quality Scale 
# A PBC-PQA score between 3.4 and 4.0 was considered “satisfactory” quality, 
# while a score of 4.1 or higher was considered “high” quality. 

# def program_quality_scale(row):
#     if  row['Form A Scale Score'] >=4.1:
#         return "high quality"
#     if  row['Form A Scale Score'] >= 3.4 and  row['Form A Scale Score'] <=4.0:
#         return "satisfactory"
#     if row['Form A Scale Score'] <=3.4:
#         return "Low quality"
#     else:
#         return "Satisfactory2"

    

# pqa['pqa_scores_scale'] = pqa.apply(lambda row: program_quality_scale(row), axis = 1)

# pqa['pqa_scores_scale'].value_counts(sort = True, dropna = False)
# pqa['pqa_scores_scale'].value_counts(sort = True, dropna = False, normalize=True)

# In[]:
# Removing the _merge columns
final_grades_with_programs_fsaela_fsamath = final_grades_with_programs_fsaela_fsamath.drop(['_merge'], axis=1)





#%%
# MERGING 
PT_School_District_data_set = pd.merge(final_grades_with_programs_fsaela_fsamath, pqa,  how = 'outer', on = ['ORG_ID'], indicator=True)


#%%
len(PT_School_District_data_set)

PT_School_District_data_set.columns

PT_School_District_data_set['_merge'].value_counts(sort = True, dropna = False)
#%%
# Let's see in the dataset from the right_only = 25 we had after the full merge
filter_right_only = PT_School_District_data_set['_merge'] == 'right_only'
right_only_df = PT_School_District_data_set[filter_right_only]
a_df = right_only_df[['ORG_ID', 'Account Name']]


#%%
# =============================================================================
# Cleaning the demographics
# =============================================================================
PT_School_District_data_set.head()

# Student's age
# =============================================================================
PT_School_District_data_set['STU_BIRTH_DT'][0]
PT_School_District_data_set['STU_BIRTH_DT'][100]

# column_to_strip = df['STU_BIRTH_DT'].str.split("T")
column_to_strip = PT_School_District_data_set['STU_BIRTH_DT'].str.split("-")
PT_School_District_data_set['date_of_birth'] = column_to_strip.str[0]

# Verifications...
PT_School_District_data_set['date_of_birth'][100]
PT_School_District_data_set['date_of_birth'][0:10]

# convert column to numaric
PT_School_District_data_set['date_of_birth'] = pd.to_numeric(PT_School_District_data_set['date_of_birth'])

YEAR = 2019
PT_School_District_data_set['age'] = YEAR-PT_School_District_data_set['date_of_birth']

PT_School_District_data_set['age'].value_counts(sort=True, dropna=False)
PT_School_District_data_set.groupby('age')['PSEUDOID'].count()


# Elementary school is kindergarten through 5th grade (ages 5-10)
# Delete the youth age = 3
#df[df.age == 3]

#df=df.drop(df.index[3726])
PT_School_District_data_set=PT_School_District_data_set.loc[(PT_School_District_data_set['age']<=14) & (PT_School_District_data_set['age']>3)]

#PT_School_District_data_set=PT_School_District_data_set.loc[(PT_School_District_data_set['age']>3)]

# Verifications ...
PT_School_District_data_set['age'].min()
PT_School_District_data_set['age'].max()
PT_School_District_data_set['age'].hist()

PT_School_District_data_set['age'].value_counts(sort=True, dropna=False)
PT_School_District_data_set['age'].value_counts(sort=True, dropna=False, normalize=True)

len(PT_School_District_data_set)







#%%
# =============================================================================
# DATA ANALYSIS
# =============================================================================

#%%
# cleaning ...pqa
# %who
del not_empty_pqa_score, final_grades_with_programs_fsaela_fsamath, YEAR, column_to_strip

# In[79]:


len(PT_School_District_data_set)


# In[80]:


PT_School_District_data_set['_merge'].value_counts(sort=True, dropna=False)


# In[81]:


print(len(PT_School_District_data_set), "==> If there are multiple matches between x and y, all combinations of the matches are returned.")


# In[82]:


PT_School_District_data_set.columns


# In[83]:


PT_School_District_data_set = PT_School_District_data_set.rename(columns={'Form A Scale Score' : 'pqa_score',
                           'QIS Level' : 'qis_level',
                           'Organization Need Level' : 'org_need_level'
                           })


# In[84]:


PT_School_District_data_set['qis_level'].value_counts(sort=True, dropna=True)


# ### --Identify variables in "base model" and ensure the theory of change diagram reflects this, then identify variables in a few alternate models 
# (e.g. models where sample is limited to special populations such as high community need level, student SEL concerns present, lower-achieving students, community-based programs, etc.)

# In[85]:


PT_School_District_data_set.head()


# In[86]:


PT_School_District_data_set.describe()


# In[]:
# =============================================================================
# EXPORTING THE RESULTS OF ALL THE MERGES
# =============================================================================
PT_School_District_data_set.to_excel("FEB_24_2023_PT_School_District_data_set.xlsx")
# In[89]:

    


# =============================================================================
# Second part of the analysis import the managed data and start here
# Import the required libraries also!!!
# =============================================================================

PT_School_District_data_set = pd.read_excel("FEB_24_2023_PT_School_District_data_set.xlsx") 
#%%


PT_School_District_data_set['qis_level'].value_counts(sort=True, dropna=True)
PT_School_District_data_set['qis_level'].value_counts(sort=True, dropna=True, normalize = True)

# ## Exporting the final dataset

# In[90]:


# PT_School_District_data_set.to_excel("2023_02_03_PT_School_District_data_set.xlsx")


# # Table 1. Descriptive Statistics for Data Analytic Variables 

# In[91]:


PT_School_District_data_set.columns


# In[92]:


PT_School_District_data_set['SiteType'].value_counts(sort=True, dropna=False)


# In[93]:


#adataset = PT_School_District_data_set[['final_grades', 'pqa_score', 'qis_level', 'org_need_level', 'SCALESCORE_x']]


# In[94]:


#adataset.describe()


# ## Youth's Grades

# In[95]:




#%%

PT_School_District_data_set.columns

# =============================================================================
# NUMBER OF YOUTHS
# =============================================================================
len(PT_School_District_data_set['PSEUDOID'].value_counts(sort=True, dropna=False))

PT_School_District_data_set.groupby('PSEUDOID').count()

# =============================================================================
# Grades
# =============================================================================


#Grouping and perform count over each group
#PT_School_District_data_set.groupby('PSEUDOID')['Enrolled_GRADE_x'].count()

# PT_School_District_data_set.groupby('Enrolled_GRADE_x')['PSEUDOID'].count()

# PT_School_District_data_set.groupby('Enrolled_GRADE_y')['PSEUDOID'].count()

# PT_School_District_data_set.groupby('Enrolled_GRADE_x')['PSEUDOID'].value_counts(normalize = True)

# PT_School_District_data_set.groupby('Enrolled_GRADE_x')['PSEUDOID'].count()/()

# =============================================================================
# GENDER
# =============================================================================

PT_School_District_data_set.groupby('STU_GENDER')['PSEUDOID'].count()


#Group by two keys and then summarize each group
# students = PT_School_District_data_set.groupby(['Enrolled_GRADE_x', 'PSEUDOID'], as_index=False).count()

# len(PT_School_District_data_set)-(10864+10203)


# =============================================================================
# Ethnicity
# =============================================================================
# type(PT_School_District_data_set[ 'STU_BIRTH_DT'][1])

PT_School_District_data_set.groupby('STU_ETHNICITY')['PSEUDOID'].count()


# # =============================================================================
# # AGE
# # =============================================================================

# # Using string assessors - right strip on the series
# PT_School_District_data_set[ 'STU_BIRTH_DT'][0]
# column_to_strip = PT_School_District_data_set[ 'STU_BIRTH_DT'].str.split('-')


# #PT_School_District_data_set['STU_BIRTH_DT'] = PT_School_District_data_set[ 'STU_BIRTH_DT'].str.partition('-')

# PT_School_District_data_set['age'] = column_to_strip.str[0]


# PT_School_District_data_set = PT_School_District_data_set.rename(columns={'age' : 'birth_year'})

# # convert column "a" of a DataFrame
# PT_School_District_data_set['birth_year'] = pd.to_numeric(PT_School_District_data_set['birth_year'])
# PT_School_District_data_set['age'] = 2019-PT_School_District_data_set['birth_year']

print("range age = ", PT_School_District_data_set['age'].min(), "to ", PT_School_District_data_set['age'].max())

PT_School_District_data_set['age'].value_counts(sort = True, dropna = False)
PT_School_District_data_set['age'].value_counts(sort = True, dropna = True, normalize = True)

PT_School_District_data_set.groupby('age')['PSEUDOID'].count()


# # Histogram

# for_age_graph = PT_School_District_data_set.groupby('age')['PSEUDOID'].count()

# #plt.hist(PT_School_District_data_set['age'], bins = 30, density = False, alpha = 0.55)

# # convert to dataframe
# for_age_graph = for_age_graph.to_frame()
# for_age_graph

# # with pandas
# for_age_graph.hist(bins=20, alpha=0.5)
# plt.ylabel('Frequency')


# plt.hist(for_age_graph, alpha = 0.55)
# plt.ylabel('Frequency')


# plt.xlabel('')
# plt.title("");

# sns.histplot(
#     PT_School_District_data_set,
#     x='age', 
#     palette="light:m_r",
#     edgecolor=".3",
#     linewidth=.5
# )
 
# =============================================================================
# Final grades
# =============================================================================
PT_School_District_data_set.groupby('final_grades')['PSEUDOID'].count()
PT_School_District_data_set['final_grades'].value_counts(sort = True)
PT_School_District_data_set['final_grades'].value_counts(sort = True, normalize=True)

PT_School_District_data_set.groupby('final_grades')['PSEUDOID'].describe()
PT_School_District_data_set.groupby('final_grades')['PSEUDOID'].mean()



#%%
# =============================================================================
# Table 5. Youth Final Grade by QIS Level  
# =============================================================================

# Creating filters for the QIS levels
PT_School_District_data_set.columns

PT_School_District_data_set['qis_level'].value_counts(sort = True, dropna = False)
a = PT_School_District_data_set.qis_level
b = PT_School_District_data_set.final_grades
pd.crosstab(a, b, normalize=True, margins_name='Total')





# ENTRY:
entry_filter = PT_School_District_data_set['qis_level'] == 'Entry'
Entry = PT_School_District_data_set[entry_filter]
#Entry = PT_School_District_data_set.loc[PT_School_District_data_set['qis_level'] == 'Entry']
e1 = Entry.qis_level
e2 = Entry.final_grades
pd.crosstab(e1, e2, margins = True, dropna=True, normalize=True, margins_name='Total')

# Ave. youth final grade for entry programs 
entry_data = Entry['final_grades']
# calculate the mean of the series
mean = entry_data.mean()
print(round(mean, 2))

# Intermediate
interm_filter = PT_School_District_data_set['qis_level'] == 'Intermediate'
Intermediate = PT_School_District_data_set[interm_filter]
#Intermediate = PT_School_District_data_set.loc[PT_School_District_data_set['qis_level'] == 'Intermediate']
i1 = Intermediate.qis_level
i2 = Intermediate.final_grades
pd.crosstab(i1, i2, margins = True, dropna=False, normalize=True, margins_name='Total')

# Ave. youth final grade for intermediate quality programs 
intermediate_data = Intermediate['final_grades']
# calculate the mean of the series
mean = intermediate_data.mean()
print(round(mean, 2))


# Maintenance
maintenance_filter =  PT_School_District_data_set['qis_level'] == 'Maintenance'
Maintenance = PT_School_District_data_set[maintenance_filter]
#Maintenance = PT_School_District_data_set.loc[PT_School_District_data_set['qis_level'] == 'Maintenance']
m1 = Maintenance.qis_level
m2 = Maintenance.final_grades
pd.crosstab(m1, m2, margins = True, dropna=False, normalize=True, margins_name='Total')

# Ave. youth final grade for maintenance quality programs 
maintenance_data = Maintenance['final_grades']
# calculate the mean of the series
mean = maintenance_data.mean()
print(round(mean, 2))

#%%

# =============================================================================
# Table 4. Youth Final Grade by Program Quality  
# =============================================================================

PT_School_District_data_set['PQA_Classification'].value_counts(sort = True, dropna = False)

# high quality
high_quality_filter = PT_School_District_data_set['PQA_Classification'] == 'high quality'
high_quality = PT_School_District_data_set[high_quality_filter]

hq1 = high_quality.PQA_Classification
hq2 = high_quality.final_grades
pd.crosstab(hq1, hq2, margins = True, dropna=True, normalize=True, margins_name='Total')

# Ave. youth final grade for high quality programs 
high_quality_data = high_quality['final_grades']
# calculate the mean of the series
mean = high_quality_data.mean()
print(round(mean, 2))




# satisfactory
satisfactory_filter = PT_School_District_data_set['PQA_Classification'] == 'satisfactory'
satisfactory = PT_School_District_data_set[satisfactory_filter]

s1 = satisfactory.PQA_Classification
s2 = satisfactory.final_grades
pd.crosstab(s1, s2, margins = True, dropna=True, normalize=True, margins_name='Total')

# Ave. youth final grade for satisfactory programs 
satisfactory_data = satisfactory['final_grades']
# calculate the mean of the series
mean = satisfactory_data.mean()
print(round(mean, 2))



# Low quality
Low_quality_filter = PT_School_District_data_set['PQA_Classification'] == 'Low quality'
Low_quality = PT_School_District_data_set[Low_quality_filter]

lq1 = Low_quality.PQA_Classification
lq2 = Low_quality.final_grades
pd.crosstab(lq1, lq2, margins = True, dropna=True, normalize=True, margins_name='Total')

# Ave. youth final grade for satisfactory programs 
Low_quality_data = Low_quality['final_grades']
# calculate the mean of the series
mean = Low_quality_data.mean()
print(round(mean, 2))


#%%

d_qis = {
    "Entry": [0, 2.150538,  19.354839,  34.408602,  44.086022],
    'Intermediate': [1.03366, 2.332362,  12.854492,  28.465412,  55.314074],
    'Maintenance': [1.733102,  4.159445,  17.677643,  34.662045,  41.767764],
}

df = pd.DataFrame(data=d_qis)
df.plot.bar()


plt.show()

#%%
# Cleaning ...
del  e1, e2, Entry,  i1, i2, Intermediate, m1, m2, Maintenance, a, b, entry_filter, interm_filter, maintenance_filter, pqa #for_age_graph, column_to_strip
del df, d_qis,  entry_data	, entry_filter,	 interm_filter,	 intermediate_data,	 maintenance_data,	 maintenance_filter,	 mean
#%%
# Table 5. Youth Final Grades by Need Level 
PT_School_District_data_set['org_need_level'].value_counts()

a = PT_School_District_data_set.org_need_level
b = PT_School_District_data_set.final_grades
pd.crosstab(a, b, normalize=True, margins_name='Total')



Low = PT_School_District_data_set.loc[PT_School_District_data_set['org_need_level']=='Low Need']
l1 = Low.org_need_level
l2 = Low.final_grades
pd.crosstab(l1, l2, margins = True, dropna=False, normalize=True, margins_name='Total')

# Ave. youth final grade for low-quality programs 
low_data = Low['final_grades']
# calculate the mean of the series
mean = low_data.mean()
print(round(mean, 2))



Medium = PT_School_District_data_set.loc[PT_School_District_data_set['org_need_level']=='Medium Need']
m1 = Medium.org_need_level
m2 = Medium.final_grades
pd.crosstab(m1, m2, margins = True, dropna=False, normalize=True, margins_name='Total')

# Ave. youth final grade for low-quality programs 
medium_data = Medium['final_grades']
# calculate the mean of the series
mean = medium_data.mean()
print(round(mean, 2))


High = PT_School_District_data_set.loc[PT_School_District_data_set['org_need_level'] == 'High Need']
h1 = High.org_need_level
h2 = High.final_grades
pd.crosstab(h1, h2, margins = True, dropna=False, normalize=True, margins_name='Total')

# Ave. youth final grade for low-quality programs 
hight_data = High['final_grades']
# calculate the mean of the series
mean = hight_data.mean()
print(round(mean, 2))



#%%
# Cleaning ...
del h1, h2, High, l1, l2, Low, m1, m2, Medium, a, b

# In[96]:


#PT_School_District_data_set['Enrolled_GRADE_x'].value_counts(sort=True, dropna=False)


# In[97]:


#PT_School_District_data_set['Enrolled_GRADE_x'].value_counts(sort=True, dropna=False, normalize = True)


# ## Dataset for the pair plots
# *Cleaning the Not Applicable  part*

# In[104]:


PT_School_District_data_set[ 'org_need_level' ] = PT_School_District_data_set[ 'org_need_level' ].replace("Not Applicable", np.nan)
 


# In[98]:


df3 = PT_School_District_data_set[['final_grades', 'pqa_score', 'qis_level' , 'org_need_level']]
# Let's add the student's gender
#df3 = PT_School_District_data_set[['final_grades', 'pqa_score', 'qis_level' , 'org_need_level', 'STU_GENDER']]
df3.describe()


# In[99]:


PT_School_District_data_set[[ 'qis_level' , 'org_need_level']].describe()


# In[100]:


PT_School_District_data_set[ 'qis_level' ].value_counts(sort=True, dropna=False)
 

# In[101]:


PT_School_District_data_set[ 'qis_level' ].value_counts(sort=True, dropna=False, normalize = True)


# In[102]:


PT_School_District_data_set[ 'org_need_level' ].value_counts(sort=True, dropna=False)


# In[103]:


PT_School_District_data_set[ 'org_need_level' ].value_counts(sort=True, dropna=False, normalize = True)



# # Bivariate analysis

# In[105]:


sns.pairplot(df3);


# In[106]:


sns.scatterplot(data=df3, x='pqa_score', y='final_grades') #, hue='qis_level')
plt.ylabel("Youth's Final grades")
plt.xlabel('PQA Scores')
plt.title("PQA Scores vs Youth's Final grades");


# In[107]:


sns.pairplot(df3, hue = 'qis_level', markers=["o", "s", "D"]);


# In[108]:
# =============================================================================
# Figure 5a. Pairwise Association Among Variables grouped by QIS Level 
# =============================================================================
# Select variables to include in the pair plot
# selected_vars = ['final_grades', 'pqa_score', 'qis_level']

# # Create a new DataFrame with only the selected variables
# selected_data = df3[selected_vars]

# # Create a pair plot with the selected variables
# sns.pairplot(selected_data, hue = 'qis_level', diag_kind='hist')


# sns.pairplot(df3, hue = 'qis_level') #, markers=["o", "s", "D"])
# #sns.pairplot(penguins, hue="species", diag_kind="hist");

# sns.kdeplot(data=PT_School_District_data_set, x='final_grades', 
#              hue = 'qis_level')

# sns.histplot(data=PT_School_District_data_set, x='final_grades',
#             hue = 'qis_level', multiple="stack")




# =============================================================================
# Figure 7a. Pairwise Associations Grouped by QIS Level  
# =============================================================================
# Create the first graph
# Define the color palette you want to use
color_palette = ["dodgerblue", "maroon", "darkgreen"]
# That's the good one :
sns.displot(data=PT_School_District_data_set, x='final_grades',
            hue = 'qis_level', 
            kind='kde',  palette=color_palette,
            fill=True)

plt.xlabel("Final Grades")

# That's the good one :
sns.displot(data=PT_School_District_data_set, x='pqa_score',
            hue = 'qis_level', 
            kind='kde',  palette=color_palette,
            fill=True)

plt.xlabel("PQA Scores")



# =============================================================================
# Figure 7b. Pairwise Associations Grouped by Community Need Level
# =============================================================================
sns.displot(data=PT_School_District_data_set, x='final_grades',
            hue = 'org_need_level', 
            kind='kde',  palette=color_palette,
            fill=True)
plt.xlabel("Final Grades")
plt.show()
# That's the good one :
sns.displot(data=PT_School_District_data_set, x='pqa_score',
            hue = 'org_need_level', 
            kind='kde',  palette=color_palette,
            fill=True)

plt.xlabel("PQA Scores")




# In[109]:


sns.pairplot(df3, hue = 'qis_level')


# In[110]:




# In[111]:


var1 = PT_School_District_data_set.final_grades
var2 = PT_School_District_data_set.qis_level
pd.crosstab(var1, var2, margins = True, dropna=False, normalize=True, margins_name='Total')*100


# In[112]:
# =============================================================================
# Figure 5b. Pairwise Association Among Variables grouped by Community Need Level
# =============================================================================






# Define the color palette you want to use
color_palette = ["dodgerblue", "maroon", "darkgreen"]

# Create the pair plot and set the color palette
#sns.pairplot(iris, hue="species", palette=color_palette)
# Create a pair plot
sns.pairplot(df3, hue = 'org_need_level', palette=color_palette) #, markers=["o", "s", "D", "X"]);
# Compute the means of each variable by 
#means = df3.groupby('org_need_level').mean()


# # Add the means to the pair plot
# for i, j in zip(*np.triu_indices_from(g.axes, k=1)):
#     g.axes[i, j].axhline(means.iloc[0, j], ls='--', color='red')
#     g.axes[i, j].axhline(means.iloc[1, j], ls='--', color='green')
#     g.axes[i, j].axhline(means.iloc[2, j], ls='--', color='blue')

# Show the pair plot
plt.show()

# In[113]:
# =============================================================================
# CROSS-TABS
# =============================================================================

var1 = PT_School_District_data_set.final_grades
var2 = PT_School_District_data_set.org_need_level
pd.crosstab(var1, var2, margins = True, dropna=False, normalize=True, margins_name='Total')*100


# In[114]:


var1 = PT_School_District_data_set.final_grades
var2 = PT_School_District_data_set['STU_GENDER']
pd.crosstab(var1, var2, margins = True, dropna=False, normalize=True, margins_name='Total')*100


# # ANOVA

# In[ ]:





# In[115]:



moore_lm = ols('final_grades ~ C(STU_GENDER)',
               data=PT_School_District_data_set).fit()

table = sm.stats.anova_lm(moore_lm, typ=2) # Type 2 ANOVA DataFrame
table


# In[ ]:





# In[116]:


df2 = PT_School_District_data_set[['qis_level' , 'org_need_level']]
df2.describe()


# In[117]:


PT_School_District_data_set['qis_level'].value_counts(sort = True, dropna = False)


# In[118]:


df2['qis_level'].value_counts(sort = True, dropna = False)


# In[119]:


df2['org_need_level'].value_counts(sort = True, dropna = False)


# # Correlations

# In[120]:


corr_df = PT_School_District_data_set[['final_grades', 'pqa_score']]


# In[121]:


# spearman : Spearman rank correlation
# DataFrame.corr(method='pearson')
# As a reminder : 

df3 = PT_School_District_data_set[['final_grades', 'pqa_score', 'qis_level' , 'org_need_level', 'STU_GENDER', "age"]]

df3.corr(method='spearman')


# In[122]:


# Testing from an example
# import numpy as np
from scipy import stats
# res = stats.spearmanr([1, 2, 3, 4, np.nan], [5, 6, 7, np.nan, 7])
# res


# ## Correlations that are in the report

# In[123]:


df3_for_correlation = df3.dropna()


# In[124]:
# =============================================================================
# CORRELATIONS 
# =============================================================================

from scipy import stats
result1 = stats.spearmanr(df3_for_correlation.final_grades, df3_for_correlation.qis_level, nan_policy="omit")
print("Results grades vs qis_levels =", result1)


print(round(-0.0802527571678361, 2))
print(round(1.245872031555676e-07))


# In[126]:


result2 = stats.spearmanr(df3_for_correlation.final_grades, df3_for_correlation.org_need_level, nan_policy="omit")
print("Final grades vs org need level =", result2)


print(round(0.009447003023966092, 2))
print(round(0.5343829132014501, 2))


# In[128]:


result3 = stats.spearmanr(df3_for_correlation.final_grades, df3_for_correlation.pqa_score, nan_policy="omit")
print("Final grades and PQA = ", result3)


print(round(-0.2194340601121642, 3))
print(round(2.415532489743061e-48, 2))

#%%


result4 = stats.spearmanr(df3_for_correlation.final_grades, df3_for_correlation.pqa_score, nan_policy="omit")
print("Final grades and PQA = ", result3)


#%%
result4 = stats.spearmanr(df3_for_correlation.final_grades, df3_for_correlation.STU_GENDER, nan_policy="omit")
print("Final grades and gender = ", result4)

print(round(-0.16784868894719612, 3))
print(round(1.024010958616467e-28, 2))

#%%
result5 = stats.pearsonr(df3_for_correlation.final_grades, df3_for_correlation.age) #, nan_policy="omit")
print("Final grades and age = ", result5)

print(round(0.024376354564962593, 3))
print(round( 0.1088385747821721, 2))

# In[130]:


# # Creating a filter and applying it to the dataset :

# grade_0 = corr_df[corr_df['final_grades']==0]
# grade_0.head()


# # In[131]:


# grade_0.dropna().corr(method='spearman')


# # In[132]:


# # Creating a filter and applying it to the dataset :

# grade_1 = corr_df[corr_df['final_grades']==1]
# grade_1.head()


# In[133]:


# grade_1.dropna().corr()


# In[134]:


# Creating a filter and applying it to the dataset :

# grade_2 = corr_df[corr_df['final_grades']==2]
# grade_2.head()


# In[135]:


# grade_2.dropna().corr()


# In[136]:


# Creating a filter and applying it to the dataset :

# grade_3 = corr_df[corr_df['final_grades']==3]
# grade_3.head()


# In[137]:


# grade_3.dropna().corr()


# In[138]:


# Creating a filter and applying it to the dataset :

# grade_4 = corr_df[corr_df['final_grades']==4]
# grade_4.head()


# In[139]:


# grade_4.dropna().corr()


# In[ ]:





# In[140]:


corr_df.corr()


# In[141]:


from scipy.stats.stats import pearsonr

#calculation correlation coefficient and p-value between x and y
corr_df = PT_School_District_data_set[['final_grades', 'pqa_score', 'age']].dropna()

v1 = corr_df.final_grades
v2 = corr_df.pqa_score

pearsonr(v2, v1)


# In[142]:


# from scipy.stats.stats import pearsonr

# #calculation correlation coefficient and p-value between x and y
# corr_grades_pqa = grade_0[['final_grades', 'pqa_score']].dropna()

# v1 = corr_grades_pqa.final_grades
# v2 = corr_grades_pqa.pqa_score

# pearsonr(v2, v1)


# In[143]:


# Creating a filter and applying it to the dataset :

# grade_1 = PT_School_District_data_set[PT_School_District_data_set['final_grades']==1]
# grade_1.head()


# In[144]:


#calculation correlation coefficient and p-value between x and y
# corr_df = grade_1[['final_grades', 'pqa_score']].dropna()

# v1 = corr_df.final_grades
# v2 = corr_df.pqa_score

# pearsonr(v2, v1)


# In[145]:


var1 = PT_School_District_data_set.final_grades
var2 = PT_School_District_data_set.qis_level
pd.crosstab(var1, var2, margins = True, dropna=False, normalize=True)*100

# In[146]:


sns.catplot(x="qis_level", y="final_grades", kind="bar", data=PT_School_District_data_set);
plt.xlabel("QIS Level")
plt.ylabel("Final grades")
plt.ylim(0, 5)
plt.title("Final course grades and QIS level");


# In[147]:


var1 = PT_School_District_data_set.final_grades
var2 = PT_School_District_data_set.org_need_level
pd.crosstab(var1, var2, margins = True, dropna=False, normalize=True)*100


# In[148]:


PT_School_District_data_set.columns


# In[149]:


PT_School_District_data_set['Type'].value_counts(sort = True, dropna = True)


# In[150]:


PT_School_District_data_set['PSEUDOID'].value_counts(sort = True, dropna = True)


# In[151]:


45.887386+0.541676+0.235511+0.088317-46.227821


# In[152]:


#basic scatterplot:  Q->Q

#scat1 = sns.stripplot(x="pqa_score", y="final_grades", data=PT_School_District_data_set)
scat1 = sns.regplot(x="pqa_score", y="final_grades", fit_reg=False, data=df3)
plt.ylabel('Final grades')
plt.xlabel('PQA Scores')
plt.title('Scatterplot for the Association Between pqa scores and final grade\n');


# In[153]:


df3.columns


# In[154]:


g = sns.relplot(
    data=df3,
    x="pqa_score", y="final_grades",
    hue = 'qis_level', size='org_need_level',
    sizes=(10, 200),
)


# In[191]:


dir()


# In[ ]:


del df3
del df3_for_correlation


# ## Gender and equity

# In[155]:


sns.set_theme(style="whitegrid")


# In[156]:


# Draw a nested boxplot to show bills by day and time
ax = sns.barplot(x='STU_GENDER', y="final_grades",
            hue='qis_level',
            data=PT_School_District_data_set)
plt.xlabel("Student's gender")
plt.ylabel("Final grades")
plt.ylim(0, 6.5)
plt.title("Final course grades and QIS level by Gender");

sns.move_legend(ax, "upper right")


# In[157]:
# =============================================================================
# Figure 4. Youth Final Grades by QIS Level, Community Socioeconomic Need and Youth Gender Identity 
# =============================================================================

# ax = sns.barplot(x='qis_level', y="final_grades", ci = None,hue='STU_GENDER',  data=PT_School_District_data_set)
# # Add annotations to the plot
# for p in ax.patches:
#     height = p.get_height()
#     ax.text(x=p.get_x()+p.get_width()/2, y=height+0.125, s=f"{height:.2f}", ha="center")
# #plt.xlabel("Students gender")
# plt.ylabel("Mean Final Grades")
# plt.xlabel("QIS Level")

# # Customize legend
# handles, labels = ax.get_legend_handles_labels()
# ax.legend(handles, ["Male", "Female"], title="Gender", loc="upper right")

# # sns.move_legend(ax, "upper right", title ="Student's Gender");
# plt.ylim(0, 5)
# plt.show()


ax = sns.barplot(x='qis_level', y="final_grades", ci = None, hue='STU_GENDER',
                 order=['Entry', 'Intermediate', 'Maintenance'], data=PT_School_District_data_set)

# Add annotations to the plot
for p in ax.patches:
    height = p.get_height()
    ax.text(x=p.get_x()+p.get_width()/2, y=height+0.125, s=f"{height:.2f}", ha="center")

plt.ylabel("Mean Final Grades")
plt.xlabel("QIS Level")

# Customize legend
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, ["Male", "Female"], title="Gender", loc="upper right")

plt.ylim(0, 5)
plt.show()


# In[159]:
# =============================================================================
# Figure 4. Youth Final Grades by QIS Level, Community Socioeconomic Need and Youth Gender Identity 
# =============================================================================

ax = sns.barplot(x='org_need_level', y="final_grades", ci = None, hue='STU_GENDER', data=PT_School_District_data_set)
#plt.xlabel("Students gender")
plt.ylabel("Mean Final Grades")
plt.xlabel("Community Need Level")

sns.move_legend(ax, "upper right", title ="Student's Gender");
# Add annotations to the plot
for p in ax.patches:
    height = p.get_height()
    ax.text(x=p.get_x()+p.get_width()/2, y=height+0.125, s=f"{height:.2f}", ha="center")

# Customize legend
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, ["Male", "Female"], title="Gender", loc="upper right")
plt.ylim(0, 5.5)

# Show plot
plt.show()


ax = sns.barplot(x='org_need_level', y="final_grades", ci=None, hue='STU_GENDER',
                 order=['Low Need', 'Medium Need', 'High Need'], data=PT_School_District_data_set)

# Add annotations to the plot
for p in ax.patches:
    height = p.get_height()
    ax.text(x=p.get_x()+p.get_width()/2, y=height+0.125, s=f"{height:.2f}", ha="center")

plt.ylabel("Mean Final Grades")
plt.xlabel("Community Need Level")

# Customize legend
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, ["Male", "Female"], title="Gender", loc="upper right")

plt.ylim(0, 5.5)

# Show plot
plt.show()

#%%



# In[158]:


# # Draw a nested boxplot to show bills by day and time
# ax = sns.barplot(x='STU_GENDER', y="final_grades",
#             hue='org_need_level',
#             data=PT_School_District_data_set)
# plt.xlabel("Students gender")
# plt.ylabel("Final grades")
# plt.ylim(0, 6.5)
# sns.move_legend(ax, "upper right", title ="Community Need Levels");



# In[160]:


# Draw a nested boxplot to show bills by day and time
ax = sns.barplot(x='STU_GENDER', y="final_grades",
            hue='org_need_level',
            data=PT_School_District_data_set)
plt.ylim(0, 6.5)
sns.move_legend(ax, "upper right")


# In[161]:


# Load the penguins dataset
# df = sns.load_dataset("penguins")

# Draw a categorical scatterplot to show each observation
#ax = sns.swarmplot(data=df3, x="pqa_score", y="final_grades", hue = 'qis_level')
#ax.set(ylabel="")


# # Regression 1 - Base model : grades = a * PQA(i) + et

# In[162]:


#  PQA  --> Grades (basic model)
print("Base model - model #1")
reg  = smf.ols("final_grades ~ pqa_score", data = PT_School_District_data_set).fit()
print(reg.summary())


# # Regression 2 - grades = a*PQA(i) + QIS_Need_level(j) + et

# In[163]:


PT_School_District_data_set['qis_level'].value_counts(sort = True, dropna = False)


# In[164]:


def qis_levels(row):
    if row['qis_level'] == 'Entry':
        return 0
    if row['qis_level'] == 'Intermediate':
        return 1
    if row['qis_level'] == 'Maintenance':
        return 2
    else:
        return np.nan


PT_School_District_data_set['QIS_LEVELS'] = PT_School_District_data_set.apply(lambda row: qis_levels(row), axis = 1)


# In[166]:


#  PQA + Need_level --> Grades 
print("This might be the best one for now : a combinaison of needs level, pqa scores and qis level.")
#reg2  = smf.ols("final_grades ~ pqa_score + C(qis_level)", data=PT_School_District_data_set).fit()
reg2  = smf.ols("final_grades ~ C(QIS_LEVELS) + pqa_score ", data=PT_School_District_data_set).fit()
print(reg2.summary())


# # Regression 3 - grades = a*PQA(i) + QIS_Need_Level(j) + Need_Level(k) + et

# In[167]:


PT_School_District_data_set['org_need_level'].value_counts(sort = True, dropna = False)


# In[168]:


def ORG_NEED_LEVEL(row):
    if row['org_need_level'] == 'Low Need':
        return 0
    if row['org_need_level'] == 'Medium Need':
        return 1
    if row['org_need_level'] == 'High Need':
        return 2
    else:
        return np.nan


# In[169]:


PT_School_District_data_set['ORG_NEED_LEVEL'] = PT_School_District_data_set.apply(lambda row: ORG_NEED_LEVEL(row), axis = 1)


# In[170]:


#  PQA + QIS_Need_level + Org_Need_Level --> Grades 
#reg3  = smf.ols("final_grades ~ pqa_score + C(qis_level) + C(org_need_level)", data=PT_School_District_data_set).fit()
reg3  = smf.ols("final_grades ~ pqa_score + C(QIS_LEVELS) + C(ORG_NEED_LEVEL)", data=PT_School_District_data_set).fit()
print(reg3.summary())


# # Regression 4 - grades = pqa + QIS_Need_Level(j) + Need_Level(k) + et

# In[171]:


# QIS_Need_level + Org_Need_Level --> Grades 
reg4  = smf.ols("final_grades ~ pqa_score + C(QIS_LEVELS) + C(ORG_NEED_LEVEL)", data=PT_School_District_data_set).fit()
print(reg4.summary())


# # Regression 5 - grades = QIS_Need_Level(j) + Need_Level(k) + Gender + et

# In[172]:


PT_School_District_data_set['STU_GENDER'].val ue_counts(sort=True, dropna=False)


# In[173]:


def GENDER(row):
    if row['STU_GENDER'] == 'M':
        return 1
    if row['STU_GENDER'] == 'F':
        return 0
    else:
        return np.nan


# In[174]:


PT_School_District_data_set['GENDER'] = PT_School_District_data_set.apply(lambda row: GENDER(row), axis = 1)


# In[175]:

print("THIS IS THE FINAL ONE!!!")
# QIS_Need_level + Org_Need_Level --> Grades 
reg5  = smf.ols("final_grades ~  pqa_score +C(QIS_LEVELS) + C(ORG_NEED_LEVEL) + C(GENDER)", data=PT_School_District_data_set).fit()
print(reg5.summary())

print("USE THIS!!!")
print("gender as an impact on final grades !!!")


# =============================================================================
# DIAGNOSTICS
# =============================================================================

fig = sm.qqplot(reg5.resid, line = "r")



# In[ ]:





# In[176]:


PT_School_District_data_set['Type'].value_counts(sort=True, dropna=False)


# In[177]:


# QIS_Need_level + Org_Need_Level --> Grades 
reg6  = smf.ols("final_grades ~ pqa_score + age + C(QIS_LEVELS) + C(ORG_NEED_LEVEL)+ C(GENDER)", data=PT_School_District_data_set).fit()
print(reg6.summary())




# In[ ]:
   


# In[178]:


#  PQA + QIS_Need_level + Org_Need_Level --> Grades 
reg4  = smf.ols("final_grades ~ pqa_score + C(org_need_level)", data=PT_School_District_data_set).fit()
print(reg4.summary())


# # Base model with FINAL_FSAELA
# 
# ### We shouldn't use those they are correlated to the final grades.

# In[179]:


PT_School_District_data_set.columns


# In[180]:


PT_School_District_data_set['FSALEVEL_x'].value_counts()


# In[181]:


#  PQA  --> SCALESCORE	FSALEVEL (Basic model)
print("Base model - model #1 with the FSAELA test as a dependent variable")
print("\n")
reg_0  = smf.ols("SCALESCORE_x ~ pqa_score", data = PT_School_District_data_set).fit() # + C(FSALEVEL_x)
print(reg_0.summary())


# In[182]:


#  PQA  --> SCALESCORE	FSALEVEL (Basic model + FSAELA scores)
print("Base model - model #1 with the FSAELA test as a dependent variable and FSA levels as a dependent categorical variable")
print("\n")
reg_1  = smf.ols("SCALESCORE_x ~ pqa_score + C(FSALEVEL_x)", data = PT_School_District_data_set).fit() # 
print(reg_1.summary())


# In[183]:


#  PQA  --> SCALESCORE	FSALEVEL (Basic model + FSAELA scores)
print("\n")
reg_1  = smf.ols("SCALESCORE_x ~ pqa_score + C(FSALEVEL_x)", data = PT_School_District_data_set).fit() # 
print(reg_1.summary())


# In[184]:


PT_School_District_data_set.columns


# In[185]:


#  PQA  --> SCALESCORE	FSALEVEL (Basic model)
print("Base model - model #1 with the FSAELA test as a dependent variable and the QIS levels")
print("\n")
reg_00  = smf.ols("SCALESCORE_x ~ pqa_score + C(FSALEVEL_x) + C(qis_level)", data = PT_School_District_data_set).fit() # + C(FSALEVEL_x)
print(reg_00.summary())


# In[186]:


#  PQA  --> SCALESCORE	FSALEVEL (Basic model)
print("Base model - model #1 with the FSAELA test as a dependent variable")
print("\n")
reg_01  = smf.ols("SCALESCORE_x ~ pqa_score + C(qis_level)", data = PT_School_District_data_set).fit() # + C(FSALEVEL_x)
print(reg_01.summary())


# In[ ]:





# In[187]:

del GENDER, ORG_NEED_LEVEL, ax, pqa, qis_levels,	 reg3,	 reg5,	 reg6,	 reg_0,	 reg_1    

print("THIS IS THE FINAL ONE!!!")
# QIS_Need_level + Org_Need_Level --> Grades 
reg5  = smf.ols("final_grades ~  pqa_score +C(QIS_LEVELS) + C(ORG_NEED_LEVEL) + C(GENDER)", data=PT_School_District_data_set).fit()
print(reg5.summary())

print("USE THIS!!!")
print("gender as an impact on final grades !!!")

#%%
# =============================================================================
# DESSA ANALYSIS
# =============================================================================
print("This was done in a previsou data management and was exported. To continue, import the treated data set below.")
# PT_School_District_data_set.columns
# PT_School_District_data_set["dessa_change"] = PT_School_District_data_set['Overall_post']-PT_School_District_data_set['Overall_pre']

# df4 = PT_School_District_data_set[['SiteName', 'QIS_LEVELS', 'ORG_NEED_LEVEL', 'final_grades', 
#                                    'pqa_score', 'Overall_pre', 'Overall_post',
#                                    'age', 'dessa_change']]


# grouped_by_program = df4.groupby("SiteName").mean()
           
# grouped_by_program[0:5]      

# Exporting and importing the results            
# This is commented out, because we've added the index column to the file
# grouped_by_program.to_excel("2023_03_08_grouped_by_program_for_DESSA.xlsx")

data = pd.read_excel("2023_03_08_grouped_by_program_for_DESSA.xlsx")
data.columns
data['SiteName'].value_counts()





# =============================================================================
# Correlation Final Grades and SEL 
# =============================================================================
df_for_correlation = data.dropna()
result = stats.pearsonr(df_for_correlation.final_grades, df_for_correlation.dessa_change)
print("Correlation Final Grades vs DESSA change =", result)
round(-0.21183818126031673, 2)
round(0.6869958912621787, 2)


# =============================================================================
# SEL  by program quality
# =============================================================================

var1 = data.final_grades
var2 =data.dessa_change
pd.crosstab(var1, var2, margins = True, dropna=False, normalize=True, margins_name='Total')*100

def qis_levels2(row):
    if row['QIS_LEVELS']==0:
        return 'Entry'
    if row['QIS_LEVELS']==1:
        return 'Intermediate'
    if row['QIS_LEVELS'] == 2:
        return 'Maintenance'
    else:
        return np.nan


data['qis_levels2'] = data.apply(lambda row: qis_levels2(row), axis = 1)
    
        
# create scatter plot
sns.scatterplot(data=data, x='dessa_change', y="final_grades", hue = "qis_levels2")
plt.ylabel("Mean Final Grades")
plt.xlabel("DESSA Change")

# display plot
plt.show()







#  PQA  --> SCALESCORE	FSALEVEL (Basic model)
# AGE AND THE CHANGE IN DESSA SCORES DOESN'T HAVE AN EFFECT ON THE FINAL GRADES  age++Overall_pre+Overall_post
print("Base model - Program  level data with the DESSA")
print("\n")
reg_8  = smf.ols("final_grades ~ pqa_score + dessa_change + age", data = PT_School_District_data_set).fit() # 
print(reg_8.summary())

reg_grouped_by  = smf.ols("final_grades ~  dessa_change +C(ORG_NEED_LEVEL)", data = data).fit() # 
print(reg_grouped_by.summary())

# =============================================================================+ pqa_score ++ C(QIS_LEVELS)
# DESSA WITHOUT THE GROUPBY PROGRAM
# =============================================================================

PT_School_District_data_set.columns
#PT_School_District_data_set["dessa_change"] = PT_School_District_data_set['Overall_post']-PT_School_District_data_set['Overall_pre']


# QIS_Need_level + Org_Need_Level --> Grades 
# + Overall_pre + Overall_post 
reg_all_dat_not_groupef  = smf.ols("final_grades ~ pqa_score + age + C(QIS_LEVELS) + C(ORG_NEED_LEVEL)+ C(GENDER)+ dessa_change ", data=PT_School_District_data_set).fit()
print(reg_all_dat_not_groupef.summary())

# We know there is a significante difference between the two
dessa_anova = ols('final_grades ~ C(DESSA_rating)',
               data=PT_School_District_data_set).fit()

anov_table = sm.stats.anova_lm(dessa_anova, typ=2) # Type 2 ANOVA DataFrame
anov_table

# On fait l'analyse pour ceux qui ont le dessa et pour ceux qui n'ont pas le dessa
# With the DESSA :
with_dessa_filter = PT_School_District_data_set['DESSA_rating'] == 1
with_dess_df = PT_School_District_data_set[with_dessa_filter ]

# Running the model
# QIS_Need_level + Org_Need_Level --> Grades 
reg_with_dessa_only  = smf.ols("final_grades ~ pqa_score + age + C(QIS_LEVELS) + C(ORG_NEED_LEVEL) + C(GENDER) + dessa_change", data=PT_School_District_data_set).fit()
print(reg_with_dessa_only.summary())

































