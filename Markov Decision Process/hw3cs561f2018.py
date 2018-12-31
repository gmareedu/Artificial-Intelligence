# -*- coding: utf-8 -*-
"""
Created on Sat Nov 10 17:38:56 2018

@author: Giridhar
"""
import numpy as np;

class Coordinate():
    def __init__(self,x,y):
        self.x=x
        self.y=y

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
    
def evaluateAndUpdatePolicy(goal,rewardMatrix,valueMatrix,policyMatrix,r,updatedValueMatrix,updatedPolicyMatrix):
    for i in range(len(valueMatrix)):
        for j in range(len(valueMatrix[0])):
            updatedValueMatrix[i,j]=valueMatrix[i,j]
            updatedPolicyMatrix[i][j]=policyMatrix[i][j]
            if(i==goal.x and j== goal.y):
                left=0
                right=0
                up=0
                down=0
            elif(i==0 and j==0): #top left corner
                left=calculateValue(valueMatrix[0,0],valueMatrix[0,0],valueMatrix[0,1],valueMatrix[1,0])
                right=calculateValue(valueMatrix[0,1],valueMatrix[0,0],valueMatrix[0,0],valueMatrix[1,0])
                up=calculateValue(valueMatrix[0,0],valueMatrix[0,0],valueMatrix[0,1],valueMatrix[1,0])
                down=calculateValue(valueMatrix[1,0],valueMatrix[0,0],valueMatrix[0,0],valueMatrix[0,1])
            elif(i==0 and j==(len(valueMatrix[0])-1)):#top right corner
                left=calculateValue(valueMatrix[0,j-1],valueMatrix[0,j],valueMatrix[i+1,j],valueMatrix[0,j])
                right=calculateValue(valueMatrix[0,j],valueMatrix[0,j],valueMatrix[0,j-1],valueMatrix[i+1,j])
                up=calculateValue(valueMatrix[0,j],valueMatrix[0,j-1],valueMatrix[i+1,j],valueMatrix[0,j])
                down=calculateValue(valueMatrix[i+1,j],valueMatrix[0,j],valueMatrix[0,j-1],valueMatrix[0,j])
            elif(i==(len(valueMatrix)-1) and j==0):#bottom left corner
                left=calculateValue(valueMatrix[i,j],valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i,j+1])
                right=calculateValue(valueMatrix[i,j+1],valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i,j])
                up=calculateValue(valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i,j],valueMatrix[i,j+1])
                down=calculateValue(valueMatrix[i,j],valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i,j+1])
            elif(i==(len(valueMatrix)-1) and j==(len(valueMatrix[0])-1)):#bottom right corner
                left=calculateValue(valueMatrix[i,j-1],valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i,j])
                right=calculateValue(valueMatrix[i,j],valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i,j])
                up=calculateValue(valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i,j],valueMatrix[i,j])
                down=calculateValue(valueMatrix[i,j],valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i,j])
            elif(i==0):#upper row
                left=calculateValue(valueMatrix[i,j-1],valueMatrix[i,j],valueMatrix[i+1,j],valueMatrix[i,j+1])
                right=calculateValue(valueMatrix[i,j+1],valueMatrix[i,j],valueMatrix[i,j-1],valueMatrix[i+1,j])
                up=calculateValue(valueMatrix[i,j],valueMatrix[i,j-1],valueMatrix[i+1,j],valueMatrix[i,j+1])
                down=calculateValue(valueMatrix[i+1,j],valueMatrix[i,j],valueMatrix[i,j-1],valueMatrix[i,j+1])
            elif(j==0):#left most column
                left=calculateValue(valueMatrix[i,j],valueMatrix[i-1,j],valueMatrix[i+1,j],valueMatrix[i,j+1])
                right=calculateValue(valueMatrix[i,j+1],valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i+1,j])
                up=calculateValue(valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i+1,j],valueMatrix[i,j+1])
                down=calculateValue(valueMatrix[i+1,j],valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i,j+1])
            elif(j==(len(valueMatrix[0])-1)):#right most column
                left=calculateValue(valueMatrix[i,j-1],valueMatrix[i-1,j],valueMatrix[i+1,j],valueMatrix[i,j])
                right=calculateValue(valueMatrix[i,j],valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i+1,j])
                up=calculateValue(valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i+1,j],valueMatrix[i,j])
                down=calculateValue(valueMatrix[i+1,j],valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i,j])
            elif(i==(len(valueMatrix)-1)):#bottom row
                left=calculateValue(valueMatrix[i,j-1],valueMatrix[i-1,j],valueMatrix[i,j],valueMatrix[i,j+1])
                right=calculateValue(valueMatrix[i,j+1],valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i,j])
                up=calculateValue(valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i,j],valueMatrix[i,j+1])
                down=calculateValue(valueMatrix[i,j],valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i,j+1])
            else:#other elements
                left=calculateValue(valueMatrix[i,j-1],valueMatrix[i-1,j],valueMatrix[i+1,j],valueMatrix[i,j+1])
                right=calculateValue(valueMatrix[i,j+1],valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i+1,j])
                up=calculateValue(valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i+1,j],valueMatrix[i,j+1])
                down=calculateValue(valueMatrix[i+1,j],valueMatrix[i-1,j],valueMatrix[i,j-1],valueMatrix[i,j+1])
            if(max(left,right,up,down)==left):
                updatedValueMatrix[i,j]=rewardMatrix[i,j]+r*left
                updatedPolicyMatrix[i,j]=1
            elif(max(left,right,up,down)==right):
                updatedValueMatrix[i,j]=rewardMatrix[i,j]+r*right
                updatedPolicyMatrix[i,j]=3
            elif(max(left,right,up,down)==down):
                updatedValueMatrix[i,j]=rewardMatrix[i,j]+r*down
                updatedPolicyMatrix[i,j]=2
            elif(max(left,right,up,down)==up):
                updatedValueMatrix[i,j]=rewardMatrix[i,j]+r*up
                updatedPolicyMatrix[i,j]=0
    if(not np.array_equal(valueMatrix,updatedValueMatrix)):
        np.copyto(valueMatrix,updatedValueMatrix)
        policyMatrix=updatedPolicyMatrix.copy()
        evaluateAndUpdatePolicy(goal,rewardMatrix,valueMatrix,policyMatrix,0.9,updatedValueMatrix,updatedPolicyMatrix)

