from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from datetime import datetime
from src.NumericalData import NumericalStructure

app = FastAPI()
default_data_treatment = NumericalStructure(global_instance=True)


@app.get("/health")
def check_server_health() -> JSONResponse:
    return {"message": "The server is currently running at the time " + datetime.now().strftime("%Y-%m-%d %H:%M:%S")}


@app.get("/getValues/{nValues}")
def getValues(nValues: int) -> JSONResponse:
    values = default_data_treatment.get_Data(nValues)
    return JSONResponse(content={"values": values})



@app.post("/replaceDataset/")
async def upload_file(file: UploadFile = File(...)) -> JSONResponse:
    contents = await file.read()
    default_data_treatment.process_data(file)
    return {"message": "Dataset uploaded successfully. The server is currently treating the dataset..."}


@app.post("/uploadAndTreatFile/{nResponses}")
async def upload_and_treat_file(file: UploadFile, nResponses: int = 1000) -> JSONResponse:
    analysis = NumericalStructure()
    values = analysis.get_Data(nResponses,file)
    return JSONResponse(content={"values": [str(x) for x in values]})
