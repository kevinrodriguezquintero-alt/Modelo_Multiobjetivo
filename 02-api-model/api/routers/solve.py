from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from api.state import app_state
from solvers.lgp import run_lgp
from solvers.er import run_er

router = APIRouter(prefix="/solve", tags=["solve"])


@router.post("/lgp")
def solve_lgp():
    """Run Lexicographic Goal Programming and return structured JSON results."""
    try:
        result = run_lgp(
            params_obj=app_state.get_params_object(),
            solver_name=app_state.solver_name,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result


class ERRequest(BaseModel):
    steps: int = Field(default=5, ge=2, le=50, description="Number of epsilon iterations")


@router.post("/er")
def solve_er(body: ERRequest = ERRequest()):
    """Run Epsilon-Constraint Method and return Pareto frontier JSON."""
    try:
        result = run_er(
            params_obj=app_state.get_params_object(),
            solver_name=app_state.solver_name,
            steps=body.steps,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    return result
