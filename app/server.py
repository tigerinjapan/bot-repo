from threading import Thread

import uvicorn
from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Server is Online."}


@app.get("/test")
async def test():
    return {"message": "Server is on test."}


def start():
    local_host = "0.0.0.0"
    port_number = 8000
    # local_host =  "127.0.0.1"
    # port_number = 5000
    uvicorn.run(app, host=local_host, port=port_number)


def server_thread():
    t = Thread(target=start)
    t.start()


if __name__ == "__main__":
    server_thread()
