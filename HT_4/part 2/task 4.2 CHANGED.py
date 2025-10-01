
import argparse
import json
import struct
import sys
from pathlib import Path
from typing import Tuple

import numpy as np

try:
    import cv2  
    HAS_CV2 = True
except Exception:
    HAS_CV2 = False
    from PIL import Image 


def _read_image(path: str) -> np.ndarray:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Input image not found: {path}")
    if HAS_CV2:
        img = cv2.imdecode(np.fromfile(str(p), dtype=np.uint8), cv2.IMREAD_COLOR)
        if img is None:
            raise ValueError(f"Unsupported or broken image: {path}")
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img
    else:
        img = Image.open(str(p)).convert("RGB")
        return np.array(img)


def _write_image(path: str, img_rgb: np.ndarray) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    if HAS_CV2:
        bgr = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2BGR)
        ext = p.suffix.lower()
        success, buf = cv2.imencode(ext if ext else ".png", bgr)
        if not success:
            raise RuntimeError("Failed to encode output image")
        buf.tofile(str(p))
    else:
        Image.fromarray(img_rgb).save(str(p))


def hist_256(img_rgb: np.ndarray) -> np.ndarray:
    if img_rgb.ndim == 3 and img_rgb.shape[2] == 3:
        if HAS_CV2:
            ycrcb = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2YCrCb)
            y = ycrcb[..., 0]
        else:
            r, g, b = img_rgb[..., 0], img_rgb[..., 1], img_rgb[..., 2]
            y = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)
    else:
        y = img_rgb.astype(np.uint8)
    hist, _ = np.histogram(y, bins=256, range=(0, 255))
    return hist.astype(np.int64)


def save_hist(path: str, hist: np.ndarray) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    suf = p.suffix.lower()
    if suf in (".txt", ".dat"):
        p.write_text(" ".join(map(str, hist.tolist())), encoding="utf-8")
    elif suf == ".csv":
        p.write_text(",".join(map(str, hist.tolist())), encoding="utf-8")
    elif suf == ".json":
        p.write_text(json.dumps(hist.tolist()), encoding="utf-8")
    elif suf in (".bin", ".raw"):
        with open(p, "wb") as f:
            f.write(struct.pack("<256I", *hist.tolist()))
    elif suf == ".wav":
        write_hist_as_wav(str(p), hist)
    else:
        p.with_suffix(".txt").write_text(" ".join(map(str, hist.tolist())), encoding="utf-8")


def load_hist(path: str) -> np.ndarray:
    p = Path(path)
    suf = p.suffix.lower()
    if suf in (".txt", ".dat"):
        data = list(map(int, p.read_text(encoding="utf-8").split()))
    elif suf == ".csv":
        data = list(map(int, p.read_text(encoding="utf-8").replace("\n", "").split(",")))
    elif suf == ".json":
        data = json.loads(p.read_text(encoding="utf-8"))
    elif suf in (".bin", ".raw"):
        with open(p, "rb") as f:
            data = list(struct.unpack("<256I", f.read(256 * 4)))
    elif suf == ".wav":
        data = read_hist_from_wav(str(p))
    else:
        raise ValueError(f"Unsupported histogram format: {suf}")
    arr = np.array(data, dtype=np.int64)
    if arr.size != 256:
        raise ValueError(f"Histogram must have 256 values, got {arr.size}")
    return arr


