"""FastAPI application entry point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.state import app_state
from api.routers import config, params, solve

app = FastAPI(
    title="Supply Chain Optimizer API",
    description="Multi-objective optimization of a sustainable citrus supply chain.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():
    app_state.initialize()


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok"}


app.include_router(config.router)
app.include_router(params.router)
app.include_router(solve.router)
