# -*- coding: utf-8 -*-
"""
Created on Thr Jul 31 2022

@author: dsquevedo
@author: ntorresd
"""

import yaml
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

# Load configuration
ymlfile = open("config.yml", "r")
cfg = yaml.load(ymlfile)
config = cfg["default"]

# Paths
DATA_PATH = config['PATHS']['DATA_PATH']
OUT_PATH = config['PATHS']['OUT_PATH'].format(dir = 'severe_outcomes')
FIG_PATH = config['PATHS']['FIG_PATH'].format(dir = 'severe_outcomes')

# Plot style
plt.style.use(config['PATHS']['PLOT_STYLE'])
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

# Read data 
strat = 'wave'
# percentages
df_hosp_perc = pd.read_csv(OUT_PATH + 'hosp_percentages.csv')
df_icu_perc = pd.read_csv(OUT_PATH + 'icu_percentages.csv')
df_death_perc = pd.read_csv(OUT_PATH + 'deaths_percentages.csv')
df_hosp_perc[strat] = df_hosp_perc[strat].astype(int)
df_icu_perc[strat] = df_icu_perc[strat].astype(int)
df_death_perc[strat] = df_death_perc[strat].astype(int)
# proportions
df_proportions_all = pd.read_csv(OUT_PATH+'proportions_all.csv')
df_proportions_60p = pd.read_csv(OUT_PATH+'proportions_60p.csv')
# rates 
df_rates = pd.read_csv(OUT_PATH+'rates.csv')

# Auxiliar plot function
def plot_xyvar(df, ax, n_strat, varx='age_group', vary='percentage'):
    data = df.loc[df[strat]==n_strat]
    ax.plot(data[varx], data[vary], label=strat+str(n_strat), linestyle='-', marker='o')

# Wave cases percentage distribution by age group
def plot_percentage(ax):
    vary = 'percentage'
    strat_list = df_hosp_perc[strat].unique()
    for n_strat in strat_list:
        plot_xyvar(df_hosp_perc, ax=ax[0], n_strat=n_strat, vary=vary)
        plot_xyvar(df_icu_perc, ax=ax[1], n_strat=n_strat, vary=vary)
        plot_xyvar(df_death_perc, ax=ax[2], n_strat=n_strat, vary=vary)

fig, ax = plt.subplots(1, 3, figsize=(15, 5))
plot_percentage(ax)
ax[0].set_ylabel('hospitalization percentage by age')
ax[1].set_ylabel('icu percentage by age')
ax[2].set_ylabel('death percentage by age')
for axi in ax:
    axi.tick_params(axis='x', labelrotation=90)
    axi.set_xlabel('age group')
handles, labels = ax[2].get_legend_handles_labels()
ax[2].legend(handles, labels, loc='upper left')
# fig.savefig(FIG_PATH+'hosp_icu_death_percentages.png')
# fig.show()

# Wave counts by age group
def plot_counts(ax):
    strat_list = df_hosp_perc[strat].unique()
    vary = 'counts'
    for axi in ax:
        axi.tick_params(axis='x', labelrotation=90)
        axi.set_ylabel(vary)
        axi.set_xlabel('age group')
    for wave in strat_list:
        plot_xyvar(df_hosp_perc, ax=ax[0], n_strat=wave, vary=vary)
        plot_xyvar(df_icu_perc, ax=ax[1], n_strat=wave, vary=vary)
        plot_xyvar(df_death_perc, ax=ax[2], n_strat=wave, vary=vary)

fig, ax = plt.subplots(1, 3, figsize=(15, 5))
plot_counts(ax)
handles, labels = ax[0].get_legend_handles_labels()
fig.legend(handles, labels, bbox_to_anchor = (0.8, -0.03), ncol = len(labels)) 
fig.savefig(FIG_PATH+'hosp_icu_death_counts.png')
# fig.show()

# Stacked histogram of cases by wave and age group
from met_brewer import met_brew
#  Package installation : https://github.com/BlakeRMills/MetBrewer

def plot_stacked_histogram(df, ax, strat=strat, group_var='age_group', vary='counts', pallete='VanGogh1'): 
    strat_list = df[strat].unique()
    group_list = df[group_var].unique()
    color_list = met_brew(pallete, n=len(group_list), brew_type='continuous')
    
    y_offset = np.zeros(len(strat_list))
    counter=0
    for group in group_list:
        mask = (df[group_var]==group)
        counts_list =  df.loc[mask][vary].values
        ax.bar(strat_list, counts_list, label=group, bottom=y_offset, color=color_list[counter]) 
        y_offset = y_offset + counts_list 
        counter+=1

