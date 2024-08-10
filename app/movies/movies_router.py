from fastapi import APIRouter

router = APIRouter(prefix="/api/v1/movies", tags=['Movies'])

@router.get("/")
def say_hello():
    return {"message": "Hello from movies"}
