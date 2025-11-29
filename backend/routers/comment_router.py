from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Comment, Post, User
from schemas import CommentCreate, CommentResponse
from auth import get_current_user

router = APIRouter(prefix="/posts/{post_id}/comments", tags=["评论"])


@router.post("/", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    comment_data: CommentCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """创建评论"""
    # 检查帖子是否存在
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在"
        )

    new_comment = Comment(
        content=comment_data.content,
        author_id=current_user.id,
        post_id=post_id
    )
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment


@router.get("/", response_model=List[CommentResponse])
def get_comments(post_id: int, db: Session = Depends(get_db)):
    """获取帖子的所有评论"""
    post = db.query(Post).filter(Post.id == post_id).first()
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="帖子不存在"
        )

    comments = db.query(Comment).filter(Comment.post_id == post_id).order_by(Comment.created_at).all()
    return comments


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(
    post_id: int,
    comment_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """删除评论"""
    comment = db.query(Comment).filter(
        Comment.id == comment_id,
        Comment.post_id == post_id
    ).first()

    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="评论不存在"
        )
    if comment.author_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无权删除此评论"
        )

    db.delete(comment)
    db.commit()
