from fastapi import FastAPI , APIRouter , Depends , UploadFile, status ,Request
from fastapi.responses import JSONResponse
from models import OpenAISentiemtModel , ModelEnum
from models import SentimentPrediction
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

@perdict_router.post("/sentiment/")
async def analyze_sentiment( request : Request , text_request: TextRequest):
    openai_sentiment_model = OpenAISentiemtModel(
        db_client=request.app.db_client
    )
    isvalid , results = openai_sentiment_model.predict_sentiment(text=text_request.text)
    if not isvalid :
        return JSONResponse(
                status_code= status.HTTP_400_BAD_REQUEST,
                content={
                    "signal" : ModelEnum.OPENAI_ERROR.value
                } 

            )
    
    print(f"Here are the results : {results}")


    response = await openai_sentiment_model.insert_prediction(
            SentimentPrediction(
                sentiment_text= text_request.text , 
                result=results
            )
    )




    return {
            "text" : text_request.text , 
            "results" : results , 
            "response" : response
            }
