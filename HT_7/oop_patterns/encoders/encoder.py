import sys
import struct
import csv
import json

"""
Стратегия (Strategy) для записи гистограмм.
"""


class HistEncoder:
    @staticmethod
    def encode(file_path, data):
        """
        file_path — имя выходного файла
        data — словарь вида {int: float} длиной 256.
        """
        raise NotImplementedError()


class BinHistEncoder(HistEncoder):
    @staticmethod
    def encode(file_path, data):
        values = [float(data.get(i, 0.0)) for i in range(256)]
        with open(file_path, "wb") as file:
            packed = struct.pack("f" * len(values), *values)
            file.write(packed)


class CsvHistEncoder(HistEncoder):
    @staticmethod
    def encode(file_path, data):
        with open(file_path, "w", newline="") as csv_file:
            writer = csv.writer(csv_file)
            for key in sorted(data.keys()):
                writer.writerow([key, data[key]])


class TxtHistEncoder(HistEncoder):
    @staticmethod
    def encode(file_path, data):
        with open(file_path, "w") as file:
            for key in sorted(data.keys()):
                file.write(f"{key} {data[key]}\n")


class JsonHistEncoder(HistEncoder):
    @staticmethod
    def encode(file_path, data):
        keys = sorted(data.keys())
        values = [data[k] for k in keys]
        payload = {"keys": keys, "values": values}
        with open(file_path, "w") as file:
            json.dump(payload, file)
