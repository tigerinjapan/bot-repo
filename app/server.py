from threading import Thread

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Server is Online."}


def start():
    uvicorn.run(app, host="127.0.0.1", port=8080)


def server_thread():
    t = Thread(target=start)
    t.start()
