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
        return f"{self.key}"
    
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
            self.data = self.process_data(file_path)

    def process_data(self,file:UploadFile=None) -> None:
        if file.size < chunk_file_size:
            self.process_entire_file(-1,file)
        else:
            self.process_data_per_chunk(file)
    
    def get_Data(self,n_values:int = 3,file:UploadFile=None) -> list[NumericalInstance]:
        if not self.global_instance and file is not None:
            return self.process_entire_file(n_values,file)
        else:
            return self.get_data_from_files(n_values)

    def process_entire_file(self,n_values:int,file:UploadFile=None) -> list[NumericalInstance]:
        heap = []
        i = 0
        with file.file as f:
            for line in io.TextIOWrapper(f, encoding='utf-8'):
                heapq.heappush(heap,NumericalInstance(*line.split('_'))) if (i <= n_values or n_values == -1) else heapq.heapreplace(heap,NumericalInstance(*line.split('_')))
                i += 1        
        return heapq.nlargest(n_values, heap) if n_values != -1 else heap

    def process_data_per_chunk(self:int,file:UploadFile=None) -> None:
        with file.file as f:
            for line in io.TextIOWrapper(f, encoding='utf-8'):
                hashed_key = line.split('_')[0]  // 10000
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
                        heap.put(NumericalInstanceReverseOrder(*line.split('_')))
        return heap.queue[:-1]
                
                