"""Minimal demo web service used to exercise the Argo CD GitOps pipeline."""
import os
from contextlib import asynccontextmanager

from fastapi import FastAPI, Response

APP_NAME = os.getenv("APP_NAME", "demo-app")
VERSION = os.getenv("APP_VERSION", "0.0.0-dev")
ENVIRONMENT = os.getenv("APP_ENV", "local")
GIT_SHA = os.getenv("GIT_SHA", "unknown")
BUILD_TIME = os.getenv("BUILD_TIME", "unknown")

_ready = True  # flipped to False on shutdown so rollouts drain cleanly


@asynccontextmanager
async def lifespan(_: FastAPI):
    global _ready
    _ready = True
    yield
    _ready = False


app = FastAPI(title=APP_NAME, version=VERSION, lifespan=lifespan)


@app.get("/")
def root() -> dict:
    return {"name": APP_NAME, "version": VERSION, "environment": ENVIRONMENT, "status": "ok"}


@app.get("/healthz")
def healthz() -> dict:
    return {"status": "healthy"}


@app.get("/readyz")
def readyz(response: Response) -> dict:
    if not _ready:
        response.status_code = 503
        return {"status": "not-ready"}
    return {"status": "ready"}


@app.get("/version")
def version() -> dict:
    return {"version": VERSION, "git_sha": GIT_SHA, "build_time": BUILD_TIME}
