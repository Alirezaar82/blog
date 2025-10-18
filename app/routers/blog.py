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

@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_one_post(post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@router.delete("/{post_id}", status_code=204)
def delete_post(user_id:int,post_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if user_id != post.author_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    db.delete(post)
    db.commit()
    return

@router.patch("/{post_id}", response_model=schemas.PostResponseUpdate)
def update_post(post_id: int, updated_post: schemas.PostUpdate, user_id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == post_id).first()
    if not post:
        raise HTTPException(status_code=404, detail="Post not found")
    
    if user_id != post.author_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this post")
    
    update_data = updated_post.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(post, key, value)
    
    db.commit()
    db.refresh(post)
    return post


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()
