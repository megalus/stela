from fastapi import FastAPI

from stela import env
from stela.utils import read_env

app = FastAPI()


@app.get("/")
async def root():
    _ = read_env()
    return {
        "message": "Hello World",
        "environment": env.current_environment,
        "secret": env.MY_SECRET,
    }
