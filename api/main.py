import sys
import os
from pathlib import Path
from fastapi import FastAPI, HTTPException, Query
from mangum import Mangum 
from contextlib import asynccontextmanager
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

sys.path.append(str(Path(__file__).resolve().parent.parent))

from database import database
from api.endpoints import professor, department, rating

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=["*"],
    allow_headers=["*"],
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage startup and shutdown events using a context manager."""
    database.initialize_connection_pool()
    yield  # Application runs while execution is suspended here
    database.close_pool()

app = FastAPI(lifespan=lifespan)

@app.get("/")
def root():
    return {"message": "Welcome to the Rate my Professor API"}

app.include_router(professor.router)
app.include_router(department.router)
app.include_router(rating.router)

# The magic that allows the integration with AWS Lambda
handler = Mangum(app)

# if __name__ == "__main__":
#     uvicorn.run(app, port=8000)