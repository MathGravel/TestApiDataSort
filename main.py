from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from datetime import datetime
from src.NumericalData import NumericalStructure

app = FastAPI()
default_data_treatment = NumericalStructure(global_instance=True)

@app.get("/")
def read_root():
    return {"message": "The server is currently running at the time " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

@app.get("/health")
def check_server_health():
    return {"message": "The server is currently running at the time " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


@app.get("/getValues/{nValues}")
def getValues(nValues: int):
    return {"message": "The server is currently running at the time " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")}



@app.post("/replaceDataset/")
async def upload_file(file: UploadFile = File(...)):
    contents = await file.read()
    analysis = NumericalStructure(file_path=file.filename)
    analysis.process_data(file.filename)
    return {"message": "Dataset uploaded successfully. The server is currently treating the dataset..."}


@app.post("/uploadAndTreatFile/{nResponses}")
async def upload_and_treat_file(file: UploadFile, nResponses: int = 1000):
    analysis = NumericalStructure()
    values = analysis.get_Data(nResponses,file)
    return JSONResponse(content={"values": values})
