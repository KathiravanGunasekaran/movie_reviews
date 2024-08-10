from pydantic import BaseModel
from datetime import datetime
from app.users.schemas import UserResponse


class Movie(BaseModel):
    title: str
    review: str
    rating: int | None


class MovieResponse(Movie):
    id: int
    created_at: datetime
    owner_id: int
    owner: UserResponse

    class Config:
        form_attributes = True
