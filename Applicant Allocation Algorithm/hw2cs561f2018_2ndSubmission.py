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
f = open("input.txt")
o = open("output.txt","w")
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
applicantListSPLA=[]
applicantListLAHSA=[]
for x in applicantList:
    if applicantList[x].isSPLA:
        applicantListSPLA.append(x)
    if applicantList[x].isLAHSA:
        applicantListLAHSA.append(x)
DP={}        
def isValid(temp,availability):
    for y in range(7):
        if temp[y]=='1':
            if availability[y]==0:
                return False
    return True
def updateAvailability(availability,x):
    temp=applicantList[x].days
    for y in range(7):
        if temp[y]=='1':
            availability[y]=availability[y]-1
def removeApplicant(x,applicantListSPLA,applicantListLAHSA):
    if x in applicantListSPLA:
        applicantListSPLA.remove(x)
    if x in applicantListLAHSA:
        applicantListLAHSA.remove(x)
def getKey(pickedListSPLA,pickedListLAHSA,x):
    pickedListSPLA.sort()
    pickedListLAHSA.sort()
    return str(pickedListSPLA)+str(pickedListLAHSA)+x
def pickBestLAHSA(applicantListSPLA,applicantListLAHSA,currentEfficiencySPLA,currentEfficiencyLAHSA,
                  availabilitySPLA,availabilityLAHSA,pickedListSPLA,pickedListLAHSA):
    global DP
    key=getKey(pickedListSPLA,pickedListLAHSA,'LAHSA')
    if key in DP:
        return DP[key]
    currentMax=currentEfficiencyLAHSA
    currentSPLA=currentEfficiencySPLA
    for x in applicantListLAHSA:
        currentScore=currentEfficiencyLAHSA
        temp=applicantList[x].days
        if isValid(temp,availabilityLAHSA):
            currentScore+=temp.count('1')
            tempAvailabilityLAHSA=availabilityLAHSA[:]
            tempApplicantListLAHSA=copy.deepcopy(applicantListLAHSA)
            tempApplicantListSPLA=copy.deepcopy(applicantListSPLA)
            tempPickedListLAHSA=copy.deepcopy(pickedListLAHSA)
            tempPickedListLAHSA.append(x)
            updateAvailability(tempAvailabilityLAHSA,x)
            removeApplicant(x,tempApplicantListSPLA,tempApplicantListLAHSA)
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
    DP[key]=[currentSPLA,currentMax]
    return DP[key]
def pickBestSPLA(applicantListSPLA,applicantListLAHSA,currentEfficiencySPLA,currentEfficiencyLAHSA,
                  availabilitySPLA,availabilityLAHSA,pickedListSPLA,pickedListLAHSA):
    global DP
    key=getKey(pickedListSPLA,pickedListLAHSA,'SPLA')
    if key in DP:
        return DP[key]
    currentMax=currentEfficiencySPLA
    currentLAHSA=currentEfficiencyLAHSA
    for x in applicantListSPLA:
        currentScore=currentEfficiencySPLA
        temp=applicantList[x].days
        if isValid(temp,availabilitySPLA):
            currentScore+=temp.count('1')
            tempAvailabilitySPLA=availabilitySPLA[:]
            tempApplicantListLAHSA=copy.deepcopy(applicantListLAHSA)
            tempApplicantListSPLA=copy.deepcopy(applicantListSPLA)
            tempPickedListSPLA=copy.deepcopy(pickedListSPLA)
            tempPickedListSPLA.append(x)
            updateAvailability(tempAvailabilitySPLA,x)
            removeApplicant(x,tempApplicantListSPLA,tempApplicantListLAHSA)
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
    DP[key]=[currentMax,currentLAHSA]
    return DP[key]
def pickBestSPLAHelper(applicantListSPLA,applicantListLAHSA,currentEfficiencySPLA,currentEfficiencyLAHSA,
                 availabilitySPLA,availabilityLAHSA,pickedListSPLA,pickedListLAHSA):
    currentMax=currentEfficiencySPLA
    currentBestApplicant=None
    for x in applicantListSPLA:
        currentScore=currentEfficiencySPLA
        temp=applicantList[x].days
        if isValid(temp,availabilitySPLA):
            currentScore+=temp.count('1')
            tempAvailabilitySPLA=availabilitySPLA[:]
            tempApplicantListLAHSA=copy.deepcopy(applicantListLAHSA)
            tempApplicantListSPLA=copy.deepcopy(applicantListSPLA)
            updateAvailability(tempAvailabilitySPLA,x)
            tempPickedListSPLA=copy.deepcopy(pickedListSPLA)
            tempPickedListSPLA.append(x)
            removeApplicant(x,tempApplicantListSPLA,tempApplicantListLAHSA)
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
    return currentBestApplicant
o.write(str(pickBestSPLAHelper(applicantListSPLA,applicantListLAHSA,currentEfficiencySPLA,currentEfficiencyLAHSA,
                   availabilitySPLA,availabilityLAHSA,[],[])))