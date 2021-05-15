import cProfile as cP

#cP.run("import Statistics")
from Objects import *


NowGame=Game()
NowGame.start()
NowGame.Print()
cP.run("for i in range(100):Think(NowGame.Bgrid)")

import time
from Objects import *

N=int(input("回数>>>"))
#N=1
scores=[]
maxes=[]
n=0
start=time.time()
for i in range(N):
    NowGame=Game()
    NowGame.start()
    while NowGame.gameover==False:
        #NowGame.Print()
        NowGame.Move(Think(NowGame.Bgrid,False))
        n+=1
    print("No.{}".format(i+1))
    NowGame.Print()
    scores+=[NowGame.score]
    maxes+=[max(BtoO(NowGame.Bgrid))]

finish=time.time()



print("BEST : {}".format(max(scores)))
print("WORST : {}".format(min(scores)))
print("MEAN : {}".format(sum(scores)/len(scores)))
print("WEIGHT : {}".format(WEIGHT))
print("COUNT : {}".format(COUNT))
print("DEPTHLIST : {}".format(DEPTHLIST))
print("{}moves/sec".format(round(n/(finish-start),2)))
maxdata=[0]*16
for i in maxes:
    maxdata[i]+=1
for i in range(16):
    n=maxdata[i]
    print("{} : {}回 ({}%)".format(int(2**i),n,round(100*(n/N))))
print()
scores.sort()
for i in scores:
    print(i)
time.sleep(100000)

POSSIBILITY=[0.8, 0.2]
WEIGHT=[9,2]

#
#for i in range(COUNT,16):
#  if i in Ogrid:
#    variety+=1
#return max(math.floor(((variety)**POWER)*FACTOR)+GAIN,MINIMUM)
POWER=0.85
FACTOR=1.1
GAIN=1.5
MINIMUM=4
COUNT=4
#          0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18
DEPTHLIST=[4,4,4,4,4,4,5,5,5,6, 6, 7, 9,10,11,12,10,11,12]

TableMR=[]
TableML=[]
TableV=[]
from Settings import *

def b_to_r(b):
    r=[]
    x=b
    for i in range(4):
        n=x&0b1111
        r+=[n]
        x=x>>4
    return r

def r_to_b(r):
    b=0
    for i in range(4):
        k=r[3-i]
        b=b<<4
        b=b|k
    return b
    
def moveleft(b):
    r=b_to_r(b)

    for i in range(4):
        if 0 in r:
            r.remove(0)
        else:
            break

    M=max(0,len(r)-1)
    for i in range(M):
        if i<len(r)-1:
            if r[i]==r[i+1]:
                r[i]+=1
                del r[i+1]
    r+=[0]*(4-len(r))
    return r_to_b(r)
    

def moveright(b):
    r=b_to_r(b)
    r.reverse()
    for i in range(4):
        if 0 in r:
            r.remove(0)
        else:
            break

    M=max(0,len(r)-1)
    for i in range(M):
        if i<len(r)-1:
            if r[i]==r[i+1]:
                r[i]+=1
                del r[i+1]
    r+=[0]*(4-len(r))

    r.reverse()
    
    return r_to_b(r)

def add(b):
    rs1=[]
    rs2=[]
    r=b_to_r(b)
    for i in range(4):
        if r[i]==0:
            x=b_to_r(b)
            y=b_to_r(b)
            x[i]=1
            y[i]=2
            rs1+=[r_to_b(x)]
            rs2+=[r_to_b(y)]
    return [rs1,rs2]
            
def smoothness(b):
    result=0
    for i in range(3):
        x=(b>>(4*i))&15
        y=(b>>(4*(i+1)))&15
        result-=abs((2**x)-(2**y))
    return result

def emerge(b):
    r=b_to_r(b)
    result=0
    for i in r:
        result+=i*(2**i)
    return result
    
def evaluate(b):
    #print("{}, {}".format(smoothness(b)*WEIGHT[0],emerge(b)*WEIGHT[1]))
    return smoothness(b)*WEIGHT[0]+emerge(b)*WEIGHT[1]

def solid(b):
    r=b_to_r(b)
    result=1
    if not 0 in r:
        for i in range(3):
            if r[i]==r[i+1]:
                break
        else:
            result=0
    return result
        

TableML=[]
TableMR=[]
TableV=[]
TableA=[]
TableS=[]
for i in range(65536):
    TableML+=[moveleft(i)]
    TableMR+=[moveright(i)]
    TableV+=[evaluate(i)]
    TableA+=[add(i)]
    TableS+=[solid(i)]

from Settings import *
from MakeTable import TableML, TableMR, TableA, TableV, TableS
import math

def BtoO(Bgrid):
    Ogrid=[]
    x=Bgrid
    for i in range(16):
        n=x&0b1111
        Ogrid+=[n]
        x=x>>4
    return Ogrid

"""def OtoB(Ogrid):
    Bgrid=0
    for i in range(16):
        k=Ogrid[15-i]
        Bgrid=Bgrid<<4
        Bgrid=Bgrid|k
    return Bgrid"""