def turn_left(move):
    if(move==0):
        return 1
    elif(move==1):
        return 2
    elif(move==2):
        return 3
    else:
        return 0

def turn_right(move):
    if(move==0):
        return 3
    elif(move==3):
        return 2
    elif(move==2):
        return 1
    else:
        return 0

def runSimulation(i,updatedPolicyMatrix,rewardMatrix):    
    totalRewards=0.0
    for j in range(10):
        pos = start[i].copy()
        np.random.seed(j)
        swerve = np.random.random_sample(1000000)
        k=0
        reward=0.0
        while(not(pos[0]==goal[i][0] and pos[1]==goal[i][1])):
            move = updatedPolicyMatrix[pos[0],pos[1]]
            if swerve[k] > 0.7:
                if swerve[k] > 0.8:
                    if swerve[k] > 0.9:
                        move = turn_right(turn_right(move))
                    else:
                        move = turn_right(move)
                else:
                    move = turn_left(move)
            if(move==0):
                if(pos[0]!=0):
                    pos[0]-=1
            elif(move==1):
                if(pos[1]!=0):
                    pos[1]-=1
            elif(move==2):
                if(pos[0]!=s-1):
                    pos[0]+=1
            else:
                if(pos[1]!=s-1):
                    pos[1]+=1    
            reward+=rewardMatrix[pos[0],pos[1]]
            k=k+1
        totalRewards+=reward    
    out.write(str(int(np.floor(totalRewards/10)))+"\n")

def main(x,currentGoal,valueMatrix,policyMatrix,rewardMatrix):    
    valueMatrix[currentGoal.x,currentGoal.y]+=100.0
    np.copyto(rewardMatrix,valueMatrix)
#    initializeMatrix(valueMatrix,currentGoal)
#    initializePolicy(valueMatrix,policyMatrix)
    updatedValueMatrix=np.full((s,s),-1.0)
    updatedPolicyMatrix=np.full((s,s),9)
    evaluateAndUpdatePolicy(currentGoal,rewardMatrix,valueMatrix,policyMatrix,0.9,updatedValueMatrix,updatedPolicyMatrix)
    runSimulation(x,updatedPolicyMatrix,rewardMatrix)

f = open("input.txt")
out = open("output.txt","w")
line = f.readlines()
s = int(line[0].strip('\n').strip('\r'))
n = int(line[1].strip('\n').strip('\r'))
o = int(line[2].strip('\n').strip('\r'))
policyMatrix = np.full((s,s),0)
valueMatrix = np.full((s,s),-1.0)
rewardMatrix = np.full((s,s),-1.0)
for i in range(3,o+3):
    y,x = (int(z) for z in line[i].strip('\n').strip('\r').split(','))
    valueMatrix[x,y] -= 100.0
start = [[] for i in range(n)]
x = 0
for i in range(o+3,o+n+3):
    start[x] = (list(reversed([int(z) for z in line[i].strip('\n').strip('\r').split(',')])))
    x += 1
goal = [[] for i in range(n)]
x = 0
for i in range(o+n+3,o+n+n+3):
    goal[x] = (list(reversed([int(z) for z in line[i].strip('\n').strip('\r').split(',')])))
    x += 1
for x in range(n):
    currentGoal=Coordinate(goal[x][0],goal[x][1])
    newValueMatrix=np.full((s,s),-1.0)
    newPolicyMatrix=np.full((s,s),0)
    newRewardMatrix=np.full((s,s),-1.0)
    np.copyto(newValueMatrix,valueMatrix)
    np.copyto(newRewardMatrix,rewardMatrix)
    np.copyto(newPolicyMatrix,policyMatrix)
    main(x,currentGoal,newValueMatrix,newPolicyMatrix,newRewardMatrix)