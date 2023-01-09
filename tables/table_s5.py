# -*- coding: utf-8 -*-
"""
Created on Mon Nov 28 2022
@author: davidsantiagoquevedo
@author: ntorresd
"""  
import warnings
warnings.filterwarnings('ignore')

import sys
import yaml
import pandas as pd

config = yaml.load(open("config.yml", "r"))["default"]

DIST_PATH = config['PATHS']['OUT_PATH'].format(dir = 'epidemiological_distributions')
OUT_PATH = config['PATHS']['OUT_PATH'].format(dir = 'tables')

df_summary = pd.read_csv(DIST_PATH + "best_fit_summary.csv").set_index("stat")
waves = [col for col in df_summary.columns if "wave" in col]

dict_epi_distri   = {'onset_hosp': 'Onset to hosp',
                        'onset_icu': 'Onset to ICU',
                        'onset_death': 'Onset to death',
                        'hosp_stay':'Hosp. stay',
                        'icu_stay': 'ICU stay'
                        }

def get_mean_var_dist(dist):
    mean = []
    var  = []
    df_dist = {"Wave" : [1,2,3,4],
            "Delay time" : [dist]*len(waves)
            }
    for wv in waves:
        df_temp = df_summary[df_summary["dist"] == dist]
        mn = round(df_temp[wv].loc["mean"], 2)
        mn_q1 = round(df_temp[wv].loc["q025"], 2)
        mn_q2 = round(df_temp[wv].loc["q975"], 2)
        if mn_q1 > mn_q2:
            temp = mn_q1
            mn_q1 = mn_q2
            mn_q2 = temp
            
        vr = round(df_temp[wv].loc["var_mean"], 2)
        vr_q1 = round(df_temp[wv].loc["var_q025"], 2)
        vr_q2 = round(df_temp[wv].loc["var_q975"], 2)
        
        if vr_q1 > vr_q2:
            temp = vr_q1
            vr_q1 = vr_q2
            vr_q2 = temp
            
        mean.append(str(mn)+" ("+str(mn_q1)+", "+str(mn_q2)+")")
        var.append(str(vr)+" ("+str(vr_q1)+", "+str(vr_q2)+")")
    df_dist.update({"Mean (days)" : mean, "Var (days²)" : var})
    return pd.DataFrame(df_dist)

df_final = pd.DataFrame({})
for dist in dict_epi_distri.keys():
    df_final = pd.concat([df_final, get_mean_var_dist(dist)])    
    
df_final = df_final.replace(dict_epi_distri)
df_final.to_csv(OUT_PATH + "table_s5.csv", index = False)