def OtoB(Ogrid):
    Bgrid=0
    c=0
    for i in Ogrid:
        Bgrid=Bgrid|i<<(c)
        c+=4
    return Bgrid


def PrintLetter(x):
    y=int(2**x)
    if y==1:
        z=""
    else:
        z=str(y)
    return z
    
def Print(B):
    Ogrid=BtoO(B)
    result=""
    for i in range(4):
        a,b,c,d=Ogrid[4*i+0],Ogrid[4*i+1],Ogrid[4*i+2],Ogrid[4*i+3]
        a,b,c,d=map(PrintLetter,(a,b,c,d))
        
        result+="{}	|{}	|{}	|{}\n".format(a,b,c,d)
    print(result)


def rotate(Bgrid,mode):#1:90°反時計回り 2:180° 3:90°時計回り
    C=[[ 0, 1, 2, 3,
         4, 5, 6, 7,
         8, 9,10,11,
        12,13,14,15], 
        
       [ 3, 7,11,15,
         2, 6,10,14,
         1, 5, 9,13,
         0, 4, 8,12],

       [15,14,13,12,
        11,10, 9, 8,
         7, 6, 5, 4,
         3, 2, 1, 0],

       [12, 8, 4, 0,
        13, 9, 5, 1,
        14,10, 6, 2,
        15,11, 7, 3]]
    
    D=C[mode]
    Ogrid=BtoO(Bgrid)
    newOgrid=[0]*16
    for i in range(16):
        newOgrid[i]=Ogrid[D[i]]

    newBgrid=OtoB(newOgrid)
    return newBgrid

def Orotate(Ogrid,mode):
    C=[[ 0, 1, 2, 3,
         4, 5, 6, 7,
         8, 9,10,11,
        12,13,14,15], 
        
       [ 3, 7,11,15,
         2, 6,10,14,
         1, 5, 9,13,
         0, 4, 8,12],

       [15,14,13,12,
        11,10, 9, 8,
         7, 6, 5, 4,
         3, 2, 1, 0],

       [12, 8, 4, 0,
        13, 9, 5, 1,
        14,10, 6, 2,
        15,11, 7, 3]]
    
    D=C[mode]
    newOgrid=[0]*16
    for i in range(16):
        newOgrid[i]=Ogrid[D[i]]

    return newOgrid

def MoveLeft(Bgrid):
    global TableML
    x=Bgrid
    result=0
    for i in range(4):
        n=x&65535
        result=result|TableML[n]<<(16*i)
        x=x>>16
    return result

def MoveRight(Bgrid):
    global TableMR
    x=Bgrid
    result=0
    for i in range(4):
        n=x&65535
        result=result|TableMR[n]<<(16*i)
        x=x>>16
    return result
    
def Move(Bgrid,mode):#0:left 1:up 2:right 3:down
    result=0 #B
    x=Bgrid
    if mode==0:
        result=MoveLeft(Bgrid)

    elif mode==1:
        x=rotate(x,1)
        x=MoveLeft(x)
        result=rotate(x,3)

    elif mode==2:
        result=MoveRight(Bgrid)

    elif mode==3:
        x=rotate(x,1)
        x=MoveRight(x)
        result=rotate(x,3)

    moved=False
    if Bgrid!=result:
        moved=True
        
    return result,moved
        
def Add(Bgrid):
    global TableA
    x=Bgrid
    result=[[],[]]
    for i in range(4):
        n=x>>(16*i)&65535
        a=TableA[n]
        for j in range(2):
            for k in a[j]:
                result[j]+=[(x&( ~(65535<<(16*i)) ))|(k<<(16*i))]
    return result[0],result[1]

def Expectation(x):
    global POSSIBILITY
    result=-999999999999999
    
    if len(x[0])>0:
        mean1=0
        mean2=0
        
        for i in x[0]:
            mean1+=i
        mean1=mean1/len(x[0])
        for i in x[1]:
            mean2+=i
        mean2=mean2/len(x[1])
        result=(mean1*POSSIBILITY[0])+(mean2*POSSIBILITY[1])
    #if result==0:
    #    print("Expectation : 0")
    return result


def Evaluate(Bgrid):
    if Bgrid==0:
        result=-999999999999
    else:
        result=0
        rBgrid=rotate(Bgrid,1)
        #gameover=True
        """for i in range(4):
            x=(Bgrid>>(16*i))&65535
            y=(rBgrid>>(16*i))&65535
            if max(TableS[x],TableS[y])==1:
                gameover=False
                break"""

        #if gameover:
            #result=-99999999
        #else:
        for i in range(4):
            x=(Bgrid>>(16*i))&65535
            y=(rBgrid>>(16*i))&65535
            result+=TableV[x]+TableV[y]

    return result

def Depth(Bgrid):
    variety=COUNT-1
    #global DEPTHLIST
    Ogrid=BtoO(Bgrid)
    for i in range(COUNT,16):
        if i in Ogrid:
            variety+=1
    return DEPTHLIST[variety]

import random
from Calcs import *
from copy import deepcopy
import time


