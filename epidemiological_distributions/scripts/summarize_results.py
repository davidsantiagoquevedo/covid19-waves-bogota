# -*- coding: utf-8 -*-
"""
Created on Wed Oct 12 2022
Adapted from: https://github.com/mrc-ide/Brazil_COVID19_distributions

@author: dsquevedo
@author: ntorres
"""
import yaml
import pandas as pd
import numpy as np

ymlfile = open("config.yml", "r")
cfg = yaml.load(ymlfile)
config = cfg["default"]

OUT_PATH = config['PATHS']['OUT_PATH'].format(dir = 'epidemiological_distributions')
UTILS_PATH = config['PATHS']['UTILS_PATH'].format(dir = 'epidemiological_distributions')

import sys
sys.path.append(UTILS_PATH)
import utilities as ut

df_best_models = pd.read_csv(OUT_PATH + 'best_models.csv')
df_best_models = df_best_models.set_index(df_best_models.columns[0]).transpose()

# 1. Prepare the data
all_dfs, columns = ut.prepare_confirmed_cases_data()

stats = ['mean', ut.q975, ut.q025]
dist_posteriors = ut.load_samples(stats)


def get_mean_best(dist, df_best_models):
    best = df_best_models[df_best_models[dist] == 0].index[0]
    df_temp = dist_posteriors[dist][best]

    df_result = {'stat' : df_temp.index.tolist(),
                 'dist' : [dist]*len(df_temp.index.tolist())
                 }
    for wave in range(1,5):
        wave_mean = []
        for stat in df_result['stat']:
            if best == 'Gamma':
                alpha = df_temp[f'alpha[{wave}]'][stat]
                beta = df_temp[f'beta[{wave}]'][stat]
                mn = ut.mean_gamma(alpha, beta)
                wave_mean.append(mn)
            if best == 'Exponential':
                beta = df_temp[f'beta[{wave}]'][stat]
                mn = ut.mean_exponential(beta)
                wave_mean.append(mn)
            if best == 'Weibull':
                alpha = df_temp[f'alpha[{wave}]'][stat]
                sigma = df_temp[f'sigma[{wave}]'][stat]
                mn = ut.mean_weibull(alpha, sigma)
                wave_mean.append(mn)
            if best == 'Lognormal':
                mu = df_temp[f'mu[{wave}]'][stat]
                sigma = df_temp[f'sigma[{wave}]'][stat]
                mn = ut.mean_log_normal(mu, sigma)
                wave_mean.append(mn)
            if best == 'Gen Lognormal':
                print('Entró')
                mu = df_temp[f'mu[{wave}]'][stat]
                sigma = df_temp[f'sigma[{wave}]'][stat]
                g = df_temp[f'g[{wave}]'][stat]
                mn = ut.mean_gln(mu, sigma, g)
                wave_mean.append(mn)
        df_result.update({'wave_' + str(wave) : wave_mean})

    return pd.DataFrame(df_result)

def get_mean_observed(all_dfs, dist):
    dist_di = {'icu_stay' : 0,
               'hosp_stay' : 1,
               'onset_icu' : 2,
               'onset_hosp' : 3,
               'onset_death' : 4,
               }
    df_result = {'stat' : ['observed'],
                 'dist' : [dist]
                 }
    
    df_dist = all_dfs[dist_di[dist]]
    for wave in range(1,5):
        df_temp = df_dist[df_dist['wave'] == wave]
        wave_mean = df_temp[dist].mean()
        df_result.update({'wave_' + str(wave) : [wave_mean]})
    return pd.DataFrame(df_result)
    
df_res = pd.DataFrame({})
dist = 'hosp_stay'
df_res = pd.concat([df_res, get_mean_best(dist, df_best_models), get_mean_observed(all_dfs, dist)])
dist = 'icu_stay'
df_res = pd.concat([df_res, get_mean_best(dist, df_best_models), get_mean_observed(all_dfs, dist)])
dist = 'onset_hosp'
df_res = pd.concat([df_res, get_mean_best(dist, df_best_models), get_mean_observed(all_dfs, dist)])
dist = 'onset_icu'
df_res = pd.concat([df_res, get_mean_best(dist, df_best_models), get_mean_observed(all_dfs, dist)])
dist = 'onset_death'
df_res = pd.concat([df_res, get_mean_best(dist, df_best_models), get_mean_observed(all_dfs, dist)])
        
df_res.to_csv(OUT_PATH + 'best_fit_summary.csv', index = False)