def plot_counts_histograms(ax, strat=strat, group_var='age_group', vary='counts'):

    plot_stacked_histogram(df = df_hosp_perc, ax=ax[0], strat=strat, group_var=group_var, vary=vary)
    plot_stacked_histogram(df = df_icu_perc, ax=ax[1], strat=strat, group_var=group_var, vary=vary)
    plot_stacked_histogram(df = df_death_perc, ax=ax[2], strat=strat, group_var=group_var, vary=vary)


vary='counts'
fig, ax = plt.subplots(1, 3, figsize=(15,5))
for axi in ax:
    axi.set_xlabel(strat)
ax[0].set_ylabel('hospitalization counts by age')
ax[1].set_ylabel('icu counts by age')
ax[2].set_ylabel('death counts by age')
plot_counts_histograms(ax)
fig.savefig(FIG_PATH+'hosp_icu_death_counts_hist.png') 
# fig.show()

# Proportion histogram with binomial confidence interval
# Auxiliar plot function
def plot_proportions_histogram(df, ax, outcome_var, prop_lower, prop_upper, strat=strat, group='all',side='center', width=0.3):
    proportions = df[outcome_var].values
    yerr_lower = proportions - df[prop_lower].values
    yerr_upper = df[prop_upper].values - proportions
    yerr = [yerr_lower, yerr_upper]
    if side=='center':
        ax.bar(df[strat], proportions, yerr=yerr, width=width, label=group)
    elif side=='left':
        ax.bar(df[strat]-width/2, proportions, yerr=yerr, width=width, label=group)
    elif side=='right':
        ax.bar(df[strat]+width/2, proportions, yerr=yerr, width=width, label=group)
    
def plot_proportions_hist(ax):
    plot_proportions_histogram(df_proportions_all, ax[0], 
                        outcome_var='hosp', prop_lower='hosp_lower', prop_upper='hosp_upper', side='left', group='all')
    plot_proportions_histogram(df_proportions_60p, ax[0], 
                        outcome_var='hosp', prop_lower='hosp_lower', prop_upper='hosp_upper', side='right', group='60+')

    plot_proportions_histogram(df_proportions_all, ax[1], 
                        outcome_var='icu', prop_lower='icu_lower', prop_upper='icu_upper', side='left', group='all')
    plot_proportions_histogram(df_proportions_60p, ax[1], 
                        outcome_var='icu', prop_lower='icu_lower', prop_upper='icu_upper', side='right', group='60+')

    plot_proportions_histogram(df_proportions_all, ax[2], 
                        outcome_var='death', prop_lower='death_lower', prop_upper='death_upper', side='left', group='all')
    plot_proportions_histogram(df_proportions_60p, ax[2], 
                        outcome_var='death', prop_lower='death_lower', prop_upper='death_upper', side='right', group='60+')

# Rates
def plot_rates(ax, var, var_name):
    for wave in range(1,5):
        df_temp = df_rates[df_rates['wave'] == wave]
        ax.plot(df_temp['age_group'], df_temp[var], marker = 'o', label = 'wave '+str(wave), color = colors[wave-1])
    ax.set_xlabel('age group')
    ax.set_ylabel(var_name)
# CFR
fig, ax = plt.subplots()
var = 'CFR'
var_name = 'CFR'
plot_rates(ax, var, var_name)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc='upper left',numpoints=1)
fig.savefig(FIG_PATH + f'{var}.png')

# HCR
fig, ax = plt.subplots()
var = 'HCR'
var_name = 'HCR'
plot_rates(ax, var, var_name)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc='upper left',numpoints=1)
fig.savefig(FIG_PATH + f'{var}.png')

# HCR - I
fig, ax = plt.subplots()
var = 'HCR_I'
var_name = 'HCR - ICU'
plot_rates(ax, var, var_name)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc='upper left',numpoints=1)
fig.savefig(FIG_PATH + f'{var}.png')

# HFR - I
fig, ax = plt.subplots()
var = 'HFR'
var_name = 'HFR'
plot_rates(ax, var, var_name)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc='upper left',numpoints=1)
fig.savefig(FIG_PATH + f'{var}.png')

# HFR - I
fig, ax = plt.subplots()
var = 'HFR_I'
var_name = 'HFR - ICU'
plot_rates(ax, var, var_name)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc='upper left',numpoints=1)
fig.savefig(FIG_PATH + f'{var}.png')