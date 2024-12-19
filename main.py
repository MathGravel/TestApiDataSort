from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
from datetime import datetime
from dataStuctures.NumericalData import NumericalStructure
from fastapi.encoders import jsonable_encoder

app = FastAPI()

default_file = './defaultDb.txt'
default_data_treatment = NumericalStructure(True, default_file)


@app.get("/health")
def check_server_health() -> JSONResponse:
    return {
        "message":
        "The server is currently running at the time " +
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }


@app.get("/getValues/{nValues}")
def getValues(nValues: int) -> JSONResponse:
    if not default_data_treatment.database_has_loaded():
        return {
            "message":
            "The database is currently being reindexed. Please try again in a few seconds"
        }
    values = default_data_treatment.get_Data(nValues)
    return JSONResponse(content={"values": values})


@app.post("/replaceDataset")
async def upload_file(file: UploadFile) -> JSONResponse:
    if not default_data_treatment.database_has_loaded():
        return {
            "message":
            "The database is currently being reindexed. Please try again in a few seconds"
        }
    default_data_treatment.process_data(file)
    return {
        "message":
        "Dataset uploaded successfully. The server is currently treating the dataset..."
    }


@app.post("/uploadAndTreatFile/{nResponses}")
async def upload_and_treat_file(file: UploadFile,
                                nResponses: int = 1000) -> JSONResponse:
    analysis = NumericalStructure()
    values = analysis.get_Data(nResponses, file)
    return JSONResponse(content={"values": values})
