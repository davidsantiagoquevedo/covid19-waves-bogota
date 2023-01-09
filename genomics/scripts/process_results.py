# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 2022
@author: davidsantiagoquevedo
@author: cwhittaker1000
@author: ntorresd
"""
import yaml
import pandas as pd
import numpy as np

config = yaml.load(open("config.yml", "r"))["default"]

DATA_PATH = config['PATHS']['DATA_PATH']
OUT_PATH = config['PATHS']['OUT_PATH'].format(dir = 'genomics')
FIG_PATH = config['PATHS']['FIG_PATH'].format(dir = 'genomics')
DATE_GENOMICS = config['UPDATE_DATES']['GENOMICS']

# Load raw fitting data
df_fit_raw = pd.read_csv(OUT_PATH + 'fit_raw.csv')
df_variants = pd.read_csv(DATA_PATH + 'variants_pivot.csv')

# 2.5th Percentile
def q025(x):
    return x.quantile(0.025)
# 97.5th Percentile
def q975(x):
    return x.quantile(0.975)

#################################################################################################
# Prepare results
variants_dict = {'1' : 'Alpha',
                 '2' : 'Delta',
                 '3' : 'Gamma',
                 '4' : 'Mu',
                 '5' : 'Omicron'
            }
#################################################################################################
#################################################################################################
#theta
theta_cols = [col for col in df_fit_raw.columns if 'theta' in col]
df_theta = df_fit_raw[theta_cols]
df_theta_mean =  df_theta.agg(['mean', q025, q975])
df_theta_mean.reset_index(inplace = True)
df_theta_mean.rename(columns = {'index' : 'stat'}, inplace = True)
df_theta_mean = pd.melt(df_theta_mean, id_vars=['stat'])
df_theta_mean = df_theta_mean.rename(columns = {'value' : 'theta'})
df_theta_mean[['trash1','week_var']] = df_theta_mean['variable'].str.split('[', 1, expand = True)
df_theta_mean[['week','variant']] = df_theta_mean['week_var'].str.split(',', 1, expand = True)
df_theta_mean[['variant', 'thash2']] = df_theta_mean['variant'].str.split(']', 1, expand = True)
df_theta_mean = df_theta_mean[['week','variant','stat','theta']]
df_theta_mean['week'] = df_theta_mean['week'].astype(int) - 1 #Shifting weeks by -1 to make them coherent with the variant counts
df_theta_mean.replace({"variant": variants_dict}, inplace = True)

# Variant counts - week
df_variants['weekly_count_variants'] = df_variants['Alpha'] + df_variants['Delta'] + df_variants['Gamma'] + df_variants['Mu'] + df_variants['Omicron']
df_variants['t'] = df_variants['t'].astype(int)
df_theta_mean = df_theta_mean.merge(df_variants, how = 'left', right_on = 't', left_on = 'week')
del(df_theta_mean['t'])
df_theta_mean.sort_values(by = ['variant', 'week'], inplace = True)
df_theta_mean.to_csv(OUT_PATH + 'theta.csv', index = False)

#################################################################################################
#################################################################################################
#beta
beta_cols = [col for col in df_fit_raw.columns if 'beta[' in col]
df_beta = df_fit_raw[beta_cols]
df_beta_mean =  df_beta.agg(['mean', q025, q975])
cols = list(variants_dict.values())
df_beta_mean.columns = cols
# Notice that these beta's are the advantage of variants 2-5 with respect to variant 1 (which is the pivot). In order to get the advantage
# between the others, we should subtract them

def calculate_relative_advantage(stat):
    df_beta_cp = df_beta.copy()
    df_result = pd.DataFrame({})
    for piv_var in list(variants_dict.keys()):  
        advantage_list =[variants_dict[piv_var]]
        for var in list(variants_dict.keys()):
            advantage = df_beta_cp[f'beta[{var}]']-df_beta_cp[f'beta[{piv_var}]']
            adv = advantage.agg(stat)
            advantage_list.append(adv)
        df_temp = pd.DataFrame([advantage_list], columns = ['pivot_variant'] + cols)
        df_result = pd.concat([df_result, df_temp])

    return df_result.round(2).reset_index(drop = True)

df_mean = calculate_relative_advantage('mean')
df_025 = calculate_relative_advantage(q025)
df_975 = calculate_relative_advantage(q975)

df_mean.to_csv(OUT_PATH + 'advantage_mean.csv', index = False)
df_025.to_csv(OUT_PATH + 'advantage_025.csv', index = False)
df_975.to_csv(OUT_PATH + 'advantage_975.csv', index = False)