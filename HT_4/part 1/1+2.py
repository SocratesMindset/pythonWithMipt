import random
import time

def matmul(A,B):
    return [[sum(A[i][k]*B[k][j] for k in range(len(B))) for j in range(len(B[0]))] for i in range(len(A))]

def matvec(A,v):
    return [sum(A[i][j]*v[j] for j in range(len(v))) for i in range(len(A))]

def trace(A):
    return sum(A[i][i] for i in range(min(len(A),len(A[0]))))

def dot(u,v):
    return sum(u[i]*v[i] for i in range(len(u)))

def histogram(v,q):
    m = min(v)
    M = max(v)
    bins = [0]*q
    for x in v:
        idx = int((x-m)/(M-m+1e-12)*q)
        if idx==q: idx=q-1
        bins[idx]+=1
    return bins

def filter_vec(v,kernel):
    r = len(kernel)//2
    out = []
    for i in range(len(v)):
        s=0
        for j in range(len(kernel)):
            idx = i+j-r
            if 0<=idx<len(v):
                s+=v[idx]*kernel[j]
        out.append(s)
    return out

def gradient(v):
    return [v[i+1]-v[i] for i in range(len(v)-1)]

def save_vector(v,filename):
    with open(filename,'w') as f:
        f.write(' '.join(str(x) for x in v))

def load_vector(filename):
    with open(filename) as f:
        return [float(x) for x in f.read().split()]

def measure_time():
    sizes=[10,100,300]
    funcs=[matmul,matvec,trace,dot,histogram,filter_vec,gradient]
    for n in sizes:
        A=[[random.random() for _ in range(n)] for _ in range(n)]
        B=[[random.random() for _ in range(n)] for _ in range(n)]
        v=[random.random() for _ in range(n)]
        for f in funcs:
            start=time.time()
            if f==matmul: f(A,B)
            elif f==matvec: f(A,v)
            elif f==trace: f(A)
            elif f==dot: f(v,v)
            elif f==histogram: f(v,10)
            elif f==filter_vec: f(v,[-1,0,1])
            elif f==gradient: f(v)
            print(f.__name__,n,time.time()-start)