def equalize_image(img_rgb: np.ndarray) -> np.ndarray:
    if HAS_CV2:
        if img_rgb.ndim == 3 and img_rgb.shape[2] == 3:
            ycrcb = cv2.cvtColor(img_rgb, cv2.COLOR_RGB2YCrCb)
            ycrcb[..., 0] = cv2.equalizeHist(ycrcb[..., 0])
            return cv2.cvtColor(ycrcb, cv2.COLOR_YCrCb2RGB)
        else:
            return cv2.equalizeHist(img_rgb)
    else:
        if img_rgb.ndim == 3 and img_rgb.shape[2] == 3:
            r, g, b = img_rgb[..., 0], img_rgb[..., 1], img_rgb[..., 2]
            y = (0.299 * r + 0.587 * g + 0.114 * b).astype(np.uint8)
            hist, bins = np.histogram(y.flatten(), 256, [0, 256])
            cdf = hist.cumsum()
            cdf_masked = np.ma.masked_equal(cdf, 0)
            cdf_m = (cdf_masked - cdf_masked.min()) * 255 / (cdf_masked.max() - cdf_masked.min())
            cdf_final = np.ma.filled(cdf_m, 0).astype(np.uint8)
            y_eq = cdf_final[y]
            scale = (y_eq.astype(np.float32) + 1e-6) / (y.astype(np.float32) + 1e-6)
            r2 = np.clip(r.astype(np.float32) * scale, 0, 255).astype(np.uint8)
            g2 = np.clip(g.astype(np.float32) * scale, 0, 255).astype(np.uint8)
            b2 = np.clip(b.astype(np.float32) * scale, 0, 255).astype(np.uint8)
            return np.stack([r2, g2, b2], axis=-1)
        else:
            y = img_rgb
            hist, bins = np.histogram(y.flatten(), 256, [0, 256])
            cdf = hist.cumsum()
            cdf_masked = np.ma.masked_equal(cdf, 0)
            cdf_m = (cdf_masked - cdf_masked.min()) * 255 / (cdf_masked.max() - cdf_masked.min())
            cdf_final = np.ma.filled(cdf_m, 0).astype(np.uint8)
            return cdf_final[y]


def gamma_correction(img_rgb: np.ndarray, gamma: float = 1.0) -> np.ndarray:
    if gamma <= 0:
        raise ValueError("gamma must be > 0")
    inv = 1.0 / gamma
    lut = (np.linspace(0, 1, 256) ** inv * 255.0).astype(np.uint8)
    out = lut[img_rgb]
    return out


def write_hist_as_wav(path: str, hist: np.ndarray, samplerate: int = 8000) -> None:
    p = Path(path)
    p.parent.mkdir(parents=True, exist_ok=True)
    h = hist.astype(np.float64)
    if h.max() > 0:
        h = (h - h.min()) / (h.max() - h.min()) * 255.0
    samples = h.astype(np.uint8).tobytes() * 64 
    num_channels = 1
    bits_per_sample = 8
    byte_rate = samplerate * num_channels * bits_per_sample // 8
    block_align = num_channels * bits_per_sample // 8
    data_size = len(samples)
    riff_size = 36 + data_size
    with open(p, "wb") as f:
        f.write(b"RIFF")
        f.write(struct.pack("<I", riff_size))
        f.write(b"WAVEfmt ")
        f.write(struct.pack("<IHHIIHH", 16, 1, num_channels, samplerate, byte_rate, block_align, bits_per_sample))
        f.write(b"data")
        f.write(struct.pack("<I", data_size))
        f.write(samples)


def read_hist_from_wav(path: str) -> list:
    with open(path, "rb") as f:
        data = f.read()
    idx = data.find(b"data")
    if idx < 0:
        raise ValueError("Invalid WAV: no data chunk")
    size = struct.unpack("<I", data[idx + 4 : idx + 8])[0]
    audio = data[idx + 8 : idx + 8 + size]
    if len(audio) < 256:
        raise ValueError("WAV doesn't contain 256 samples")
    first256 = audio[:256]
    return list(first256)


def parse_args(argv=None):
    ap = argparse.ArgumentParser(description="Image processing: histogram equalization & gamma correction.")
    ap.add_argument("-i", "--input", required=True, help="Path to input image (jpg/png/bmp/...)")
    ap.add_argument("-o", "--output", required=True, help="Path to save processed image")
    ap.add_argument("-m", "--method", choices=["equalize", "gamma"], required=True, help="Transformation method")
    ap.add_argument("--gamma", type=float, default=1.0, help="Gamma value for --method gamma")
    ap.add_argument("--save-hist", help="Optional path to save 256-bin histogram (txt/csv/json/bin/wav)")
    ap.add_argument("--load-hist", help="Optional path to load a 256-bin histogram (txt/csv/json/bin/wav). Not required for transforms, for study/demo only.")
    return ap.parse_args(argv)


def main(argv=None):
    args = parse_args(argv)

    img = _read_image(args.input)

    if args.load_hist:
        _ = load_hist(args.load_hist) 

    if args.method == "equalize":
        out = equalize_image(img)
    elif args.method == "gamma":
        out = gamma_correction(img, args.gamma)
    else:
        raise ValueError("Unknown method")

    if args.save_hist:
        save_hist(args.save_hist, hist_256(out))

    _write_image(args.output, out)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)
