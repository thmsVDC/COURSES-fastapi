from fastapi import APIRouter

auth_router = APIRouter(prefix="/auth", tags=["auth"])


@auth_router.get("/")
async def auth():
    """
    Default auth route
    """
    return {"message": "you accessed the auth route", "authenticated": False}
