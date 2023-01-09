# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 2022
@author: davidsantiagoquevedo
@author: ntorresd
"""  
import warnings
warnings.filterwarnings('ignore')

import yaml
import pandas as pd

config = yaml.load(open("config.yml", "r"))["default"]

DIST_PATH = config['PATHS']['OUT_PATH'].format(dir = 'epidemiological_distributions')
OUT_PATH = config['PATHS']['OUT_PATH'].format(dir = 'tables')
UTILS_PATH = config['PATHS']['UTILS_PATH'].format(dir = 'epidemiological_distributions')

import sys
sys.path.append(UTILS_PATH)
import utilities_epi_dist as ut

df_best_models = ut.best_model()
for col in df_best_models.columns:
    df_best_models[col] = df_best_models[col].round(2)

dict_epi_distri   = {'onset_hosp': 'Onset to hosp',
                        'onset_icu': 'Onset to ICU',
                        'onset_death': 'Onset to death',
                        'hosp_stay':'Hosp. stay',
                        'icu_stay': 'ICU stay'
                        }
df_best_models = df_best_models.reset_index()
df_best_models = df_best_models.replace(dict_epi_distri)
df_best_models = df_best_models.rename(columns = {'Epidemilogical distribution' : 'Delay time'})

df_best_models.to_csv(OUT_PATH + 'table_s4.csv', index = False)