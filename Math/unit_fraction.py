import math


def coprime(a,b):
    g=math.gcd(a,b)
    x,y=int(a/g),int(b/g)
    return x,y


def unit_fraction(n,a,b,ex):#a/b
    c,d=coprime(a,b)
    result=0
    pex=[]
    if n==1:
        if c==1:
            result=d
        else:
            result=0
        pex=ex
    else:
        m=1
        if len(ex)>0:
            m=max(max(ex),math.ceil(d/c))
            
        M=math.floor((n*d)/c)
        for i in range(m+1,M+1):
            x,y=(c*i)-d,d*i
            r,pex=unit_fraction(n-1,x,y,ex+[i])
            if r!=0:
                break
        else:
            r=0

        result=r
    
    return result,pex


#探索する上限
LIM=10
print("0 < 分子 < 分母 で整数値を入力")
a=int(input("分子："))
b=int(input("分母："))

for i in range(1,LIM+1):
    r,ex=unit_fraction(i,a,b,[])
    if r!=0:
        ex=ex+[r]
        ans="{}/{} = ".format(a,b)
        for j in ex:
            ans+="1/{}".format(j)
            if j!=max(ex):
                ans+=" + "
        break
else:
    print("No solution")

print(ans)
