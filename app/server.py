# 説明：サーバ処理

from threading import Thread

import constants as const
import function as func
import uvicorn
from fastapi import FastAPI
from fastapi.responses import FileResponse

# fast api
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "[root] Server is online."}


@app.get("/test")
async def test():
    return {"message": "[test] Server is on test."}


@app.get("/img/{file_name}")
async def img(file_name: str):
    image_path = (
        f"{const.STR_OUTPUT}/{const.STR_IMG}/{file_name}.{const.FILE_TYPE_JPEG}"
    )
    return FileResponse(image_path)


def start():
    if func.check_local_ip():
        host = const.IP_LOCAL_HOST
        port = const.PORT_NUM

    else:
        host = const.IP_DEFAULT
        port = const.PORT_DEFAULT

    uvicorn.run(app, host=host, port=port)


def server_thread():
    t = Thread(target=start)
    t.start()


if __name__ == const.MAIN_FUNCTION:
    server_thread(app)
