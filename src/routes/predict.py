from fastapi import FastAPI , APIRouter , Depends , UploadFile, status 
from fastapi.responses import JSONResponse
from models import OpenAISentiemtModel , ModelEnum
import os
import logging
from pydantic import BaseModel


logger = logging.getLogger("uvicorn.error")
perdict_router = APIRouter(
    prefix = "/api/v1/predict",
    tags=['api_v1' , "predict"]
)

## going to refactor this

class TextRequest(BaseModel):
    text: str

@perdict_router.post("/text/")
async def analyze_sentiment(request: TextRequest):

    isvalid , results = OpenAISentiemtModel().predict_sentiment(text=request.text)
    if not isvalid :
        return JSONResponse(
                status_code= status.HTTP_400_BAD_REQUEST,
                content={
                    "signal" : ModelEnum.OPENAI_ERROR.value
                } 

            )
    else:
        return {"text" : request.text , 
                "results" : results}
