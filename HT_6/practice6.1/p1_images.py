import numpy as np
from collections import deque
from dataclasses import dataclass

@dataclass
class BinaryImage:
    data: np.ndarray
    def __post_init__(self):
        a = np.asarray(self.data)
        if a.ndim != 2:
            raise ValueError("binary image must be 2D")
        if a.dtype != np.uint8:
            a = a.astype(np.uint8)
        a = np.where(a > 0, 255, 0).astype(np.uint8)
        object.__setattr__(self, "data", a)
    @property
    def shape(self):
        return self.data.shape

@dataclass
class MonoImage:
    data: np.ndarray
    def __post_init__(self):
        a = np.asarray(self.data)
        if a.ndim != 2:
            raise ValueError("mono image must be 2D")
        if a.dtype != np.uint8:
            a = np.clip(a, 0, 255).astype(np.uint8)
        object.__setattr__(self, "data", a)
    @property
    def shape(self):
        return self.data.shape

@dataclass
class ColorImage:
    data: np.ndarray
    def __post_init__(self):
        a = np.asarray(self.data)
        if a.ndim != 3 or a.shape[2] != 3:
            raise ValueError("color image must be HxWx3")
        if a.dtype != np.uint8:
            a = np.clip(a, 0, 255).astype(np.uint8)
        object.__setattr__(self, "data", a)
    @property
    def shape(self):
        return self.data.shape

class ImageConverter:
    @staticmethod
    def mono_to_mono_stat(m: MonoImage, target_mean: float = 127.0, target_std: float = 64.0) -> MonoImage:
        a = m.data.astype(np.float32)
        mean = float(a.mean())
        std = float(a.std()) if float(a.std()) > 1e-6 else 1.0
        out = (a - mean) / std * target_std + target_mean
        out = np.clip(out, 0, 255).astype(np.uint8)
        return MonoImage(out)

    @staticmethod
    def color_to_color_stat(c: ColorImage, target_means=(127.0, 127.0, 127.0), target_stds=(64.0, 64.0, 64.0)) -> ColorImage:
        a = c.data.astype(np.float32)
        out = np.empty_like(a)
        for ch in range(3):
            chdat = a[..., ch]
            mean = float(chdat.mean())
            std = float(chdat.std()) if float(chdat.std()) > 1e-6 else 1.0
            out[..., ch] = np.clip((chdat - mean) / std * target_stds[ch] + target_means[ch], 0, 255)
        return ColorImage(out.astype(np.uint8))

    @staticmethod
    def bin_to_bin(b: BinaryImage) -> BinaryImage:
        return BinaryImage(b.data.copy())

    @staticmethod
    def color_to_mono(c: ColorImage) -> MonoImage:
        a = c.data.astype(np.float32)
        g = ((a[..., 0] + a[..., 1] + a[..., 2]) / 3.0).astype(np.uint8)
        return MonoImage(g)

    @staticmethod
    def mono_to_color(m: MonoImage, palette: np.ndarray | None = None) -> ColorImage:
        if palette is None:
            p = np.arange(256, dtype=np.uint8)
            palette = np.stack([p, p, p], axis=1)
        pal = np.asarray(palette, dtype=np.uint8)
        if pal.shape != (256, 3):
            raise ValueError("palette must be 256x3")
        out = pal[m.data]
        return ColorImage(out)

    @staticmethod
    def mono_to_bin(m: MonoImage, threshold: int | None = None) -> BinaryImage:
        a = m.data
        if threshold is None:
            hist = np.bincount(a.ravel(), minlength=256).astype(np.float64)
            total = a.size
            sum_total = np.dot(np.arange(256), hist)
            sumB = 0.0
            wB = 0.0
            maxVar = -1.0
            thresh = 0
            for t in range(256):
                wB += hist[t]
                if wB == 0:
                    continue
                wF = total - wB
                if wF == 0:
                    break
                sumB += t * hist[t]
                mB = sumB / wB
                mF = (sum_total - sumB) / wF
                var = wB * wF * (mB - mF) ** 2
                if var > maxVar:
                    maxVar = var
                    thresh = t
            threshold = int(thresh)
        out = np.where(a > threshold, 255, 0).astype(np.uint8)
        return BinaryImage(out)

    @staticmethod
    def bin_to_mono_distance(b: BinaryImage) -> MonoImage:
        a = (b.data > 0).astype(np.uint8)
        h, w = a.shape
        inf = 10**9
        dist = np.full((h, w), inf, dtype=np.int32)
        dq = deque()
        for y in range(h):
            for x in range(w):
                if a[y, x] == 1:
                    dist[y, x] = 0
                    dq.append((y, x))
        dirs = [(1, 0), (-1, 0), (0, 1), (0, -1)]
        while dq:
            y, x = dq.popleft()
            d = dist[y, x] + 1
            for dy, dx in dirs:
                ny, nx = y + dy, x + dx
                if 0 <= ny < h and 0 <= nx < w and d < dist[ny, nx]:
                    dist[ny, nx] = d
                    dq.append((ny, nx))
        maxd = dist.max() if dist.max() > 0 and dist.max() < 10**9 else 1
        dist = np.where(dist >= 10**9, maxd, dist)
        norm = (dist.astype(np.float32) / maxd * 255.0).astype(np.uint8)
        return MonoImage(norm)

    @staticmethod
    def color_to_bin(c: ColorImage, threshold: int | None = None) -> BinaryImage:
        return ImageConverter.mono_to_bin(ImageConverter.color_to_mono(c), threshold=threshold)

    @staticmethod
    def bin_to_color(b: BinaryImage, palette: np.ndarray | None = None) -> ColorImage:
        m = ImageConverter.bin_to_mono_distance(b)
        return ImageConverter.mono_to_color(m, palette=palette)
