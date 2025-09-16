import random

def print_table(op):
    ops = {
        '+': lambda a,b: a+b,
        '-': lambda a,b: a-b,
        '*': lambda a,b: a*b,
        '/': lambda a,b: a/b if b!=0 else float('inf')
    }
    f = ops[op]
    for i in range(1,10):
        row = []
        for j in range(1,10):
            val = f(i,j)
            s = f"{val:.2f}" if op=='/' else str(val)
            row.append(s.rjust(6))
        print(''.join(row))