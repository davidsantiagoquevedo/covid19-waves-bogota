# -*- coding: utf-8 -*-
"""
Created on Tue Nov 29 2022
@author: davidsantiagoquevedo
@author: ntorresd
"""
import sys
import yaml
import pandas as pd
import pystan
import time

config = yaml.load(open("config.yml", "r"))["default"]

DATA_PATH = config['PATHS']['DATA_PATH']
OUT_PATH = config['PATHS']['OUT_PATH'].format(dir = 'severe_outcomes')
SCRIPTS_PATH = config['PATHS']['SCRIPTS_PATH'].format(dir = 'severe_outcomes')
UTILS_PATH = config['PATHS']['UTILS_PATH'].format(dir = 'severe_outcomes')

# Import useful functions
sys.path.append(UTILS_PATH)
import utilities_severity as ut
df_confirmed_bogota = pd.read_csv(DATA_PATH + 'confirmed_cases_waves.csv')

# Changing the age groups
age_group_dic={'0-9':[0,9],
              '10-19':[10,19],
              '20-29':[20,29], 
              '30-39':[30,39], 
              '40-49':[40,49], 
              '50-59':[50,59],
              '60-69':[60,69],
              '70-79':[70,79], 
              '80+':[80,9999]}

cat_type = pd.api.types.CategoricalDtype(categories = age_group_dic.keys(),
                                         ordered=True)
df_confirmed_bogota = ut.age_group_dec(df_confirmed_bogota, 'age', 'age_unit', age_group_dic)
df_confirmed_bogota['age_group'] = df_confirmed_bogota.age_group.astype(cat_type)

cases_wave = df_confirmed_bogota[['wave', 'age_group']].value_counts()\
            .reset_index().rename(columns = {0 : 'cases'})

hosp = \
df_confirmed_bogota[(df_confirmed_bogota.hospitalization.notnull())]\
                    [['wave', 'age_group']].value_counts()\
                    .reset_index().rename(columns = {0 : 'hosp'})
                    
icu = \
df_confirmed_bogota[(df_confirmed_bogota.icu.notnull())]\
                    [['wave', 'age_group']].value_counts()\
                    .reset_index().rename(columns = {0 : 'icu'})

hosp_death = \
df_confirmed_bogota[(df_confirmed_bogota.hospitalization.notnull()) &
                    (df_confirmed_bogota.condition == 'Fallecido') & 
                    (df_confirmed_bogota.death.notnull())]\
                    [['wave', 'age_group']].value_counts()\
                    .reset_index().rename(columns = {0 : 'hosp_death'})
                    
icu_death = \
df_confirmed_bogota[(df_confirmed_bogota.icu.notnull()) &
                    (df_confirmed_bogota.condition == 'Fallecido') & 
                    (df_confirmed_bogota.death.notnull())]\
                    [['wave', 'age_group']].value_counts()\
                    .reset_index().rename(columns = {0 : 'icu_death'})

                    
deaths = \
df_confirmed_bogota[(df_confirmed_bogota.condition == 'Fallecido') & 
                    (df_confirmed_bogota.death.notnull())]\
                    [['wave', 'age_group']].value_counts()\
                    .reset_index().rename(columns = {0 : 'deaths'})

cases_wave = \
cases_wave.merge(hosp, how = 'left', on = ['wave', 'age_group'])\
                .merge(icu, how = 'left', on = ['wave', 'age_group'])\
                .merge(hosp_death, how = 'left', on = ['wave', 'age_group'])\
                .merge(icu_death, how = 'left', on = ['wave', 'age_group'])\
                .merge(deaths, how = 'left', on = ['wave', 'age_group'])
cases_wave = cases_wave.sort_values(by = ['wave', 'age_group'])

cases_wave['CFR'] =  (cases_wave.deaths / cases_wave.cases * 100).round(1)
cases_wave['HCR'] =  (cases_wave.hosp / cases_wave.cases * 100).round(1)
cases_wave['HCR_I'] =  (cases_wave.icu / cases_wave.cases * 100).round(1)
cases_wave['HFR'] =  (cases_wave.hosp_death / cases_wave.hosp * 100).round(1)
cases_wave['HFR_I'] =  (cases_wave.icu_death / cases_wave.icu * 100).round(1)

cases_wave.to_csv(OUT_PATH + 'rates.csv', index = False)