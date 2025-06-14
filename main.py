from fastapi import FastAPI
from routes import base , predict



app = FastAPI()
app.include_router(base.base_router)
app.include_router(predict.perdict_router)
