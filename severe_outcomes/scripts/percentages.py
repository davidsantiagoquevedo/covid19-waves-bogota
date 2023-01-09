# -*- coding: utf-8 -*-
"""
Created on Thr Jul 31 2022
@author: davidsantiagoquevedo
@author: ntorresd
"""

import sys
import yaml
import pandas as pd
import matplotlib.pyplot as plt

config = yaml.load(open("config.yml", "r"))["default"]

# Paths
DATA_PATH = config['PATHS']['DATA_PATH']
OUT_PATH = config['PATHS']['OUT_PATH'].format(dir = 'severe_outcomes')
UTILS_PATH = config['PATHS']['UTILS_PATH'].format(dir = 'severe_outcomes')

# Plot style
plt.style.use(config['PATHS']['PLOT_STYLE'])
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

# Import useful functions
sys.path.append(UTILS_PATH)
import utilities_severity as ut

# Read data
df_hosp = pd.read_csv(DATA_PATH+'hosp_waves_bog.csv')
df_icu = pd.read_csv(DATA_PATH+'icu_waves_bog.csv')
df_death = pd.read_csv(DATA_PATH+'death_waves_bog.csv')

# Calculate counts and percentages
df_hosp_perc = ut.calculate_percentage(df_hosp)
df_icu_perc = ut.calculate_percentage(df_icu)
df_death_perc = ut.calculate_percentage(df_death)  

# Save data
df_hosp_perc.to_csv(OUT_PATH+'hosp_percentages.csv', index=False)
df_icu_perc.to_csv(OUT_PATH+'icu_percentages.csv', index=False)
df_death_perc.to_csv(OUT_PATH+'deaths_percentages.csv', index=False)
