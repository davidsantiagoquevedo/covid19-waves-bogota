# -*- coding: utf-8 -*-
"""
Created on Th December 1 2022
@author: davidsantiagoquevedo
@author: ntorresd
"""  

import warnings
warnings.filterwarnings('ignore')

import sys
import yaml
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

config = yaml.load(open("config.yml", "r"))["default"]

SCRIPTS_PATH = config['PATHS']['PLOT_PATH']
FIG_PATH = config['PATHS']['FIG_PATH'].format(dir = 'plots')
sys.path.append(SCRIPTS_PATH)

import results_severe_outcomes as results_severe_outcomes

fig, ax = plt.subplots(2, 3, figsize=(12, 8), sharex = True)

results_severe_outcomes.plot_rates(ax=ax[1][0], var='CFR', var_name='CFR')
results_severe_outcomes.plot_rates(ax=ax[0][1], var='HCR', var_name='HCR')
results_severe_outcomes.plot_rates(ax=ax[1][1], var='HCR_I', var_name=' ICU-CR')

results_severe_outcomes.plot_rates(ax=ax[0][2], var='HFR', var_name='HFR')
results_severe_outcomes.plot_rates(ax=ax[1][2], var='HFR_I', var_name='ICU-FR')

handles, labels = ax[1][1].get_legend_handles_labels()
ax[0][0].legend(handles, labels, loc='center')
ax[0][0].axis('off')

ax[0][1].tick_params(axis='x', rotation=45)
ax[0][2].tick_params(axis='x', rotation=45)
ax[1][0].tick_params(axis='x', rotation=45)
ax[1][1].tick_params(axis='x', rotation=45)
ax[1][2].tick_params(axis='x', rotation=45)

ax[0][1].set_title('b.')
ax[0][2].set_title('d.')
ax[1][0].set_title('a.')
ax[1][1].set_title('c.')
ax[1][2].set_title('e.')

ax[0][1].set_xlabel('')
ax[0][2].set_xlabel('')
ax[1][0].set_xlabel('Age group')
ax[1][1].set_xlabel('Age group')
ax[1][2].set_xlabel('Age group')

fig.savefig(FIG_PATH + 'figure_5.png')