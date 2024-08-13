from fastapi import APIRouter, Depends, status, HTTPException, Response
from app.auth import Oauth2
from sqlalchemy.orm import Session
from app.database import get_db
from app.movies import models, schemas
from typing import List


router = APIRouter(prefix="/api/v1/movies", tags=['Movies'])


@router.get("/", response_model=List[schemas.MovieResponse])
def get_movies(db: Session = Depends(get_db), user=Depends(Oauth2.get_current_user)):
    movies = db.query(models.Movie).filter(models.Movie.owner_id == user).all()
    return movies


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.MovieResponse)
def post_movies(movie_review: schemas.Movie, db: Session = Depends(get_db), user=Depends(Oauth2.get_current_user)):
    new_movie_review = models.Movie(owner_id=user, **movie_review.model_dump())
    db.add(new_movie_review)
    db.commit()
    db.refresh(new_movie_review)
    return new_movie_review


@router.get("/{movie_review_id}", response_model=schemas.MovieResponse)
def get_movie_review(movie_review_id: int, db: Session = Depends(get_db), user=Depends(Oauth2.get_current_user)):
    movie_review = (db.query(models.Movie).filter(models.Movie.owner_id == user, models.Movie.id ==
                                                  movie_review_id).first())
    if movie_review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie review with {movie_review_id} "
                                                                          f"not found")
    return movie_review


@router.put("/{movie_review_id}")
def update_movie_review(movie_review_id: int, updated_review: schemas.Movie, db: Session = Depends(get_db),
                        user=Depends(Oauth2.get_current_user)):
    movie_review_query = db.query(models.Movie).filter(models.Movie.id == movie_review_id)
    movie_review = movie_review_query.first()
    if movie_review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie review with id :{movie_review_id} "
                                                                          f"not found")
    if movie_review.owner_id != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to do any actions")
    movie_review_query.update(updated_review.model_dump(), synchronize_session=False)
    db.commit()
    return movie_review_query.first()


@router.delete("/{movie_review_id}")
def delete_movie_review(movie_review_id: int, db: Session = Depends(get_db), user=Depends(Oauth2.get_current_user)):
    movie_review_query = db.query(models.Movie).filter(models.Movie.id == movie_review_id)
    movie_review = movie_review_query.first()
    if movie_review is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Movie review with id :{movie_review_id} "
                                                                          f"not found")
    if movie_review.owner_id != user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User not authorized to do any actions")
    movie_review_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
