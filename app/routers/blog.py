# app/routers/blog.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import models, schemas
from app.database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.post("/", response_model=schemas.PostResponse)
def create_post(post: schemas.PostCreate, author_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == author_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    new_post = models.Post(title=post.title, content=post.content, author_id=author_id)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()
