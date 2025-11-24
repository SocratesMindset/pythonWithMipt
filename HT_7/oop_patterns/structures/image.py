import cv2

"""
Абстрактная фабрика 
"""


class AbstractFactoryImageReader:
    def read_image(self, file_path):
        raise NotImplementedError()


class BinImageReader(AbstractFactoryImageReader):
    """
    Чтение бинарного изображения:
    читаем в оттенках серого и порогом преобразуем к 0/255.
    """
    def read_image(self, file_path):
        gray = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if gray is None:
            raise RuntimeError(f"Не удалось открыть файл {file_path}")
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return binary


class MonochromeImageReader(AbstractFactoryImageReader):
    """
    Чтение монохромного (градации серого) изображения.
    """
    def read_image(self, file_path):
        image = cv2.imread(file_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            raise RuntimeError(f"Не удалось открыть файл {file_path}")
        return image


class ColorImageReader(AbstractFactoryImageReader):
    """
    Чтение цветного изображения (BGR).
    """
    def read_image(self, file_path):
        image = cv2.imread(file_path, cv2.IMREAD_COLOR)
        if image is None:
            raise RuntimeError(f"Не удалось открыть файл {file_path}")
        return image


def get_image_reader(ident):
    if ident == 0:
        return BinImageReader()
    elif ident == 1:
        return MonochromeImageReader()
    elif ident == 2:
        return ColorImageReader()
    else:
        raise ValueError("Неизвестный идентификатор ридера изображения: %s" % ident)


if __name__ == "__main__":
    try:
        for i in range(3):
            print(get_image_reader(i))
    except Exception as e:
        print(e)
