from fastapi import APIRouter
from services.courses_service import get_all_courses

router = APIRouter()

@router.get("/all")
def all_courses():
    return get_all_courses()
