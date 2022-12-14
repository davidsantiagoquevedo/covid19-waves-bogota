# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 2022

@author: dsquevedo
@author: cwhittaker
@author: ntorres
"""     
import yaml
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from met_brewer import met_brew

ymlfile = open("config.yml", "r")
cfg = yaml.load(ymlfile)
config = cfg["default"]

DATA_PATH = config['PATHS']['DATA_PATH']
OUT_PATH = config['PATHS']['OUT_PATH'].format(dir = 'genomics')
FIG_PATH = config['PATHS']['FIG_PATH'].format(dir = 'genomics')
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

stat = "mean"

def plot_multinomial(ax):
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
        ax.legend(loc = 'center right')

fig, ax = plt.subplots()
plot_multinomial(ax)
ax.set_xlabel('week')
ax.set_ylabel('prevalence')
fig.legend(loc = 'center right')
fig.savefig(FIG_PATH + 'variants_multinomial.png')
# fig.show()

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
        sns.move_legend(variants_hist, 'lower right', bbox_to_anchor = (0.90, 0.95), ncol = 3, title=None)

fig, ax = plt.subplots(figsize = (7.5,5))
plot_prevalence(ax)
ax.set_xlabel('')
ax.set_ylabel('prevalence')
ax.tick_params(axis = 'x', rotation = 45)
fig.savefig(FIG_PATH + 'variants_prevalence_' + DATE_GENOMICS + '.png')
# fig.show()

# Advantage heatmap

fig, ax = plt.subplots()
def plot_heatmap(ax, n):
        df_adv = pd.read_csv(OUT_PATH + 'advantage.csv')
        df_mean = pd.DataFrame({})
        df_mean['pivot_variant'] = df_adv['pivot_variant']
        for col in df_adv.columns.to_list()[1:]:
                df_mean[[col,'trash']] = df_adv[col].str.split(' ', 1, expand = True)
                df_mean[col] = df_mean[col].astype(float)
                del(df_mean['trash'])
        df_adv = df_adv.set_index('pivot_variant')
        df_mean = df_mean.set_index('pivot_variant')
        df_mean = df_mean.replace(1,0)
        
        color_list = met_brew('VanGogh1', n = n, brew_type='continuous')

        sns.heatmap(data = df_mean, annot = True, cmap = color_list, ax = ax)
        ax.set_ylabel('')