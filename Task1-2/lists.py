import random

def listsTaskOne():
    nums=[]
    for i in range(int(random.randint(1,50))):
        current=input("please type number which you want append in list")
        nums.append(int(current))
        if (len(nums)==1):
            max=nums[0]
            min=nums[0]
        if(nums[i]>max):
            max=nums[i]
        if(nums[i]<min):
            min=nums[i]
    nums.sort()
    if (len(nums)%2!=0):
        print(f"maximum value is {max} minimum value is {min}  medium value is {nums[int((len(nums))/2)]}")
    else:
        print(f"maximum value is {max} minimum value is {min} medium value is {int((nums[int((len(nums)/2))]+nums[int(len(nums)/2)+1])/2)}")

def listsTaskTwo(nums):
    counts = [0] * 11
    n = len(nums)
    i = 0
    while i < n:
        x = nums[i]
        if x == 100:
            bin_idx = 10
        else:
            bin_idx = x // 10
        counts[bin_idx] = counts[bin_idx] + 1
        i = i + 1
    probs = [0.0] * 11
    i = 0
    while i < 11:
        if n > 0:
            probs[i] = counts[i] / float(n)
        else:
            probs[i] = 0.0
        i = i + 1
    return counts, probs

def listsTaskThreeSum(a, b):
    # длины должны совпадать
    res = [0] * len(a)
    i = 0
    while i < len(a):
        res[i] = a[i] + b[i]
        i = i + 1
    return res

def listsTaskThreeHadamard(a, b):
    res = [0] * len(a)
    i = 0
    while i < len(a):
        res[i] = a[i] * b[i]
        i = i + 1
    return res

def listsTaskThreeDot(a, b):
    s = 0
    i = 0
    while i < len(a):
        s = s + a[i] * b[i]
        i = i + 1
    return s

def listsTaskThreeNorm(a):
    s = 0.0
    i = 0
    while i < len(a):
        s = s + a[i] * a[i]
        i = i + 1
    return s ** 0.5

def listsTaskThreeScale(a, k):
    res = [0] * len(a)
    i = 0
    while i < len(a):
        res[i] = a[i] * k
        i = i + 1
    return res

def listsTaskThreeAll(a, b, scalar):
    s = listsTaskThreeSum(a, b)
    h = listsTaskThreeHadamard(a, b)
    na = listsTaskThreeNorm(a)
    nb = listsTaskThreeNorm(b)
    if na >= nb:
        bigger_scaled = listsTaskThreeScale(a, scalar)
    else:
        bigger_scaled = listsTaskThreeScale(b, scalar)
    return s, h, bigger_scaled

def listsTaskFour(mat, vec):
    r = len(mat)
    if r == 0:
        return []
    c = len(mat[0])
    i = 0
    while i < r:
        if len(mat[i]) != c:
            raise ValueError("Матрица должна быть прямоугольной")
        i = i + 1
    if len(vec) != c:
        raise ValueError("Длины не совпадают")
    res = [0] * r
    i = 0
    while i < r:
        j = 0
        s = 0
        while j < c:
            s = s + mat[i][j] * vec[j]
            j = j + 1
        res[i] = s
        i = i + 1
    return res

def listsTaskFive(nums):
    res = nums[:]
    n = len(nums)
    i = 0
    while i < n:
        if nums[i] < 0:
            li = i - 1
            left_val_found = False
            left_val = 0
            while li >= 0:
                if nums[li] > 0:
                    left_val = nums[li]
                    left_val_found = True
                    break
                li = li - 1
            ri = i + 1
            right_val_found = False
            right_val = 0
            while ri < n:
                if nums[ri] > 0:
                    right_val = nums[ri]
                    right_val_found = True
                    break
                ri = ri + 1
            if left_val_found and right_val_found:
                res[i] = (left_val + right_val) / 2.0
            elif left_val_found:
                res[i] = left_val
            elif right_val_found:
                res[i] = right_val
            else:
                res[i] = nums[i]
        i = i + 1
    return res

def listsTaskSix(data, kernel):
    n = len(data)
    m = len(kernel)
    if m == 0:
        raise ValueError("Ядро пустое")
    if n < m:
        return []
    out_len = n - m + 1
    out = [0] * out_len
    i = 0
    while i < out_len:
        j = 0
        s = 0
        while j < m:
            s = s + data[i + j] * kernel[j]
            j = j + 1
        out[i] = s
        i = i + 1
    return out


if __name__ == '__main__':
    listsTaskOne()
    counts, probs = listsTaskTwo([0, 5, 10, 19, 20, 35, 99, 100])
    print("2:", counts, probs)
    s, h, bs = listsTaskThreeAll([1, 2, 3], [4, -1, 0], 2)
    print("3:", s, h, bs)
    mv = listsTaskFour([[1, 2], [3, 4], [5, 6]], [10, -1])
    print("4:", mv)
    print("5:", listsTaskFive([-3, -2, 5, -1, -7, 4, -2]))
    print("6:", listsTaskSix([1, 2, 3, 4, 5], [1, 0, -1]))
    """вызов функций"""