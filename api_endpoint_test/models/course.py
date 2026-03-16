from pydantic import BaseModel
from typing import Optional


class CourseBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None


class CourseCreate(CourseBase):
    pass


class CourseUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None


class CourseResponse(CourseBase):
    id: int
    is_active: bool
