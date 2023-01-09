# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 2022
@author: davidsantiagoquevedo
@author: cwhittaker1000
@author: ntorresd
"""
import yaml
import pandas as pd

ymlfile = open("config.yml", "r")
cfg = yaml.load(ymlfile)
config = cfg["default"]

DATA_PATH = config['PATHS']['DATA_PATH']
OUT_PATH = config['PATHS']['OUT_PATH'].format(dir = 'genomics')
FIG_PATH = config['PATHS']['FIG_PATH'].format(dir = 'genomics')
DATE_GENOMICS = config['UPDATE_DATES']['GENOMICS']

# Read the data
df_var = pd.read_csv(DATA_PATH + 'variants-ic-bog_' + DATE_GENOMICS + '.csv')
df_var['y_week'] = df_var.year.astype(str) + '-' + df_var.week.astype(str)

# Pivot table
table = df_var.pivot(index='y_week',columns='lineage',values='n_seq_var')
table.fillna(0, inplace = True)
table = table.reset_index().reset_index().rename(columns = {'index':'t'}).reset_index(drop=True)
del(table['y_week'])

# Save results
table.to_csv(DATA_PATH + 'variants_pivot.csv', index = False)