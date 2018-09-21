class Coordinate():
    def __init__(self,x,y,z):
        self.x=x
        self.y=y
        self.scooterCount=z
def checkValid(inCoordinates,polCoordinates):
    for p in polCoordinates:
        if inCoordinates.x==p.x or inCoordinates.y==p.y or abs(inCoordinates.x-p.x)==abs(inCoordinates.y-p.y):
            return False
    return True
def writeOutput(x):
    o = open("output.txt","w")
    o.write(str(x))
f = open("input.txt")
line=f.readlines()
n=int(line[0].strip('\n').strip('\r'))
p=int(line[1].strip('\n').strip('\r'))
s=int(line[2].strip('\n').strip('\r'))
d={}
for i in range(3,len(line)):
    y=line[i].strip('\n').strip('\r')
    if y in d:
        d[y]+=1
    else:
        d[y]=1            
for i in range(n):
    for j in range(n):
        x=str(i)+','+str(j)
        if x not in d:
            d[x]=0
L=sorted(d,key=d.get,reverse=True)
maxScooterCount=0
finalPolCoordinates=[]
def DFSRecursive(row,polCoordinates,policeCount,totalScooterCount):
    global maxScooterCount,finalPolCoordinates
    if(policeCount==p):
        if totalScooterCount>maxScooterCount:
            maxScooterCount=totalScooterCount
            finalPolCoordinates=polCoordinates
    elif row<n:
        for i in range(n):
            currCoordinate=Coordinate(row,i,d[str(row)+","+str(i)])
            if checkValid(currCoordinate,polCoordinates):
                polCoordinates.insert(row,currCoordinate)
                totalScooterCount+=currCoordinate.scooterCount
                policeCount+=1
                DFSRecursive(row+1,polCoordinates,policeCount,totalScooterCount)
                polCoordinates.pop()
                policeCount-=1
                totalScooterCount-=currCoordinate.scooterCount
def GreedyDFS():
    global maxScooterCount,finalPolCoordinates
    for i in range(len(L)):
        polCoordinates=[Coordinate(int(L[i].split(',')[0]),int(L[i].split(',')[1]),d[L[i]])]
        totalScooterCount=d[L[i]]
        policeCount=1
        for j in range(len(L)):
            if policeCount!=p:
                currCoordinate=Coordinate(int(L[j].split(',')[0]),int(L[j].split(',')[1]),d[L[j]])
                if checkValid(currCoordinate,polCoordinates):
                    polCoordinates.append(currCoordinate)
                    totalScooterCount+=currCoordinate.scooterCount
                    policeCount+=1
            else:
                if totalScooterCount>maxScooterCount:
                    maxScooterCount=totalScooterCount
                    finalPolCoordinates=polCoordinates
                break
def ExhaustiveDFS(index,polCoordinates,policeCount,totalScooterCount):
    global maxScooterCount
    if(policeCount==p):
        if totalScooterCount>maxScooterCount:
            maxScooterCount=totalScooterCount
    else:
        for i in range(index,len(L)-(p-policeCount)+1):
            currCoordinate=Coordinate(int(L[i].split(',')[0]),int(L[i].split(',')[1]),d[L[i]])
            if checkValid(currCoordinate,polCoordinates):
                polCoordinates.insert(policeCount,currCoordinate)
                totalScooterCount+=currCoordinate.scooterCount
                policeCount+=1
                ExhaustiveDFS(i+1,polCoordinates,policeCount,totalScooterCount)
                polCoordinates.pop()
                policeCount-=1
                totalScooterCount-=currCoordinate.scooterCount
if n>=13:
    GreedyDFS()
elif p==n:
    DFSRecursive(0,[],0,0)
elif n<=10:
    for iter in range(len(L)-p+1):
        ExhaustiveDFS(iter+1,[Coordinate(int(L[iter].split(',')[0]),int(L[iter].split(',')[1]),d[L[iter]])],1,d[L[iter]])
else:
    GreedyDFS()
writeOutput(maxScooterCount)
