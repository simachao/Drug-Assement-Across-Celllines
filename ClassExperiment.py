#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  3 14:31:53 2018

@author: csima
"""
import pandas
import os.path
import numpy as np

class Experiment:
    """Experiment."""

    # A class variable, counting the number of experiments
    total = 0

    def __init__(self, name,datapath):
        """Initializes the data."""
        self.preTreatmentTPs = 2
        self.name = name
        self.datapath = datapath
        #print("(Initializing {})".format(self.name))
        Experiment.total += 1
        
        self.load()
        
    def __del__(self):
        Experiment.total -= 1
        

    def report(self,what):
        
        if what == 'init':
            print("***This is a new experiment out of total {0}, with name {1}.".format(self.total,self.name))
            print("\tNum of time points = {}".format(len(self.timepoints)))
            print("\tCelllines {}".format(self.cells))
            print("\tDrugs {}".format(self.drugs))
    
    
    def load(self):
        """load data from csv file."""

        self.get_timepoints()
        self.get_apop_pcts()

    def calc(self):
        self.auc = self.numbers.mean(axis=1)
        self.auc = self.auc.values.tolist()

        self.lastTimePoint = self.numbers.iloc[:,-1]
        
        self.calc_cross_time()

    def calc_cross_time(self):
        #first time cross a percentage
        
        pctThresholds = [0.9,0.95,0.99]
        columns =  ['p'+str(int(x*100)) for x in pctThresholds]
        crossTime = pandas.DataFrame(-1*np.ones((len(self.auc),len(pctThresholds)),dtype=np.int8), columns=columns)

        #print(crossTime)
        
        for pctThreshold in pctThresholds:
            col = 'p'+str(int(pctThreshold*100))
            
            bool_aboveThreshold = self.numbers >= pctThreshold #Pandas dataframe
        
            for index, row in bool_aboveThreshold.iterrows():
                cross_at = np.where(list(bool_aboveThreshold.iloc[index,:]))[0]
                if cross_at.size > 0:
                    crossTime[col][index] = cross_at[0] - self.preTreatmentTPs
                    
        #print(crossTime)
        self.crossTime = crossTime


        
        
        
    def get_timepoints(self):
        df = pandas.read_csv(os.path.join(self.datapath, self.name+'.csv'),nrows=1,header=None)
        df = df.drop(0,axis=1)
        self.timepoints = df.iloc[0]
        
    def get_apop_pcts(self):
        self.numbers = pandas.read_csv(os.path.join(self.datapath, self.name+'.csv'),skiprows=1,header=None)
        self.cases = self.numbers[0].str.split(':',expand=True)
        self.cases.columns = ['datatype', 'cell','drug']
        self.numbers = self.numbers.drop(0,axis=1)
        
        self.cells = set(self.cases['cell'])
        self.drugs = set(self.cases['drug'])
        
        
    @classmethod
    def Summary(cls):
        print("***There are a total of [{:d}] experiments***".format(cls.total))
        print("\n\n\n".format(cls.total))
