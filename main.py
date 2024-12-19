from fastapi import FastAPI, UploadFile, File, HTTPException
from fastapi import  Request, Response
from typing import Awaitable, Callable
from fastapi.responses import JSONResponse
from datetime import datetime
from dataStuctures.NumericalData import NumericalStructure
from pyinstrument import Profiler
import yaml

app = FastAPI()

config = yaml.safe_load(open('config.yaml'))

default_data_treatment = NumericalStructure(True, config['default_file'])


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
        raise HTTPException(
            423,
            detail="Error : The database is currently being reindexed."
            " Please try again in a few seconds."
        )
    if nValues is None or nValues < 1:
        raise HTTPException(
            423,
            detail="Error : You must give a positive value"
            " for the request parameter."
        )

    values = default_data_treatment.get_Data(nValues)
    return JSONResponse(content={"values": values})


@app.post("/replaceDataset")
async def upload_file(file: UploadFile = File(...)) -> JSONResponse:

    if file is None:
        raise HTTPException(
            400,
            detail="Error : This route must receive a text document to run.")
    if file.content_type != "text/plain":
        raise HTTPException(
            400, detail="Error : The document type must be a plain text file.")

    if not default_data_treatment.database_has_loaded():
        raise HTTPException(
            423,
            detail="Error : The database is currently being reindexed."
            " Please try again in a few seconds."
        )

    default_data_treatment.process_data(file)
    return {
        "message":
            "Dataset uploaded successfully."
            " The server is currently treating the dataset..."
    }


@app.post("/uploadAndTreatFile/{nResponses}")
async def upload_and_treat_file(file: UploadFile = File(...),
                                nResponses: int = 1000) -> JSONResponse:
    if file is None:
        raise HTTPException(
            400,
            detail="Error : This route must receive a text document to run.")
    if file.content_type != "text/plain":
        raise HTTPException(
            400, detail="Error : The document type must be a plain text file.")

    analysis = NumericalStructure()
    values = analysis.get_Data(nResponses, file)
    return JSONResponse(content={"values": values})

if config['PROFILER']:
    @app.middleware('http')
    async def individualProfiler(request : Request,
                                call_next : Callable[[Request], Awaitable[Response]]) -> None:
        prof = Profiler(async_mode ='enabled')
        prof.start()
        result = await call_next(request)
        prof.stop()
        prof.print()
        return result
        
