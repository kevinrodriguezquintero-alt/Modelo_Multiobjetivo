from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from api.state import app_state
from config import SOLVERS

router = APIRouter(prefix="/config", tags=["config"])


class SolverUpdate(BaseModel):
    solver: str


@router.get("/solver")
def get_solver_config():
    return {
        "active":  app_state.solver_name,
        "options": list(SOLVERS.keys()),
    }


@router.put("/solver")
def set_solver_config(body: SolverUpdate):
    try:
        app_state.set_solver(body.solver)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"active": app_state.solver_name, "options": list(SOLVERS.keys())}
