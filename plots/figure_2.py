# -*- coding: utf-8 -*-
"""
Created on Wed 1 Dic 2022
@author: davidsantiagoquevedo
@author: ntorresd
"""
import warnings
warnings.filterwarnings('ignore')

import sys
import yaml
import matplotlib.pyplot as plt

config = yaml.load(open("config.yml", "r"))["default"]

SCRIPTS_PATH = config['PATHS']['PLOT_PATH']
FIG_PATH = config['PATHS']['FIG_PATH'].format(dir = 'plots')
OUT_PATH = config['PATHS']['OUT_PATH'].format(dir = 'genomics')
sys.path.append(SCRIPTS_PATH)

import results_genomics as results_genomics

# Multinomial regression
fig, ax = plt.subplots(1,2, figsize = (12, 6))
axi = ax[0]
results_genomics.plot_multinomial(axi)
axi.set_xlabel('Week')
axi.set_ylabel('Prevalence')
axi.legend()
axi.set_title('a.')

# Heat map
axi = ax[1]
results_genomics.plot_heatmap(axi, n = 200)
axi.set_title('b.')
fig.savefig(FIG_PATH + 'figure_2.png')