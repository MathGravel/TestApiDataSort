import os
import heapq
from fastapi import UploadFile, File
import io
import json
from queue import PriorityQueue

chunk_file_size = 100000
process_folder = './__processFiles__'

class NumericalInstance:
    def __init__(self,key,value):
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
        return json.dumps({"key":self.key,"value":self.value})

class NumericalInstanceReverseOrder(NumericalInstance):
    def __lt__(self, other) -> bool:
        return self.value > other.value


class NumericalStructure:
    def __init__(self,global_instance:bool=False,file_path:str=None):
        self.global_instance = global_instance
        self.data = []
        if not file_path is None:
            file = open(file_path, "r")
            size = os.path.getsize(file_path)
            self.data = self._process_data(file,size)
    
    def database_has_loaded(self) -> bool:
        return len(self.data) > 0

    def process_data(self,file:UploadFile=None) -> None:
        if file:
            with file.file as f:
                fileReader = io.TextIOWrapper(f, encoding='utf-8')
                self._process_data(fileReader,f.size)

    def _process_data(self,file: io.TextIOWrapper = None,fileSize:bytes = 0) -> None:
        if fileSize < chunk_file_size:
            self.process_entire_file(-1,file)
        else:
            self.process_data_per_chunk(file)

    def get_Data(self,n_values:int = 3,file:UploadFile=None) -> list[NumericalInstance]:
        if not self.global_instance and file is not None:
            fileReader = io.TextIOWrapper(file.file, encoding='utf-8')
            return [x.key for x in self.process_entire_file(n_values,fileReader)]
        else:
            return [x.key for x in self.get_data_from_files(n_values)]

    def process_entire_file(self,n_values:int,file:io.TextIOWrapper = None) -> list[NumericalInstance]:
        heap = []
        i = 0
        for line in file:
            heapq.heappush(heap,NumericalInstance(*line.split('_'))) if (i <= n_values or n_values == -1) else heapq.heapreplace(heap,NumericalInstance(*line.split('_')))
            i += 1        
        return heapq.nlargest(n_values, heap) if n_values != -1 else heap

    def process_data_per_chunk(self:int,file:io.TextIOWrapper = None) -> None:
        for line in file :
            hashed_key = int(line.split('_')[0])  // 10000
            with open(f"{process_folder}/{hashed_key}.txt",'a') as f:
                f.write(line)
        for txt_file in os.listdir(process_folder):
            if txt_file.endswith('.txt'):
                allData = []
                with open(os.path.join(process_folder, txt_file), 'r') as f:
                    allData = [NumericalInstance(*line.split('_')) for line in f.readlines()]
                    allData.sort(key=lambda x: x.value)
                with open(os.path.join(process_folder, txt_file), 'w') as f:
                    for data in allData:
                        f.write(f'{data.key}_{data.value}\n')
                        
                        
    def get_data_from_files(self,nvalues:int = 3) -> list[NumericalInstance]:
        heap = PriorityQueue(nvalues+1)
        i = 0
        for txt_file in os.listdir(process_folder):
            if txt_file.endswith('.txt'):
                with open(os.path.join(process_folder, txt_file), 'r') as f:
                    for i in range(nvalues):
                        line = f.readline() 
                        if len(line.strip()) < 1:
                            continue
                        heap.put(NumericalInstanceReverseOrder(*line.split('_')))
        return heap.queue[:-1]
                
                