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
sys.path.append(SCRIPTS_PATH)

import results_epidemiological_distributions as red

# Option 1
fig, ax = plt.subplots(5,2, figsize = (10, 14), sharex = True)
dist = 'onset_hosp'
red.plot_best_model_bar(dist, ax[0][0], 3, 'Onset to hospitalization', 'a.')
red.plot_violin(dist, 'Onset to hospitalization', 'f.', ax[0][1])

dist = 'onset_icu'
red.plot_best_model_bar(dist, ax[1][0], 2, 'Onset to ICU entrance', 'b.')
red.plot_violin(dist, 'Onset to ICU entrance', 'g.', ax[1][1])

dist = 'onset_death'
red.plot_best_model_bar(dist, ax[2][0], 4, 'Onset to death', 'c.')
red.plot_violin(dist, 'Onset to death', 'h.', ax[2][1])

dist = 'hosp_stay'
red.plot_best_model_bar(dist, ax[3][0], 1, 'Hospital stay', 'd.')
red.plot_violin(dist, 'Hospital stay', 'i.', ax[3][1])

dist = 'icu_stay'
red.plot_best_model_bar(dist, ax[4][0], 0, 'ICU stay', 'e.')
red.plot_violin(dist, 'ICU stay', 'j.', ax[4][1])

ax[0][0].set_yscale('log')
ax[1][0].set_yscale('log')
ax[2][0].set_yscale('log')
ax[3][0].set_yscale('log')
ax[4][0].set_yscale('log')

import matplotlib.ticker as mticker
ax[0][0].yaxis.set_minor_formatter(mticker.ScalarFormatter())
ax[1][0].yaxis.set_minor_formatter(mticker.ScalarFormatter())
ax[2][0].yaxis.set_minor_formatter(mticker.ScalarFormatter())
ax[3][0].yaxis.set_minor_formatter(mticker.ScalarFormatter())
ax[4][0].yaxis.set_minor_formatter(mticker.ScalarFormatter())

ax[0][0].set_xlabel('')
ax[0][1].set_xlabel('')
ax[0][1].set_xlabel('')
ax[1][0].set_xlabel('')
ax[1][1].set_xlabel('')
ax[2][0].set_xlabel('')
ax[2][1].set_xlabel('')
ax[3][0].set_xlabel('')
ax[3][1].set_xlabel('')

ax[0][1].set_ylabel('')
ax[1][1].set_ylabel('')
ax[2][1].set_ylabel('')
ax[3][1].set_ylabel('')
ax[4][1].set_ylabel('')

fig.savefig(FIG_PATH + 'figure_3_v1.png')


# Option 2
fig, axes = plt.subplot_mosaic([['up', 'up'],['left1', 'right1'],
                                ['left2', 'right2'],['left3', 'right3']],
                              figsize = (10,10))
## Upper panel
wt=0.1
ax = axes['up']
dist = 'onset_hosp'
w=-0.2
red.plot_best_model_bar_all(dist, ax, w, 3, 'a.')
dist = 'onset_icu'
w=-0.1
red.plot_best_model_bar_all(dist, ax, w, 2, 'a.')
dist = 'onset_death'
w= 0
red.plot_best_model_bar_all(dist, ax, w, 4, 'a.')
dist = 'hosp_stay'
w=0.1
red.plot_best_model_bar_all(dist, ax, w, 1, 'a.')
dist = 'icu_stay'
w=0.2
red.plot_best_model_bar_all(dist, ax, w, 0, 'a.')
ax.set_xlabel('')

## Left 1 panel
ax = axes['left1']
dist = 'onset_hosp'
red.plot_violin(dist, 'Days', 'b.', ax)
ax.set_xlabel('')
## Right 1 panel
ax = axes['right1']
dist = 'onset_icu'
red.plot_violin(dist, 'Days', 'c.', ax)
ax.set_xlabel('')
## Left 2 panel
ax = axes['left2']
dist = 'onset_death'
red.plot_violin(dist, 'Days', 'd.', ax)
ax.set_xlabel('')
## Right 2 panel
ax = axes['right2']
dist = 'hosp_stay'
red.plot_violin(dist, 'Days', 'e.', ax)

## Left 3 panel
ax = axes['left3']
dist = 'icu_stay'
red.plot_violin(dist, 'Days', 'f.', ax)

## Right 3 panel -> hide
ax = axes['right3']
ax.axis('off')

## Legends
ax = axes['up']
ax.legend(['Onset to hospitalization', 
           'Onset to ICU entrance',
           'Onset to death',
           'Hospital stay',
           'ICU stay'], 
          bbox_to_anchor=(0.85, 0.25), bbox_transform=fig.transFigure, ncol=1)

fig.tight_layout()
fig.show()
fig.savefig(FIG_PATH + 'figure_3_v2.png')