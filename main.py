from contextlib import asynccontextmanager

import uvicorn

from fastapi import FastAPI
from starlette.responses import FileResponse, StreamingResponse
from starlette.staticfiles import StaticFiles

from backend.database import init_db, get_results, get_csv_results
from backend.routes.test_router import router as test_router
from backend.routes.admin_router import router as admin_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="static"), name="static")


app.include_router(test_router)
app.include_router(admin_router)


@app.get("/")
async def get_index_page():
    return FileResponse("static/pages/index.html")


@app.get("/finish")
async def get_finish_page():
    return FileResponse("static/pages/finish.html")
