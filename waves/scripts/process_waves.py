# -*- coding: utf-8 -*-
"""
Created on Tue Nov 15 2022
@author: davidsantiagoquevedo
@author: ntorresd
"""
import yaml
import pandas as pd
from time import time
import sys 

ymlfile = open("config.yml", "r")
cfg = yaml.load(ymlfile)
config = cfg["default"]

OUT_PATH = config['PATHS']['OUT_PATH'].format(dir = 'waves')
# The roots were selected by visual inspection of /figures/roots_confirmed_cases.png 
# and set by default in config.yml
DATES = config['WAVES']['ROOTS'] 

df_roots = pd.read_csv(OUT_PATH + 'roots_confirmed_cases.csv')

df_waves = df_roots.iloc[DATES]
df_waves['wave'] = [1, 1, 2, 2, 3, 3, 4, 4]
df_waves['label'] = ['start', 'end', 'start', 'end', 'start', 'end', 'start', 'end']
df_waves_t = df_waves.pivot(index = 'wave', columns = 'label', values = 'date').reset_index()
df_waves_t = df_waves_t[['wave', 'start', 'end']]
df_waves_t.columns = ['wave','start_date','end_date']

df_waves_t[df_waves_t.wave.notnull()].to_csv(OUT_PATH + 'waves.csv', index = False)