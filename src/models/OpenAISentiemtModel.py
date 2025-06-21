from openai import OpenAI
from helper import Settings
from .enums.ModelEnum import ModelEnum
from .enums.DataBaseEnum import DataBaseEnum
from .BaseDataModel import BaseDataModel
import re
from .db_schemes.SentimentPrediction import SentimentPrediction
class OpenAISentiemtModel(BaseDataModel):

    def __init__(self , db_client:object):
        super().__init__(db_client=db_client)
        self.collection = self.db_client[DataBaseEnum.COLLECTION_SENTIMENT.value]


    
    def load_model(self):


        client = OpenAI(
            base_url= ModelEnum.MODEL_ENDPOINT.value , 
            api_key= Settings().GITHUB_TOKEN
        )

        return client

    def set_system_message(self , system_message : str):
        self.system_message = system_message

    def predict_sentiment(self , text:str):



        if not text or not text.strip():
            return ModelEnum.NAUTRAL.value
        
        # load client
        client = self.load_model()
        

        try :
            prompt = f"Analyze the sentiment of the following text and classify it as 'Positive', 'Negative', or 'Neutral'. Only respond with the sentiment word.\n\nText: \"{text}\""
            
            
            chat_completion = client.chat.completions.create(
                model = ModelEnum.MODEL_NAME.value ,
                messages =[
                    {"role" : "system" , "content" : ModelEnum.SYSTEM_PROMPT.value},
                    {"role" : "user" , "content" : prompt}
                ],
                
   
                max_tokens= ModelEnum.MAX_TOKENS.value  ,
                temperature= ModelEnum.TEMPERATURE.value

            )

            # Extract the sentiment from the response
            # OpenAI's response is usually in chat_completion.choices[0].message.content
            raw_sentiment = chat_completion.choices[0].message.content.strip()


            # Optional: Clean up and validate the sentiment to ensure it's one of our expected categories
            if re.search(r'positive', raw_sentiment, re.IGNORECASE):
                return True , "Positive" , 
            elif re.search(r'negative', raw_sentiment, re.IGNORECASE):
                return True ,  "Negative"
            elif re.search(r'neutral', raw_sentiment, re.IGNORECASE):
                return True ,  "Neutral"
            else:
                print(ModelEnum.WARNING.value + {raw_sentiment} + ModelEnum.NAUTRAL.value)
                return True ,  "Neutral" # Default or handle as unknown


        
        except Exception as e:
            print(e)
            return False , f"Error: Could not get sentiment ({e})"
        

    async def insert_prediction(self, sentiment_prediction: SentimentPrediction):
        print("Collection type:", type(self.collection))  # Debug
        result = await self.collection.insert_one(sentiment_prediction.dict())
        if result.inserted_id:
            return {"message": "Prediction inserted successfully", "id": str(result.inserted_id)}
        else:
            return {"message": "Insertion failed"}

        
        
        


    

    