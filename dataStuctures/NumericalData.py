import os
import heapq
from fastapi import UploadFile
import io
import json
import functools
from pathlib import Path

chunk_file_size = 100000
process_folder = './__processFiles__'


class NumericalInstance:

    def __init__(self, key, value):
        self.key = int(key)
        self.value = int(value)

    def __lt__(self, other) -> bool:
        return self.value < other.value

    def __eq__(self, other) -> bool:
        return self.value == other.value

    def __str__(self) -> str:
        return f"Key: {self.key}, Value: {self.value}"

    def __repr__(self) -> str:
        return f"Key: {self.key}, Value: {self.value}"

    def to_json(self) -> str:
        return json.dumps({"key": self.key, "value": self.value})


class NumericalStructure:

    def __init__(self, global_instance: bool = False, file_path: str = None):
        self.global_instance = global_instance
        self.data = []
        self.chunkData = False
        if file_path is not None:
            file = open(file_path, "r")
            size = os.path.getsize(file_path)
            self._process_data(file, size)

    def database_has_loaded(self) -> bool:
        return len(self.data) > 0 or self.chunkData

    @functools.cache
    def process_data(self, file: UploadFile = None) -> None:
        if file:
            with file.file as f:
                fileReader = io.TextIOWrapper(f, encoding='utf-8')
                self._process_data(fileReader, file.size)

    def _process_data(self,
                      file: io.TextIOWrapper = None,
                      fileSize: bytes = 0) -> None:
        if fileSize < chunk_file_size:
            self.process_entire_file(-1, file)
            self.chunkData = False
        else:
            self.process_data_per_chunk(file, fileSize)
            self.chunkData = True

    def get_Data(self,
                 n_values: int = 3,
                 file: UploadFile = None) -> list[NumericalInstance]:
        if not self.global_instance and file is not None:
            fileReader = io.TextIOWrapper(file.file, encoding='utf-8')
            return [
                x.key for x in self.process_entire_file(n_values, fileReader)
            ]
        elif self.chunkData:
            return [x.key for x in self.data_from_files(n_values)]
        else:
            return [x.key for x in self.data[:n_values]]

    def process_entire_file(
            self,
            n_values: int,
            file: io.TextIOWrapper = None) -> list[NumericalInstance]:
        heap = []
        i = 0
        for line in file:
            heapq.heappush(heap, NumericalInstance(*line.split('_'))) if (
                i <= n_values or n_values == -1) else heapq.heapreplace(
                    heap, NumericalInstance(*line.split('_')))
            i += 1
        self.data = heap
        return heapq.nlargest(n_values, heap) if n_values != -1 else heap

    def process_data_per_chunk(self: int,
                               file: io.TextIOWrapper = None,
                               size: bytes = 0) -> None:
        Path(process_folder).mkdir(parents=True, exist_ok=True)
        fileWrites = [open(f"{process_folder}/{i}.txt", 'w')
                      for i in range(10)]

        for line in file:
            hashed_key = int(line.split('_')[0]) % 10
            fileWrites[hashed_key].write(line)
        (f.close() for f in fileWrites)
        for txt_file in os.listdir(process_folder):
            if txt_file.endswith('.txt'):
                allData = []
                with open(os.path.join(process_folder, txt_file), 'r') as f:
                    allData = [
                        NumericalInstance(*line.split('_'))
                        for line in f.readlines()
                    ]
                    allData.sort(reverse=True, key=lambda x: x.value)
                with open(os.path.join(process_folder, txt_file), 'w') as f:
                    for data in allData:
                        f.write(f'{data.key}_{data.value}\n')

    def data_from_files(self, n_values: int = 3) -> list[NumericalInstance]:
        heap = []
        for txt_file in os.listdir(process_folder):
            if txt_file.endswith('.txt'):
                with open(os.path.join(process_folder, txt_file), 'r') as f:
                    for i in range(n_values):
                        line = f.readline()
                        if len(line.strip()) < 1:
                            continue
                        heapq.heappush(heap, NumericalInstance(
                            *line.split('_'))) if (
                                i <= n_values or
                                n_values == -1) else heapq.heapreplace(
                                    heap, NumericalInstance(*line.split('_')))

        return heapq.nlargest(n_values, heap) if n_values != -1 else heap
