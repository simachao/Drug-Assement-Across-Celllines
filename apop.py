#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 14:31:53 2018

@author: csima
"""

#from IPython import get_ipython
#get_ipython().magic('reset -sf')

import IPython
IPython.get_ipython().magic('reset -sf')


import os
import os.path
#import glob
#import fnmatch

import ClassExperiment as ce
import plots as myplot



#%% get experiment names

data_folder = 'data'
all_exps_files = os.listdir(data_folder)


#filter: csv files only
all_exps_files = [name for name in all_exps_files
    if os.path.isfile(os.path.join(data_folder, name))]

all_exps_files = [name for name in all_exps_files
    if name.endswith('.csv')]

all_exps = [os.path.splitext(f)[0] for f in all_exps_files]


#%% populate exps (a list)
exps = []
for exp in all_exps:
    new_exp = ce.Experiment(exp,data_folder)
    new_exp.report('init')
    exps.append(new_exp)
    
ce.Experiment.Summary()



#%% calculations
selected_drugs = set()
for i in range(0,ce.Experiment.total):
    #print(i)
    exps[i].calc()
    selected_drugs.update(exps[i].drugs)
    

#%% plots
dictAUC = dict.fromkeys(selected_drugs)
dictLastTP = dict.fromkeys(selected_drugs)
#dictCT = dict.fromkeys(selected_drugs)

dictCTs = []

pctThresholds = ['p90','p95','p99']
for i in range(0,len(pctThresholds)):
    dictCTs.append(dict.fromkeys(selected_drugs))


for drug in selected_drugs:
    dictAUC[drug] = []
    dictLastTP[drug] = []
    for i in range(0,len(pctThresholds)):
        dictCTs[i][drug] = []
        
    for i in range(0,ce.Experiment.total):
        if drug in exps[i].drugs:
            drug_list = exps[i].cases['drug'].values.tolist()
            drugIdxRange = range(0,len(drug_list))
            
            matched_auc = [exps[i].auc[idx] for idx in drugIdxRange if drug_list[idx] == drug]
            dictAUC[drug].extend(matched_auc)
            
            matched_lastTP = [exps[i].lastTimePoint[idx] for idx in drugIdxRange if drug_list[idx] == drug]
            dictLastTP[drug].extend(matched_lastTP)
            
            for j in range(0,len(pctThresholds)):
                matched_ct = [exps[i].crossTime[pctThresholds[j]][idx] for idx in drugIdxRange if drug_list[idx] == drug]
                dictCTs[j][drug].extend(matched_ct)

# this produces barplot
myplot.barplot(dictAUC,'AUC')
myplot.barplot(dictLastTP,'Last Time Point')
for i in range(0,len(pctThresholds)):
    myplot.barplot(dictCTs[i],pctThresholds[i])

# this produces violoinplot 
myplot.violinplot(dictAUC,'AUC')
myplot.violinplot(dictLastTP,'Last Time Point')
for i in range(0,len(pctThresholds)):
    myplot.violinplot(dictCTs[i],pctThresholds[i])

