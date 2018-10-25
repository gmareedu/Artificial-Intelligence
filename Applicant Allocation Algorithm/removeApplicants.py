# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 22:16:58 2018

@author: Giridhar
"""
from datetime import datetime

import copy
class Applicant():
    def __init__(self,id,g,a,p,m,c,dl,days):
        self.id=id
        self.g=g
        self.a=a
        self.p=p
        self.m=m
        self.c=c
        self.dl=dl
        self.days=days
        if self.c==True and self.dl==True and self.m==False:
            self.isSPLA=True
        else:
            self.isSPLA=False
        if self.g=='F' and self.a>17 and self.p==False:
            self.isLAHSA=True
        else:
            self.isLAHSA=False
o=open("output_for_test_cases.txt","w")
for fnumber in range(500):

    start = datetime.now()
    file_name='test\input'+format(fnumber,'04d')+'.txt'
    f = open(file_name)

#t = open("temp2.txt","w")
    line=f.readlines()
    b=int(line[0].strip('\n').strip('\r'))
    p=int(line[1].strip('\n').strip('\r'))
    L=int(line[2].strip('\n').strip('\r'))
    pickedLAHSA=[]
    for i in range(3,L+3):
        pickedLAHSA.append(line[i].strip('\n').strip('\r'))
    S=int(line[L+3].strip('\n').strip('\r'))
    
    pickedSPLA=[]
    for i in range(L+4,L+S+4):
        pickedSPLA.append(line[i].strip('\n').strip('\r'))
    A=int(line[L+S+4].strip('\n').strip('\r'))
    applicantList={}
    for i in range(L+S+5,L+S+A+5):
        temp=line[i].strip('\n').strip('\r')
        applicantList[temp[:5]]=Applicant(temp[:5],temp[5].upper(),int(temp[6:9]),
                     True if temp[9].upper()=='Y' else False,   
                     True if temp[10].upper()=='Y' else False,
                     True if temp[11].upper()=='Y' else False,
                     True if temp[12].upper()=='Y' else False,
                     temp[13:])
    availabilityLAHSA=[b,b,b,b,b,b,b]
    availabilitySPLA=[p,p,p,p,p,p,p]
    currentEfficiencyLAHSA=0
    currentEfficiencySPLA=0
    for x in pickedLAHSA:
        temp=applicantList[x].days
        for y in range(7):
            if temp[y]=='1':
                availabilityLAHSA[y]-=1
                currentEfficiencyLAHSA+=1
        del applicantList[x]
    for x in pickedSPLA:
        temp=applicantList[x].days
        for y in range(7):
            if temp[y]=='1':
                availabilitySPLA[y]-=1
                currentEfficiencySPLA+=1
        del applicantList[x]
    def isValid(temp,availability):
        for y in range(7):
            if temp[y]=='1':
                if availability[y]==0:
                    return False
        return True
    applicantListSPLA=[]
    applicantListLAHSA=[]
    for x in applicantList:
        if applicantList[x].isSPLA and isValid(applicantList[x].days,availabilitySPLA):
            applicantListSPLA.append(x)
        if applicantList[x].isLAHSA and isValid(applicantList[x].days,availabilityLAHSA):
            applicantListLAHSA.append(x)
    DP={}        
    
    def updateAvailability(availability,x):
        temp=applicantList[x].days
        for y in range(7):
            if temp[y]=='1':
                availability[y]=availability[y]-1
    def removeApplicant(x,applicantListSPLA,applicantListLAHSA,availability,isSPLA):
        if x in applicantListSPLA:
            applicantListSPLA.remove(x)
        if x in applicantListLAHSA:
            applicantListLAHSA.remove(x)
        if(isSPLA):
            for a in applicantListSPLA:
                if not all(i>=0 for i in [x - y for x, y in zip(availability,list(map(int,list(applicantList[a].days))))]):
                    applicantListSPLA.remove(a)
        else:
            for a in applicantListLAHSA:
                if not all(i>=0 for i in [x - y for x, y in zip(availability,list(map(int,list(applicantList[a].days))))]):
                    applicantListLAHSA.remove(a)
    
    def getKey(pickedListSPLA,pickedListLAHSA,x):
        pickedListSPLA.sort()
        pickedListLAHSA.sort()
        return str(pickedListSPLA)+str(pickedListLAHSA)+x
    
    def pickBestLAHSA(applicantListSPLA,applicantListLAHSA,currentEfficiencySPLA,currentEfficiencyLAHSA,
                      availabilitySPLA,availabilityLAHSA,pickedListSPLA,pickedListLAHSA):
        global DP
    #    t.write("LAHSA   "+str(pickedListSPLA)+"        "+ str(pickedListLAHSA)+"\n")    
        key=getKey(pickedListSPLA,pickedListLAHSA,'LAHSA')
        if key in DP:
            return DP[key]
        currentMax=currentEfficiencyLAHSA
        currentSPLA=currentEfficiencySPLA
        for x in applicantListLAHSA:
            currentScore=currentEfficiencyLAHSA
            temp=applicantList[x].days
            if isValid(temp,availabilityLAHSA):
    #            t.write("Current LAHSA Pick: "+x+"\n")
                currentScore+=temp.count('1')
                tempAvailabilityLAHSA=availabilityLAHSA[:]
                tempApplicantListLAHSA=copy.deepcopy(applicantListLAHSA)
                tempApplicantListSPLA=copy.deepcopy(applicantListSPLA)
                tempPickedListLAHSA=copy.deepcopy(pickedListLAHSA)
                tempPickedListLAHSA.append(x)
                updateAvailability(tempAvailabilityLAHSA,x)
    #            t.write("Updated LAHSA Availability: "+str(tempAvailabilityLAHSA)+"\n")
                removeApplicant(x,tempApplicantListSPLA,tempApplicantListLAHSA,tempAvailabilityLAHSA,False)
    #            t.write("Remaining SPLA: "+str(tempApplicantListSPLA)+"\n")
    #            t.write("Remaining LAHSA: "+str(tempApplicantListLAHSA)+"\n")
                if len(tempApplicantListSPLA)!=0:
                    a,b=pickBestSPLA(tempApplicantListSPLA,tempApplicantListLAHSA,
                                  currentEfficiencySPLA,currentScore,availabilitySPLA,tempAvailabilityLAHSA,
                                  pickedListSPLA,tempPickedListLAHSA)
                else:
                    a,b=pickBestLAHSA(tempApplicantListSPLA,tempApplicantListLAHSA,
                                  currentEfficiencySPLA,currentScore,availabilitySPLA,tempAvailabilityLAHSA,
                                  pickedListSPLA,tempPickedListLAHSA)
                if(b>currentMax):
                    currentMax=b
                    currentSPLA=a
    #    t.write("Return LAHSA Values: "+str(currentSPLA)+" "+str(currentMax)+"\n")
        DP[key]=[currentSPLA,currentMax]
    #    t.write("Current Key  :"+key+" Current Values  "+str(DP[key]))
        return DP[key]
    
    
    def pickBestSPLA(applicantListSPLA,applicantListLAHSA,currentEfficiencySPLA,currentEfficiencyLAHSA,
                      availabilitySPLA,availabilityLAHSA,pickedListSPLA,pickedListLAHSA):
        global DP
    #    t.write('SPLA   x'+str(pickedListSPLA)+"        "+ str(pickedListLAHSA)+"\n")
        key=getKey(pickedListSPLA,pickedListLAHSA,'SPLA')
        if key in DP:
            return DP[key]
        currentMax=currentEfficiencySPLA
        currentLAHSA=currentEfficiencyLAHSA
        for x in applicantListSPLA:
            currentScore=currentEfficiencySPLA
            temp=applicantList[x].days
            if isValid(temp,availabilitySPLA):
    #            t.write("Current SPLA Pick: "+x+"\n")
                currentScore+=temp.count('1')
                tempAvailabilitySPLA=availabilitySPLA[:]
                tempApplicantListLAHSA=copy.deepcopy(applicantListLAHSA)
                tempApplicantListSPLA=copy.deepcopy(applicantListSPLA)
                tempPickedListSPLA=copy.deepcopy(pickedListSPLA)
                tempPickedListSPLA.append(x)
                updateAvailability(tempAvailabilitySPLA,x)
    #            t.write("Updated SPLA Availability: "+str(tempAvailabilitySPLA)+"\n")
                removeApplicant(x,tempApplicantListSPLA,tempApplicantListLAHSA,tempAvailabilitySPLA,True)
    #            t.write("Remaining SPLA: "+str(tempApplicantListSPLA)+"\n")
    #            t.write("Remaining LAHSA: "+str(tempApplicantListLAHSA)+"\n")
                if len(tempApplicantListLAHSA)!=0:
                    a,b=pickBestLAHSA(tempApplicantListSPLA,tempApplicantListLAHSA,
                                  currentScore,currentEfficiencyLAHSA,tempAvailabilitySPLA,availabilityLAHSA,
                                  tempPickedListSPLA,pickedListLAHSA)            
                else:
                    a,b=pickBestSPLA(tempApplicantListSPLA,tempApplicantListLAHSA,
                                  currentScore,currentEfficiencyLAHSA,tempAvailabilitySPLA,availabilityLAHSA,
                                  tempPickedListSPLA,pickedListLAHSA)
                if(a>currentMax):
                    currentMax=a
                    currentLAHSA=b
    #    t.write("Return SPLA Values: "+str(currentMax)+" "+str(currentLAHSA)+"\n")
        DP[key]=[currentMax,currentLAHSA]
    #    t.write("Current Key  :"+key+" Current Values  "+str(DP[key]))
        return DP[key]
    
    def pickBestSPLAHelper(applicantListSPLA,applicantListLAHSA,currentEfficiencySPLA,currentEfficiencyLAHSA,
                     availabilitySPLA,availabilityLAHSA,pickedListSPLA,pickedListLAHSA):
        currentMax=currentEfficiencySPLA
        currentBestApplicant=None
        for x in applicantListSPLA:
            currentScore=currentEfficiencySPLA
            temp=applicantList[x].days
            if isValid(temp,availabilitySPLA):
    #            t.write("Current SPLA Pick: "+x+"\n")
                currentScore+=temp.count('1')
                tempAvailabilitySPLA=availabilitySPLA[:]
                tempApplicantListLAHSA=copy.deepcopy(applicantListLAHSA)
                tempApplicantListSPLA=copy.deepcopy(applicantListSPLA)
                updateAvailability(tempAvailabilitySPLA,x)
                tempPickedListSPLA=copy.deepcopy(pickedListSPLA)
                tempPickedListSPLA.append(x)
    #            t.write("Updated SPLA Availability: "+str(tempAvailabilitySPLA)+"\n")
                removeApplicant(x,tempApplicantListSPLA,tempApplicantListLAHSA,tempAvailabilitySPLA,True)
    #            t.write("Remaining SPLA: "+str(tempApplicantListSPLA)+"\n")
    #            t.write("Remaining LAHSA: "+str(tempApplicantListLAHSA)+"\n")
    #            print(tempApplicantListLAHSA)
                if len(tempApplicantListLAHSA)!=0:
                    a,b=pickBestLAHSA(tempApplicantListSPLA,tempApplicantListLAHSA,
                                  currentScore,currentEfficiencyLAHSA,tempAvailabilitySPLA,availabilityLAHSA,
                                  tempPickedListSPLA,pickedListLAHSA)            
                else:
                    a,b=pickBestSPLA(tempApplicantListSPLA,tempApplicantListLAHSA,
                                  currentScore,currentEfficiencyLAHSA,tempAvailabilitySPLA,availabilityLAHSA,
                                  tempPickedListSPLA,pickedListLAHSA)
                if(a>currentMax):
                    currentMax=a
                    currentBestApplicant=x
                elif(a==currentMax):
                    if(x<currentBestApplicant):
                        currentBestApplicant=x
#        print(":::::::::::Return SPLA Ultimate Values: "+str(currentMax)+" "+str(currentBestApplicant)+"\n")                   
        return currentBestApplicant
    y=pickBestSPLAHelper(applicantListSPLA,applicantListLAHSA,currentEfficiencySPLA,currentEfficiencyLAHSA,
                       availabilitySPLA,availabilityLAHSA,[],[])
    stop = datetime.now()
    print(file_name+":   "+str(y)+"    Time Taken:   "+str(stop-start)+"\n")
    o.write(file_name+":   "+str(y)+"    Time Taken:   "+str(stop-start)+"\n")