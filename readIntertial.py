# -*- coding: utf-8 -*-
"""
Created on Mon Nov  9 12:57:44 2020

@author: bcyat
"""

import numpy as np


dataset = 'D1'
    
basePath = 'data/' + dataset + '/'    

fileID = open(basePath + 'accelerometer.txt')
lines = fileID.readlines()
accArray = []

for row in lines:
    rowArray = row.split()
    
    rowArray = [float(i) for i in rowArray]
    accArray.append(rowArray)
    
    timeAcc = [i[0] for i in accArray]
    timeAcc = np.divide(timeAcc, 10**9)
print(accArray)

accImu = [[i[1] for i in accArray], [i[2] for i in accArray], [i[3] for i in accArray]]

fileID = open(basePath + 'gyroscope.txt')
lines = fileID.readlines()
gyrArray = []

for row in lines:
    rowArray = row.split()
    
    rowArray = [float(i) for i in rowArray]
    gyrArray.append(rowArray)
    
    timeGyr = [i[0] for i in gyrArray]
    timeGyr = np.divide(timeGyr, 10**9)
print(gyrArray)

gyrImu = [[i[1] for i in gyrArray], [i[2] for i in gyrArray], [i[3] for i in gyrArray]]

dtAcc = np.diff(timeAcc)
dtAcc = sum(dtAcc)/len(dtAcc)

dtGyr = np.diff(timeGyr)
dtGyr = sum(dtGyr)/len(dtGyr)

t1 = min([timeAcc[0], timeGyr[0]])
timeImu = timeAcc - t1
angImu = np.interp(timeGyr-t1, gyrImu, timeImu)