Grids=[]
def MakeChild(grids):
    #print(grids)
    if type(grids)==int:
        newgrids=[0]*4
        for i in range(4):
            g,m=Move(grids,i)
            if m:
                newgrids[i]=g
            else:
                newgrids[i]=0
    else:
        newgrids=[]
        for i in range(4):
            if grids[i]==0:
                newgrids+=[0]
            elif type(grids[i])==int:
                add0,add1=Add(grids[i])
                newgrids+=[[add0,add1]]
            else:
                g=[[],[]]
                for j in range(2):
                    #print(len(grids[i][j]))
                    for k in grids[i][j]:
                        g[j]+=[MakeChild(k)]
                newgrids+=[g]
    return newgrids
            

def Value(grids):
    value=0
    choice=-1
    cvalue=[0,0,0,0]
    if type(grids)==int:
        value=Evaluate(grids)

    else:
        for i in range(4):
            if type(grids[i])==int:
                cvalue[i]=Evaluate(grids[i])
            else:
                v=[[],[]]
                for j in range(2):
                    for k in grids[i][j]:
                        
                        if type(k)==int:
                            v[j]+=[Evaluate(k)]
                            #print("{} : {}".format(k,Evaluate(k)))
                        else:
                            v[j]+=[Value(k)]
                cvalue[i]=Expectation(v)

        value=max(cvalue)
    #print(cvalue)
    return value

def Choose(grids,grid):
    #print(grid)
    cvalue=[0,0,0,0]
    #grids=grid
    moved=[True]*4
    for i in range(4):
        g,m=Move(grid,i)
        moved[i]=m
    if moved.count(True)==1:
        choice=moved.index(True)
    else:

        for i in range(4):
            if type(grids[i])==int:
                if grids[i]==0:
                    cvalue[i]=Evaluate(grids[i])
                else:
                    print("ERROR")
                    
            else:
                v=[[],[]]
                for j in range(2):
                    for k in grids[i][j]:
                        v[j]+=[Value(k)]
                #print("{} : {}".format(i,v))

                cvalue[i]=Expectation(v)

        validcvalue=[]
        for i in range(4):
            if moved[i]:
                validcvalue+=[cvalue[i]]

        value=max(validcvalue)
        for i in range(4):
            if moved[i]:
                if cvalue[i]==value:
                    choice=i
                    break
        
    #choice=cvalue.index(value)
    #print(cvalue)
    return choice

def Think(grid,printdepth):
    D=Depth(grid)
    if printdepth:
        print("DEPTH : {}".format(D))
    grids=grid
    #start=time.time()
    for i in range(D):
        grids=MakeChild(grids)
    choice=Choose(grids,grid)
    #print(grids)
    return choice


class Game():
    def __init__(self):
        global POSSIBILITY
        self.Bgrid=0
        self.score=0
        self.status="OK"
        self.gameover=False

    def add(self):
        global POSSIBILITY
        self.Ogrid=BtoO(self.Bgrid)
        e=[]
        for i in range(16):
            if self.Ogrid[i]==0:
                e+=[i]
        if random.random()>POSSIBILITY[0]:
            r=2
        else:
            r=1
        self.Ogrid[random.choice(e)]=r
        self.Bgrid=OtoB(self.Ogrid)
        return self.Bgrid

    def start(self):
        for i in range(2):
            self.add()

    def Gameover(self):
        self.gameover=False
        for i in range(4):
            g,moved=Move(self.Bgrid,i)
            if moved:
                break
        else:
            self.gameover=True
        return self.gameover
        
    def Move(self,mode):
        self.Ogrid=BtoO(self.Bgrid)
        prescore=0
        for i in range(16):
            n=self.Ogrid[i]
            prescore+=n*(2**n)
        self.Bgrid,moved=Move(self.Bgrid,mode)
        newscore=0
        self.Ogrid=BtoO(self.Bgrid)
        for i in range(16):
            n=self.Ogrid[i]
            newscore+=n*(2**n)
        self.score+=(newscore-prescore)
        if moved:
            self.add()
            self.Gameover()
        else:
            self.Gameover=True
        #else:
            #self.gameover=True
            #print("NotMoved")

        return self.Bgrid,self.score

    def Print(self):
        print("SCORE : {}".format(self.score))
        Print(self.Bgrid)

import time
from Objects import *


while True:
    n=0
    start=time.time()
    Depthes=[]
    NowGame=Game()
    NowGame.start()
    while NowGame.gameover==False:
        NowGame.Print()
        Depthes+=[Depth(NowGame.Bgrid)]
        NowGame.Move(Think(NowGame.Bgrid,True))
        n+=1
    NowGame.Print()
    finish=time.time()

    print("WEIGHT : {}".format(WEIGHT))
    print("COUNT : {}".format(COUNT))
    print("DEPTHLIST : {}".format(DEPTHLIST))
    print("{}moves/sec".format(round(n/(finish-start),2)))
    for i in range(15):
        if Depthes.count(i)>0:
            print("DEPTH {} : {}%".format(i,round((100*Depthes.count(i)/len(Depthes)),2)))
    input("EnterKey to restart")
