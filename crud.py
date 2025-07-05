from sqlalchemy.orm import Session
from sqlalchemy import desc, asc, or_
import models
import schemas
import auth
from typing import List, Optional

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_todos(db: Session, user_id: int, skip: int = 0, limit: int = 100, 
              sort_by: str = "created_at", sort_order: str = "desc", icon: str = None):
    query = db.query(models.Todo).filter(models.Todo.user_id == user_id)
    if icon:
        if icon == '📝':
            query = query.filter(or_(models.Todo.icon == None, models.Todo.icon == '', models.Todo.icon == '📝'))
        else:
            query = query.filter(models.Todo.icon == icon)
    
    # Apply sorting
    if sort_by == "created_at":
        if sort_order == "desc":
            query = query.order_by(desc(models.Todo.created_at))
        else:
            query = query.order_by(asc(models.Todo.created_at))
    elif sort_by == "title":
        if sort_order == "desc":
            query = query.order_by(desc(models.Todo.title))
        else:
            query = query.order_by(asc(models.Todo.title))
    elif sort_by == "priority":
        if sort_order == "desc":
            query = query.order_by(desc(models.Todo.priority))
        else:
            query = query.order_by(asc(models.Todo.priority))
    elif sort_by == "deadline":
        if sort_order == "desc":
            query = query.order_by(desc(models.Todo.deadline))
        else:
            query = query.order_by(asc(models.Todo.deadline))
    
    return query.offset(skip).limit(limit).all()

def get_todo(db: Session, todo_id: int, user_id: int):
    return db.query(models.Todo).filter(
        models.Todo.id == todo_id, 
        models.Todo.user_id == user_id
    ).first()

def create_todo(db: Session, todo: schemas.TodoCreate, user_id: int):
    db_todo = models.Todo(**todo.model_dump(), user_id=user_id)
    db.add(db_todo)
    db.commit()
    db.refresh(db_todo)
    
    # Sync with Google Calendar if deadline is set
    if db_todo.deadline:
        try:
            from google_calendar import calendar_manager
            success, result = calendar_manager.create_event(db_todo)
            if success:
                db_todo.google_calendar_id = result
                db.commit()
                db.refresh(db_todo)
        except Exception as e:
            # Log error but don't fail the todo creation
            print(f"Google Calendar sync failed: {e}")
    
    return db_todo

def update_todo(db: Session, todo_id: int, todo_update: schemas.TodoUpdate, user_id: int):
    db_todo = get_todo(db, todo_id, user_id)
    if not db_todo:
        return None
    
    update_data = todo_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_todo, field, value)
    
    db.commit()
    db.refresh(db_todo)
    
    # Sync with Google Calendar if deadline is set
    if db_todo.deadline:
        try:
            from google_calendar import calendar_manager
            success, result = calendar_manager.update_event(db_todo)
            if success:
                db_todo.google_calendar_id = result
                db.commit()
                db.refresh(db_todo)
        except Exception as e:
            print(f"Google Calendar sync failed: {e}")
    
    return db_todo

def delete_todo(db: Session, todo_id: int, user_id: int):
    db_todo = get_todo(db, todo_id, user_id)
    if not db_todo:
        return False
    
    # Delete from Google Calendar if synced
    if db_todo.google_calendar_id:
        try:
            from google_calendar import calendar_manager
            calendar_manager.delete_event(db_todo.google_calendar_id)
        except Exception as e:
            print(f"Google Calendar deletion failed: {e}")
    
    db.delete(db_todo)
    db.commit()
    return True

def toggle_todo_completion(db: Session, todo_id: int, user_id: int):
    db_todo = get_todo(db, todo_id, user_id)
    if not db_todo:
        return None
    
    db_todo.completed = not db_todo.completed
    db.commit()
    db.refresh(db_todo)
    return db_todo
