import random

def create_vector(n):
    return [random.random() for _ in range(n)]

def create_matrix(m,n):
    return [[random.random() for _ in range(n)] for _ in range(m)]

def matvec_mul(A, v):
    return [sum(A[i][j]*v[j] for j in range(len(v))) for i in range(len(A))]

def print_vector(v):
    print('['+', '.join(f"{x:.6f}" for x in v)+']')

def print_matrix(A):
    for row in A:
        print('['+', '.join(f"{x:.6f}" for x in row)+']')

def diag_sum(A):
    n = min(len(A), len(A[0]) if A else 0)
    s1 = sum(A[i][i] for i in range(n))
    s2 = sum(A[i][n-1-i] for i in range(n))
    if n%2==1:
        return s1+s2-A[n//2][n//2]
    return s1+s2

def conv2d(img, kernel, stride=1, padding='valid'):
    kh, kw = len(kernel), len(kernel[0])
    ih, iw = len(img), len(img[0])
    if padding == 'same':
        ph = (kh-1)//2
        pw = (kw-1)//2
        padded = [[0.0]*(iw+2*pw) for _ in range(ih+2*ph)]
        for i in range(ih):
            for j in range(iw):
                padded[i+ph][j+pw]=img[i][j]
    else:
        ph = pw = 0
        padded = img
    oh = (len(padded)-kh)//stride+1
    ow = (len(padded[0])-kw)//stride+1
    out = [[0.0 for _ in range(ow)] for _ in range(oh)]
    for i in range(0, oh):
        for j in range(0, ow):
            s = 0.0
            for ki in range(kh):
                for kj in range(kw):
                    s += padded[i*stride+ki][j*stride+kj]*kernel[ki][kj]
            out[i][j]=s
    return out