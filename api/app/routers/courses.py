# app/routers/courses.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, AnyUrl, Field
from typing import List, Optional

router = APIRouter()

# ----------------------------
# Data models (mirror Node.js)
# ----------------------------
class CourseCreate(BaseModel):
    title: str = Field(..., min_length=1)
    description: str = Field(..., min_length=1)
    archived: Optional[bool] = False  # Node z.preprocess allowed string/bool


class CourseUpdate(BaseModel):
    archived: bool
    description: str = Field(..., min_length=1)
    liveLink: AnyUrl
    pictrue: AnyUrl  # kept same typo spelling as Node
    title: str = Field(..., min_length=1)


class CourseLiveLinkPatch(BaseModel):
    liveLink: AnyUrl


class CourseArchivePatch(BaseModel):
    archived: bool


class CourseNavListItem(BaseModel):
    id: int
    title: str


class CourseListItem(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    liveLink: Optional[AnyUrl] = None


class CourseDetail(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    liveLink: Optional[AnyUrl] = None
    archived: bool = False


# ---------------------------------
# Temporary in-memory "DB" (mock)
# ---------------------------------
_courses: List[dict] = []
_next_id = 1


def _find_course(course_id: int) -> dict:
    for c in _courses:
        if c["id"] == course_id:
            return c
    raise HTTPException(status_code=404, detail="Course not found")


# ----------------------------
# Routes (match Express router)
# ----------------------------

@router.post("", response_model=CourseNavListItem, status_code=201)
def create_course(payload: CourseCreate):
    """
    POST /courses
    Accepts: { title, description, archived? }
    Returns: { id, title }
    """
    global _next_id

    course = {
        "id": _next_id,
        "title": payload.title,
        "description": payload.description,
        "archived": bool(payload.archived),
        "liveLink": None,
        "pictrue": None,
    }
    _courses.append(course)
    _next_id += 1
    return {"id": course["id"], "title": course["title"]}


@router.get("", response_model=List[CourseListItem])
def get_my_courses():
    """
    GET /courses
    Returns non-archived courses with id, title, description, liveLink
    """
    return [
        {
            "id": c["id"],
            "title": c["title"],
            "description": c.get("description"),
            "liveLink": c.get("liveLink"),
        }
        for c in _courses
        if not c.get("archived", False)
    ]


@router.get("/all", response_model=List[CourseNavListItem])
def get_all_courses():
    """
    GET /courses/all
    Returns id + title for all courses
    """
    return [{"id": c["id"], "title": c["title"]} for c in _courses]


@router.get("/{course_id}", response_model=CourseDetail)
def get_course(course_id: int):
    """
    GET /courses/{id}
    """
    c = _find_course(course_id)
    return CourseDetail(**c)


@router.put("/{course_id}")
def update_course(course_id: int, payload: CourseUpdate):
    """
    PUT /courses/{id}
    """
    c = _find_course(course_id)
    c.update(
        {
            "archived": payload.archived,
            "description": payload.description,
            "liveLink": str(payload.liveLink),
            "pictrue": str(payload.pictrue),
            "title": payload.title,
        }
    )
    return {"status": "ok"}


@router.patch("/{course_id}/archieved", status_code=204)
def archive_course(course_id: int, payload: CourseArchivePatch):
    """
    PATCH /courses/{id}/archieved
    """
    c = _find_course(course_id)
    c["archived"] = payload.archived
    return  # 204 No Content


@router.patch("/{course_id}/live-link")
def update_live_link(course_id: int, payload: CourseLiveLinkPatch):
    """
    PATCH /courses/{id}/live-link
    """
    c = _find_course(course_id)
    c["liveLink"] = str(payload.liveLink)
    return {"status": "ok"}
