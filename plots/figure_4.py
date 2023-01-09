# -*- coding: utf-8 -*-
"""
Created on Mon 29 Nov 2022
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
sys.path.append(SCRIPTS_PATH)

import results_severe_outcomes as results_severe_outcomes

fig, ax = plt.subplots(2,3, figsize=(12,8))
plt.rcParams["savefig.pad_inches"] = 0.4

axi = ax[0]
results_severe_outcomes.plot_percentage(axi)

axi[0].set_ylabel('Hospitalization percentage by age-group')
axi[1].set_ylabel('ICU percentage by age-group')
axi[2].set_ylabel('Deaths percentage by age-group')
for axii in axi:
    axii.tick_params(axis='x', labelrotation=90)
    axii.set_xlabel('Age group')
axi[0].set_title('a.')
axi[1].set_title('b.')
axi[2].set_title('c.')
handles1, labels1 = axi[2].get_legend_handles_labels()

axi = ax[1]
results_severe_outcomes.plot_proportions_hist(axi)

axi[0].set_ylabel('Hospital proportion by wave')
axi[1].set_ylabel('ICU proportion by wave')
axi[2].set_ylabel('Death proportion by wave')
for axii in axi:
    axii.set_xlabel('Wave')
axi[0].set_title('d.')
axi[1].set_title('e.')
axi[2].set_title('f.')
handles2, labels2 = axi[2].get_legend_handles_labels()

handles = handles1 + handles2
labels = labels1 + labels2
fig.legend(handles, labels, bbox_to_anchor = (0.79, -0.02), ncol = 6)

fig.savefig(FIG_PATH+'figure_4.png')