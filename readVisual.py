# -*- coding: utf-8 -*-
"""
Created on Sun Nov  8 22:20:58 2020

@author: bcyat
"""
import numpy as np


def readVisual(dataset):
    
    basePath = 'data/' + dataset + '/'    
    fileID = open(basePath + 'poses.txt')
    lines = fileID.readlines()
    
    posArray = []
    for row in lines:
        rowArray = row.split()
        
        rowArray = [float(i) for i in rowArray]
        posArray.append(rowArray)
    
    timeVis = [i[0] for i in posArray]
    timeVis = np.divide(timeVis, 10**9)
    
    posVis = [[i[1] for i in posArray], [i[2] for i in posArray], [i[3] for i in posArray]]
    qtVis = [[i[4] for i in posArray], [i[5] for i in posArray], [i[6] for i in posArray], [i[7] for i in posArray]]
    
    try:
        GT = open(basePath + "groundtruth.txt")
        GT = GT.readlines()
        scaleGT = float(GT[0])
    except:
        print('no ground truth')
        scaleGT = None

    return [posVis, qtVis, timeVis, scaleGT]

#output = readVisual('D1')
