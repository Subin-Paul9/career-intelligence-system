from fastapi import FastAPI

from app.config.settings import PROJECT_NAME
from app.config.settings import APP_VERSION

app = FastAPI(

    title=PROJECT_NAME,

    version=APP_VERSION,

    description="AI Powered Career Intelligence Platform"

)

@app.get("/")

def root():

    return {

        "message":"Backend Running Successfully"

    }


@app.get("/health")

def health():

    return {

        "status":"Healthy"

    }