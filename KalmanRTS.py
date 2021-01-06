# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 18:46:13 2020

@author: bcyat
"""
from readVisual import readVisual
import statistics as stat
import numpy as np
from scipy.linalg import expm, sinm, cosm

visOut = readVisual('D1')
posVis = visOut[0]
timeVis = visOut[2]


dt = stat.mean(np.diff(timeVis))
F = [[0, 1, 0],
     [0, 0, 1],
     [0, 0, 0]]
F = np.array(F)
R = .1**2
L = np.array([[0],[0],[1]])
H = [1, 0, 0]
m0 = [[0],[0],[0]]
p0 = np.eye(3)*10000

qc_list = list(range(45,130,10))
lh_list = np.zeros(np.size(qc_list))


q = qc_list[0]
#From https://github.com/probml/pmtksupport/blob/master/ekfukf1.2/lti_disc.m
A = expm(F*dt)
# Line 79
n = np.size(F,0)

# Line 80
tl = np.transpose(L)
tf = np.transpose(F)
tst = L*q*tl
topLeft = F.astype(int)
topRight = L*q*tl
topRight = topRight.astype(int)
botLeft = np.zeros((n,n))
botRight = -tf
bottom = np.concatenate((botLeft,botRight), axis = 1)
top = np.concatenate((topLeft,topRight), axis = 1)
phi = np.concatenate((top,bottom), axis = 0)
    
 # Line 81   
ab1 = expm(phi*dt)
ab2 = np.concatenate((np.zeros((n,n)),np.eye(n)), axis = 0)
AB = np.matmul(ab1,ab2)

# Line 82
Q1 = AB[0:n,:]
Q2 = AB[(n):(2*n),:]
Q = np.linalg.lstsq(Q2, Q1.T)[0].T


