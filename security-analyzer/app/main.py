from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import analyze
from app.services.ai_worker import start_worker
from contextlib import asynccontextmanager


# lifespan runs code when the server starts (before yield)
# and when it stops (after yield). It's the right place to start
# background resources like the worker.
@asynccontextmanager
async def lifespan(app: FastAPI):
    start_worker()
    yield


app = FastAPI(
    title="Security Analyzer",
    description="Security log analysis microservice",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000",],  # React's dev server URL
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(analyze.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001, reload=True)