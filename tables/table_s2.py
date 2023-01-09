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

DATA_PATH = config['PATHS']['DATA_PATH']
VAR_PATH = config['PATHS']['OUT_PATH'].format(dir = 'genomics')
OUT_PATH = config['PATHS']['OUT_PATH'].format(dir = 'tables')

df_mean = pd.read_csv(VAR_PATH + 'advantage_mean.csv')
df_025 = pd.read_csv(VAR_PATH + 'advantage_025.csv')
df_975 = pd.read_csv(VAR_PATH + 'advantage_975.csv')

# Waves information
df_res = pd.DataFrame({})
for col in df_mean.columns.to_list():
    if col == 'pivot_variant':
        df_res[col] = df_mean[col]
    else:
        df_res[col] = df_mean[col].astype(str)+ ' (' + df_025[col].astype(str) + ', ' + df_975[col].astype(str) + ')'

for i in range(df_res.shape[0]+1):
    for j in range(df_res.shape[1]):
        if i-1 == j:
            df_res[df_res.columns[i]].iloc[j] ='0'

df_res = df_res.rename(columns = {'pivot_variant' : 'Pivot variant'})
df_res.to_csv(OUT_PATH + 'table_s2.csv', index = False)