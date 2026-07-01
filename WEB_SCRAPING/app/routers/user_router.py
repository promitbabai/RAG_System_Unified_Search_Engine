from fastapi import APIRouter
from app.services.user_service import get_all_users


router = APIRouter(
    prefix="/users",        # base URL path
    tags=["Users"]          # for Swagger docs
)


@router.get("/")
def fetch_users():
    return get_all_users()