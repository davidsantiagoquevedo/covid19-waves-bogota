# -*- coding: utf-8 -*-
"""
Created on Sun Nov 20 2022
Adapted from: https://github.com/mrc-ide/Brazil_COVID19_distributions
@author: davidsantiagoquevedo
@author: ntorresd
"""
import yaml
import sys
import pandas as pd
import time
import pystan

t0 = time.time()
config = yaml.load(open("config.yml", "r"))["default"]

DATA_PATH = config['PATHS']['DATA_PATH']
OUT_PATH = config['PATHS']['OUT_PATH'].format(dir = 'epidemiological_distributions')
FIG_PATH = config['PATHS']['FIG_PATH'].format(dir = 'epidemiological_distributions')
SCRIPTS_PATH = config['PATHS']['SCRIPTS_PATH'].format(dir = 'epidemiological_distributions')
UTILS_PATH = config['PATHS']['UTILS_PATH'].format(dir = 'epidemiological_distributions')

sys.path.append(UTILS_PATH)
import utilities_epi_dist as ut

SEED = config['MODELS']['SEED']
ITER = config['MODELS']['ITER']
CHAINS = config['MODELS']['CHAINS']
MIN_VAL = config['MODELS']['MIN_VAL']
MAX_VAL = config['MODELS']['MAX_VAL']

# Model variables
strat_name = 'wave'
n_strats = 4
params = ['beta']

# 1. Prepare the data
all_dfs, columns = ut.prepare_confirmed_cases_data()

# 2. Load stan district-level model
model_district = pystan.StanModel(file = SCRIPTS_PATH + 'model_exponential_district.stan')
# 3. Run district-level model
district_posteriors = ut.get_posteriors_district(params, columns, all_dfs, model_district)

# 4. Load partial-pooling model
model = pystan.StanModel(file = SCRIPTS_PATH + 'model_exponential_pool.stan')
# 5. Run model
ut.get_posteriors_pooling(all_dfs, columns, model, 'exponential', params, district_posteriors, n_strats, strat_name)

print('Exponential model fits done')
print('Time elapsed: ', round((time.time()-t0)/60,1), ' minutes')