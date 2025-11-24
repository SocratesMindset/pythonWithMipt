import random
import numpy as np
import copy
from functools import partial

def gen_norm_hist(count):
    hist = [random.random() for i in range(count)]
    hist = np.array(hist)
    hist /= hist.sum()
    return hist

def recursion_gen_norm_hist(count):
    if count >= 2:
        res = np.array([random.random()])
        return np.append(res,recursion_gen_norm_hist(count - 1))
    else:
        return random.random()

def cumulative_hist(hist, count):
    if(count < len(hist) - 1):
        hist[count+1] += hist[count]
        return cumulative_hist(hist, count+1)
    else:
        return hist

def weighted(y):
    def prod(x):
        return sum([x[i] * y[i] for i in range(len(x))])
    return prod

def func_x(x):
    def func_y(y):
        def func_z(z):
            return x+y+z
        return func_z
    return func_y

def get_intence(x,y,z,a,b,c):
    return a*x + b*y + c*z

class Hist:
    def __iter__(self):
        return self

    def __init__(self, count):
        self.count = count
        self.counter = 0

    def __next__(self):
        if self.counter < self.count:
            self.counter += 1
            return random.random()
        else:
            raise StopIteration

def hist_generator(count):
   while count > 0:
       count -= 1
       yield random.random()

def filter_05(num):
    if num > 0.5:
        return True
    else:
        return False


# --------- итераторы обхода изображения ---------

def linear_iterator(h,w):
    for i in range(h):
        for j in range(w):
            yield i,j

def spiral_center_iterator(h,w):
    total = h*w
    seen = [[False]*w for _ in range(h)]
    cx,cy = h//2, w//2
    x,y = cx,cy
    visited = 0
    if 0 <= x < h and 0 <= y < w:
        seen[x][y] = True
        visited = 1
        yield x,y
    step = 1
    dirs = [(0,1),(1,0),(0,-1),(-1,0)]
    d = 0
    while visited < total:
        for _ in range(2):
            dx,dy = dirs[d % 4]
            for _ in range(step):
                x += dx
                y += dy
                if 0 <= x < h and 0 <= y < w and not seen[x][y]:
                    seen[x][y] = True
                    visited += 1
                    yield x,y
                if visited >= total:
                    break
            d += 1
            if visited >= total:
                break
        step += 1

def zigzag_iterator(h,w):
    for s in range(h + w - 1):
        if s % 2 == 0:
            i = min(s, h-1)
            j = s - i
            while i >= 0 and j < w:
                yield i,j
                i -= 1
                j += 1
        else:
            j = min(s, w-1)
            i = s - j
            while j >= 0 and i < h:
                yield i,j
                i += 1
                j -= 1

def hilbert_curve(x0, y0, xi, xj, yi, yj, n):
    if n <= 0:
        x = x0 + (xi + yi) // 2
        y = y0 + (xj + yj) // 2
        yield int(x), int(y)
    else:
        for p in hilbert_curve(x0,             y0,             yi//2, yj//2, xi//2, xj//2, n-1): yield p
        for p in hilbert_curve(x0+xi//2,       y0+xj//2,       xi//2, xj//2, yi//2, yj//2, n-1): yield p
        for p in hilbert_curve(x0+xi//2+yi//2, y0+xj//2+yj//2, xi//2, xj//2, yi//2, yj//2, n-1): yield p
        for p in hilbert_curve(x0+xi//2+yi,    y0+xj//2+yj,   -yi//2,-yj//2,-xi//2,-xj//2, n-1): yield p

def peano_iterator(h,w):
    if h != w:
        raise ValueError("Peano iterator requires square image")
    n = h
    if n & (n - 1) != 0:
        raise ValueError("Peano iterator requires size power of 2")
    order = n.bit_length() - 1
    for i,j in hilbert_curve(0,0,n,0,0,n,order):
        yield i,j


# --------- перевод в оттенки серого (lambda) ---------

def rgb_to_gray(image):
    to_gray = lambda r,g,b: 0.299*r + 0.587*g + 0.114*b
    r = image[:,:,0].astype(float)
    g = image[:,:,1].astype(float)
    b = image[:,:,2].astype(float)
    return to_gray(r,g,b)


# --------- свёртка и фильтры ---------

def convolution_lazy(image, kernel, iterator):
    h,w = image.shape
    kh,kw = kernel.shape
    ph,pw = kh // 2, kw // 2
    for i,j in iterator(h,w):
        if i < ph or j < pw or i >= h - ph or j >= w - pw:
            continue
        region = image[i-ph:i+ph+1, j-pw:j+pw+1]
        val = float((region * kernel).sum())
        yield i,j,val

def apply_filter(image, iterator, kernel):
    res = image.copy().astype(float)
    for i,j,val in convolution_lazy(image, kernel, iterator):
        res[i,j] = val
    return res

def gaussian_kernel(size, sigma):
    ax = np.arange(-(size // 2), size // 2 + 1)
    xx,yy = np.meshgrid(ax, ax)
    kernel = np.exp(-(xx**2 + yy**2) / (2 * sigma**2))
    kernel /= kernel.sum()
    return kernel

def mse(a,b):
    diff = a.astype(float) - b.astype(float)
    return float((diff * diff).mean())


if __name__ == '__main__':
    img_rgb = np.random.randint(0, 256, (8,8,3), dtype=np.uint8)
    img_gray = rgb_to_gray(img_rgb)

    avg_kernel = np.ones((3,3), dtype=float)
    avg_kernel /= avg_kernel.sum()
    gauss_kernel = gaussian_kernel(5,1.0)

    avg_filter = partial(apply_filter, kernel=avg_kernel)
    gauss_filter = partial(apply_filter, kernel=gauss_kernel)

    res_linear = avg_filter(img_gray, linear_iterator)
    res_spiral = avg_filter(img_gray, spiral_center_iterator)
    res_zigzag = avg_filter(img_gray, zigzag_iterator)
    res_peano = avg_filter(img_gray, peano_iterator)

    print("MSE linear/spiral:", mse(res_linear, res_spiral))
    print("MSE linear/zigzag:", mse(res_linear, res_zigzag))
    print("MSE linear/peano :", mse(res_linear, res_peano))

    res_gauss_linear = gauss_filter(img_gray, linear_iterator)
    res_gauss_spiral = gauss_filter(img_gray, spiral_center_iterator)
    print("MSE gaussian linear/spiral:", mse(res_gauss_linear, res_gauss_spiral))
