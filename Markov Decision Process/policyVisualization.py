# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 00:13:21 2018

@author: Giridhar
"""
import pprint as pp
import numpy as np
def visualizePolicy(policyMatrix):
    printMatrix=[['n' for row in range(0,len(policyMatrix))] for col in range(0,len(policyMatrix[0]))]
    for i in range(len(policyMatrix)):
        for j in range(len(policyMatrix[0])):
            if policyMatrix[i,j]==0:
                printMatrix[i][j]='^'
            elif policyMatrix[i,j]==1:
                printMatrix[i][j]='<'
            elif policyMatrix[i,j]==2:
                printMatrix[i][j]='v'
            elif policyMatrix[i,j]==3:
                printMatrix[i][j]='>'
            else:
                printMatrix[i][j]='o'
    pp.pprint(printMatrix)

f = open("policy2.txt")
policyMatrix=np.full((10,10),9)
d={}
d['0,-1']=0
d['-1,0']=1
d['0,1']=2
d['1,0']=3
d['None']=9
line=f.readlines()
bad_chars='()\n\r '
for i in range(100,200):
    x="".join(c for c in line[i] if c not in bad_chars).split(':')
    y=x[0].split(',')
    y=list(reversed(y))
    policyMatrix[int(y[0]),int(y[1])]=d[x[1]]