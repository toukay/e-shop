from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import api_router
from contextlib import asynccontextmanager
import src.database as database


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.create_all()
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")
