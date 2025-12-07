import cv2
import numpy as np
import re
from pathlib import Path

def load_and_binarize(path: str | Path, threshold: int = 127) -> np.ndarray:
    path = Path(path)
    img = cv2.imread(str(path), cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError(f"Не удалось открыть изображение: {path}")
    _, bin_img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)
    bin_img = (bin_img // 255).astype(np.uint8)
    return bin_img

def split_to_blocks(bin_img: np.ndarray, block_size: int = 16) -> np.ndarray:
    h, w = bin_img.shape
    h_cropped = (h // block_size) * block_size
    w_cropped = (w // block_size) * block_size
    bin_img = bin_img[:h_cropped, :w_cropped]
    n_blocks_y = h_cropped // block_size
    n_blocks_x = w_cropped // block_size
    block_bits = np.zeros((n_blocks_y, n_blocks_x), dtype=np.uint8)
    for by in range(n_blocks_y):
        for bx in range(n_blocks_x):
            block = bin_img[
                by * block_size : (by + 1) * block_size,
                bx * block_size : (bx + 1) * block_size,
            ]
            ones = int(block.sum())
            zeros = block.size - ones
            block_bits[by, bx] = 1 if ones >= zeros else 0
    return block_bits

def flatten_blocks(block_bits: np.ndarray) -> str:
    flat = block_bits.flatten()  # по строкам
    return ''.join(str(int(v)) for v in flat)

def count_cross_patterns(block_bits: np.ndarray) -> int:
    pattern_matrix = np.array(
        [[0, 1, 0],
         [1, 1, 1],
         [0, 1, 0]],
        dtype=np.uint8,
    )
    target_str = ''.join(str(int(v)) for v in pattern_matrix.flatten())
    regex = re.compile(target_str)
    h, w = block_bits.shape
    count = 0
    for y in range(h - 2):
        for x in range(w - 2):
            patch = block_bits[y:y + 3, x:x + 3]
            s = ''.join(str(int(v)) for v in patch.flatten())
            if regex.fullmatch(s):
                count += 1
    return count

def process_image(path: str | Path, block_size: int = 16, threshold: int = 127) -> None:
    print(f'Обработка файла: {path}')
    bin_img = load_and_binarize(path, threshold=threshold)
    print(f'  Размер бинарного изображения: {bin_img.shape[1]}x{bin_img.shape[0]}')
    block_bits = split_to_blocks(bin_img, block_size=block_size)
    n_blocks_y, n_blocks_x = block_bits.shape
    print(f'  Размер решётки блоков: {n_blocks_x} x {n_blocks_y} (всего {n_blocks_x * n_blocks_y} блоков)')
    code = flatten_blocks(block_bits)
    print(f'  Длина кодовой строки: {len(code)}')
    crosses = count_cross_patterns(block_bits)
    print(f'  Количество паттернов "крест": {crosses}')
    print()

if __name__ == "__main__":
    base_dir = Path(__file__).resolve().parent
    img_dir = base_dir / "img_examples" / "img_examples"
    for img_name in ("example1.png", "example2.png"):
        img_path = img_dir / img_name
        process_image(img_path, block_size=16, threshold=127)
