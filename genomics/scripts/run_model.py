# -*- coding: utf-8 -*-
"""
Created on Fri Oct 21 2022
@author: davidsantiagoquevedo
@author: cwhittaker1000
@author: ntorresd
"""
import yaml
import pandas as pd
import pystan
import time

ymlfile = open("config.yml", "r")
cfg = yaml.load(ymlfile)
config = cfg['default']

DATA_PATH = config['PATHS']['DATA_PATH']
OUT_PATH = config['PATHS']['OUT_PATH'].format(dir = 'genomics')
FIG_PATH = config['PATHS']['FIG_PATH'].format(dir = 'genomics')
SCRIPTS_PATH = config['PATHS']['SCRIPTS_PATH'].format(dir = 'genomics')

SEED = config['MODELS']['SEED']
ITER = config['MODELS']['ITER']
CHAINS = config['MODELS']['CHAINS']

t0 = time.time()

# Prepare data
df_variants = pd.read_csv(DATA_PATH + 'variants_pivot.csv')
variants_counts = df_variants[['Alpha', 'Delta', 'Gamma', 'Mu', 'Omicron']]
for col in variants_counts.columns:
    variants_counts[col] = variants_counts[col].astype(int)
time_vect = df_variants.t.to_list()

# Load and run model
multinomial_model = pystan.StanModel(file = SCRIPTS_PATH + 'multinomial_model.stan')
stan_data = {'K': len(variants_counts.columns),
             'N': len(time_vect),
             'y': variants_counts.values,
             'time': time_vect}
fit = multinomial_model.sampling(data=stan_data, iter=ITER, seed=SEED, chains=CHAINS, n_jobs=-1)
df_fit = fit.to_dataframe()
df_fit.to_csv(OUT_PATH + 'fit_raw.csv', index = False)
print('Multinomial model fits done')
print('Time elapsed: ', round((time.time()-t0)/60,1), ' minutes')