from fastapi import APIRouter
from api.state import app_state

router = APIRouter(prefix="/params", tags=["params"])


@router.get("")
def get_params():
    return app_state.get_serialized_params()


@router.put("")
def update_params(body: dict):
    """Partial update. Accepts same format as GET /params (subset of keys)."""
    app_state.update_params(body)
    return app_state.get_serialized_params()


@router.post("/reset")
def reset_params():
    """Restore all parameters to defaults from data/params.py."""
    app_state.reset_params()
    return app_state.get_serialized_params()
