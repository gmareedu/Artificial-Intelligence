# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 17:38:56 2018

@author: Giridhar
"""

import numpy as np;
import pprint as pp;
x=np.full((3,3),-1)
x[0,0]+=100
x[1,0]-=100
class Coordinate():
    def __init__(self,x,y):
        self.x=x
        self.y=y

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

def findManhattanDistance(x,y,gx,gy):
    return abs(x-gx)+abs(y-gy)-1
def initializeMatrix(valueMatrix,goal):
    for i in range(len(valueMatrix)):
        for j in range(len(valueMatrix[0])):
            valueMatrix[i,j]+=len(valueMatrix)-findManhattanDistance(i,j,goal.x,goal.y)
def initializePolicy(valueMatrix,policyMatrix):
    for i in range(len(valueMatrix)):
        for j in range(len(valueMatrix[0])):
            currentMax=valueMatrix[i,j]
            policyMatrix[i,j]=4
            if(i-1>=0):
                if(valueMatrix[i-1,j]>currentMax):
                    currentMax=valueMatrix[i-1,j]
                    policyMatrix[i,j]=0
            if(j-1>=0):
                if(valueMatrix[i,j-1]>currentMax):
                    currentMax=valueMatrix[i,j-1]
                    policyMatrix[i,j]=1
            if(i+1<len(valueMatrix)):
                if(valueMatrix[i+1,j]>currentMax):
                    currentMax=valueMatrix[i+1,j]
                    policyMatrix[i,j]=2
            if(j+1<len(valueMatrix[0])):
                if(valueMatrix[i,j+1]>currentMax):
                    currentMax=valueMatrix[i,j+1]
                    policyMatrix[i,j]=3
def calculateValue(a,b,c,d):
    return (0.7*a)+(0.1*b)+(0.1*c)+(0.1*d)
    
def evaluateAndUpdatePolicy(rewardMatrix,valueMatrix,policyMatrix,r,updatedValueMatrix,updatedPolicyMatrix):
    for i in range(len(valueMatrix)):
        for j in range(len(valueMatrix[0])):
            updatedValueMatrix[i,j]=valueMatrix[i,j]
            updatedPolicyMatrix[i][j]=policyMatrix[i][j]
            if(i==0 and j==0): #top left corner
                left=rewardMatrix[0,0]+r*calculateValue(valueMatrix[0,0],valueMatrix[0,0],valueMatrix[0,1],valueMatrix[1,0])
                right=rewardMatrix[0,1]+r*calculateValue(valueMatrix[0,1],valueMatrix[0,0],valueMatrix[0,0],valueMatrix[1,0])
                up=rewardMatrix[0,0]+r*calculateValue(valueMatrix[0,0],valueMatrix[0,0],valueMatrix[0,1],valueMatrix[1,0])
                down=rewardMatrix[1,0]+r*calculateValue(valueMatrix[1,0],valueMatrix[0,0],valueMatrix[0,0],valueMatrix[0,1])
            elif(i==0 and j==(len(valueMatrix[0])-1)):#top right corner
                left=rewardMatrix[0,j-1]+r*calculateValue(valueMatrix[0,j-1],valueMatrix[0,j],valueMatrix[i+1,j],valueMatrix[0,j])
                right=rewardMatrix[0,j]+r*calculateValue(valueMatrix[0,j],valueMatrix[0,j],valueMatrix[0,j-1],valueMatrix[i+1,j])
                up=rewardMatrix[0,j]+r*calculateValue(valueMatrix[0,j],valueMatrix[0,j-1],valueMatrix[i+1,j],valueMatrix[0,j])
                down=rewardMatrix[i+1,j]+r*calculateValue(valueMatrix[i+1,j],valueMatrix[0,j],valueMatrix[0,j-1],valueMatrix[0,j])
            elif(i==(len(valueMatrix)-1) and j==0):#bottom left corner
                left=rewardMatrix[i,j]+r*calculateValue(valueMatrix[i,j],valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i,j+1])
                right=rewardMatrix[i,j+1]+r*calculateValue(valueMatrix[i,j+1],valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i,j])
                up=rewardMatrix[i-1,j]+r*calculateValue(valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i,j],valueMatrix[i,j+1])
                down=rewardMatrix[i,j]+r*calculateValue(valueMatrix[i,j],valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i,j+1])
            elif(i==(len(valueMatrix)-1) and j==(len(valueMatrix[0])-1)):#bottom right corner
                left=rewardMatrix[i,j-1]+r*calculateValue(valueMatrix[i,j-1],valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i,j])
                right=rewardMatrix[i,j]+r*calculateValue(valueMatrix[i,j],valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i,j])
                up=rewardMatrix[i-1,j]+r*calculateValue(valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i,j],valueMatrix[i,j])
                down=rewardMatrix[i,j]+r*calculateValue(valueMatrix[i,j],valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i,j])
            elif(i==0):#upper row
                left=rewardMatrix[i,j-1]+r*calculateValue(valueMatrix[i,j-1],valueMatrix[i,j],valueMatrix[i+1,j],valueMatrix[i,j+1])
                right=rewardMatrix[i,j+1]+r*calculateValue(valueMatrix[i,j+1],valueMatrix[i,j],valueMatrix[i,j-1],valueMatrix[i+1,j])
                up=rewardMatrix[i,j]+r*calculateValue(valueMatrix[i,j],valueMatrix[i,j-1],valueMatrix[i+1,j],valueMatrix[i,j+1])
                down=rewardMatrix[i+1,j]+r*calculateValue(valueMatrix[i+1,j],valueMatrix[i,j],valueMatrix[i,j-1],valueMatrix[i,j+1])
            elif(j==0):#left most column
                left=rewardMatrix[i,j]+r*calculateValue(valueMatrix[i,j],valueMatrix[i-1,j],valueMatrix[i+1,j],valueMatrix[i,j+1])
                right=rewardMatrix[i,j+1]+r*calculateValue(valueMatrix[i,j+1],valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i+1,j])
                up=rewardMatrix[i-1,j]+r*calculateValue(valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i+1,j],valueMatrix[i,j+1])
                down=rewardMatrix[i+1,j]+r*calculateValue(valueMatrix[i+1,j],valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i,j+1])
            elif(j==(len(valueMatrix[0])-1)):#right most column
                left=rewardMatrix[i,j-1]+r*calculateValue(valueMatrix[i,j-1],valueMatrix[i-1,j],valueMatrix[i+1,j],valueMatrix[i,j])
                right=rewardMatrix[i,j]+r*calculateValue(valueMatrix[i,j],valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i+1,j])
                up=rewardMatrix[i-1,j]+r*calculateValue(valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i+1,j],valueMatrix[i,j])
                down=rewardMatrix[i+1,j]+r*calculateValue(valueMatrix[i+1,j],valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i,j])
            elif(i==(len(valueMatrix)-1)):#bottom row
                left=rewardMatrix[i,j-1]+r*calculateValue(valueMatrix[i,j-1],valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i,j+1])
                right=rewardMatrix[i,j+1]+r*calculateValue(valueMatrix[i,j+1],valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i,j])
                up=rewardMatrix[i-1,j]+r*calculateValue(valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i,j],valueMatrix[i,j+1])
                down=rewardMatrix[i,j]+r*calculateValue(valueMatrix[i,j],valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i,j+1])
            else:#other elements
                left=rewardMatrix[i,j-1]+r*calculateValue(valueMatrix[i,j-1],valueMatrix[i-1,j],valueMatrix[i+1,j],valueMatrix[i,j+1])
                right=rewardMatrix[i,j+1]+r*calculateValue(valueMatrix[i,j+1],valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i+1,j])
                up=rewardMatrix[i-1,j]+r*calculateValue(valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i+1,j],valueMatrix[i,j+1])
                down=rewardMatrix[i+1,j]+r*calculateValue(valueMatrix[i+1,j],valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i,j+1])
            if(max(left,right,up,down)==left):
                updatedValueMatrix[i,j]=rewardMatrix[i,j]+left
                updatedPolicyMatrix[i,j]=1
            elif(max(left,right,up,down)==right):
                updatedValueMatrix[i,j]=rewardMatrix[i,j]+right
                updatedPolicyMatrix[i,j]=3
            elif(max(left,right,up,down)==up):
                updatedValueMatrix[i,j]=rewardMatrix[i,j]+up
                updatedPolicyMatrix[i,j]=0
            elif(max(left,right,up,down)==down):
                updatedValueMatrix[i,j]=rewardMatrix[i,j]+down
                updatedPolicyMatrix[i,j]=2
    print(updatedValueMatrix)
    visualizePolicy(updatedPolicyMatrix)
    if(not np.array_equal(policyMatrix,updatedPolicyMatrix)):
        np.copyto(valueMatrix,updatedValueMatrix)
        policyMatrix=updatedPolicyMatrix.copy()
        evaluateAndUpdatePolicy(rewardMatrix,valueMatrix,policyMatrix,0.9,updatedValueMatrix,updatedPolicyMatrix)
#goal=Coordinate(2,3)
#policyMatrix=np.full((4,4),9)
#valueMatrix=np.full((4,4),-1)
#valueMatrix[2,3]+=100
#valueMatrix[1,2]-=100
#initializeMatrix(valueMatrix,goal)
#initializePolicy(valueMatrix,policyMatrix)
#rewardMatrix=np.full((4,4),-1)
#rewardMatrix[2,3]+=100
#rewardMatrix[1,2]-=100
#updatedValueMatrix=np.full((4,4),-1)
#updatedPolicyMatrix=np.full((4,4),9)

goal=Coordinate(0,0)
policyMatrix=np.full((3,3),9)
valueMatrix=np.full((3,3),-1)
valueMatrix[0,0]+=100
valueMatrix[1,0]-=100
initializeMatrix(valueMatrix,goal)
initializePolicy(rewardMatrix,policyMatrix)
rewardMatrix=np.full((3,3),-1)
rewardMatrix[0,0]+=100
rewardMatrix[1,0]-=100
updatedValueMatrix=np.full((3,3),-1)
updatedPolicyMatrix=np.full((3,3),9)
print(valueMatrix)
evaluateAndUpdatePolicy(rewardMatrix,rewardMatrix[:],policyMatrix,0.1,updatedValueMatrix,updatedPolicyMatrix)