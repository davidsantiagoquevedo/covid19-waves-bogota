# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 2022
@author: davidsantiagoquevedo
@author: ntorresd
"""     
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from met_brewer import met_brew

config = yaml.load(open("config.yml", "r"))["default"]

DATA_PATH = config['PATHS']['DATA_PATH']
OUT_PATH = config['PATHS']['OUT_PATH'].format(dir = 'genomics')
DATE_GENOMICS = config['UPDATE_DATES']['GENOMICS']

plt.style.use(config['PATHS']['PLOT_STYLE'])
prop_cycle = plt.rcParams['axes.prop_cycle']
colors = prop_cycle.by_key()['color']

# Load data
## Variants
df_variants = pd.read_csv(DATA_PATH + 'variants-ic-bog_'+ DATE_GENOMICS + '.csv')
df_variants['date'] = pd.to_datetime(df_variants['date'])
## Results from multinomial analysis
df_results = pd.read_csv(OUT_PATH + 'theta.csv')

def plot_multinomial(ax):
        stat = "mean"
        n = 0 
        variant = 'Alpha'
        mask = (df_results.stat == stat) & (df_results.variant == variant)
        mask1 = (df_results.stat == 'q025') & (df_results.variant == variant)
        mask2 = (df_results.stat == 'q975') & (df_results.variant == variant)
        ax.plot(df_results[mask].week, df_results[mask].theta, color  = colors[n], label = variant)
        ax.plot(df_results[mask].week, df_results[mask][variant]/df_results[mask].weekly_count_variants, 
                color  = colors[n], marker = '*', linestyle = '')
        ax.fill_between(df_results[mask].week, df_results[mask1].theta, df_results[mask2].theta,
                        color  = colors[n], alpha = 0.2)
        
        n += 1
        variant = 'Delta'
        mask = (df_results.stat == stat) & (df_results.variant == variant)
        mask1 = (df_results.stat == 'q025') & (df_results.variant == variant)
        mask2 = (df_results.stat == 'q975') & (df_results.variant == variant)
        ax.plot(df_results[mask].week, df_results[mask].theta, color  = colors[n], label = variant)
        ax.plot(df_results[mask].week, df_results[mask][variant]/df_results[mask].weekly_count_variants, 
                color  = colors[n], marker = '*', linestyle = '')
        ax.fill_between(df_results[mask].week, df_results[mask1].theta, df_results[mask2].theta,
                        color  = colors[n], alpha = 0.2)
        
        n += 1
        variant = 'Gamma'
        mask = (df_results.stat == stat) & (df_results.variant == variant)
        mask1 = (df_results.stat == 'q025') & (df_results.variant == variant)
        mask2 = (df_results.stat == 'q975') & (df_results.variant == variant)
        ax.plot(df_results[mask].week, df_results[mask].theta, color  = colors[n], label = variant)
        ax.plot(df_results[mask].week, df_results[mask][variant]/df_results[mask].weekly_count_variants, 
                color  = colors[n], marker = '*', linestyle = '')
        ax.fill_between(df_results[mask].week, df_results[mask1].theta, df_results[mask2].theta,
                        color  = colors[n], alpha = 0.2)
    
        n += 1
        variant = 'Mu'
        mask = (df_results.stat == stat) & (df_results.variant == variant)
        mask1 = (df_results.stat == 'q025') & (df_results.variant == variant)
        mask2 = (df_results.stat == 'q975') & (df_results.variant == variant)
        ax.plot(df_results[mask].week, df_results[mask].theta, color  = colors[n], label = variant)
        ax.plot(df_results[mask].week, df_results[mask][variant]/df_results[mask].weekly_count_variants, 
                color  = colors[n], marker = '*', linestyle = '')
        ax.fill_between(df_results[mask].week, df_results[mask1].theta, df_results[mask2].theta,
                        color  = colors[n], alpha = 0.2)
        
        n += 1
        variant = 'Omicron'
        mask = (df_results.stat == stat) & (df_results.variant == variant)
        mask1 = (df_results.stat == 'q025') & (df_results.variant == variant)
        mask2 = (df_results.stat == 'q975') & (df_results.variant == variant)
        ax.plot(df_results[mask].week, df_results[mask].theta, color  = colors[n], label = variant)
        ax.plot(df_results[mask].week, df_results[mask][variant]/df_results[mask].weekly_count_variants, 
                color  = colors[n], marker = '*', linestyle = '')
        ax.fill_between(df_results[mask].week, df_results[mask1].theta, df_results[mask2].theta,
                        color  = colors[n], alpha = 0.2)

# Prevalence histogram
def plot_prevalence(ax):
        agg_df = df_variants.pivot_table(index = 'date', 
                                        columns = 'lineage', 
                                        values = 'PointEst', 
                                        aggfunc = 'max').reset_index()
        initial_date = min(df_variants['date'])
        final_date = max(df_variants['date'])
        bins = len(df_variants['date'].unique())
        variants_hist = sns.histplot(data = df_variants, ax=ax, 
                                     multiple = 'stack', 
                                     weights = 'PointEst', bins = bins, x = 'date', hue = 'lineage', 
                                     legend = True)
        ax.set_xticks(pd.date_range(start = min(df_variants['date']), end = final_date, freq = "M"))
        ax.set_xlim(left = min(df_variants['date']), right = final_date)
        sns.move_legend(variants_hist, 'lower right', bbox_to_anchor = (0.92, 0.95), ncol = 3, title=None)

# Advantage heatmap
def plot_heatmap(ax, n):
        df_mean = pd.read_csv(OUT_PATH + 'advantage_mean.csv')
        df_mean = df_mean.set_index('pivot_variant')
        color_list = met_brew('Cassatt1', n = n, brew_type='continuous')
        sns.heatmap(data = df_mean, annot = False, cmap = color_list, ax = ax)
        ax.set_ylabel('')