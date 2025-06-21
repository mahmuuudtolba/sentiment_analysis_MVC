from pydantic import BaseModel , Field , validator
from typing import Optional
from bson.objectid import ObjectId

class SentimentPrediction(BaseModel):
    id: Optional[ObjectId] = Field(None, alias="_id")
    sentiment_text: str= Field(... , min_length=1)
    result: str= Field(... , min_length=1)


    class Config:
        arbitrary_types_allowed = True

    


