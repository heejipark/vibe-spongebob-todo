from fastapi import FastAPI, Depends, HTTPException, status, Request, Form, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse, JSONResponse
from sqlalchemy.orm import Session
from datetime import timedelta, date, datetime
from sqlalchemy import and_, func
import models
import schemas
import crud
import auth
from database import engine, SessionLocal
from typing import Optional, List, Dict, Any
from copy import deepcopy

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Todo App")

# Mount static files and templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Cookie-based authentication dependency
async def get_current_user_from_cookie(
    access_token: Optional[str] = Cookie(None),
    db: Session = Depends(get_db)
):
    if not access_token:
        raise HTTPException(status_code=401, detail="Not authenticated")
    
    try:
        # Remove "Bearer " prefix if present
        if access_token.startswith("Bearer "):
            access_token = access_token[7:]
        
        payload = auth.jwt.decode(access_token, auth.SECRET_KEY, algorithms=[auth.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid token")
        
        user = crud.get_user_by_username(db, username)
        if user is None:
            raise HTTPException(status_code=401, detail="User not found")
        
        return user
    except auth.JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")

@app.get("/", response_class=HTMLResponse)
async def landing_page(request: Request):
    return templates.TemplateResponse("landing.html", {"request": request})

@app.get("/signup", response_class=HTMLResponse)
async def signup_page(request: Request):
    return templates.TemplateResponse("signup.html", {"request": request})

@app.post("/signup")
async def signup(
    request: Request,
    username: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    # Check if username already exists
    if crud.get_user_by_username(db, username):
        return templates.TemplateResponse(
            "signup.html", 
            {"request": request, "error": "Username already registered"}
        )
    
    # Check if email already exists
    if crud.get_user_by_email(db, email):
        return templates.TemplateResponse(
            "signup.html", 
            {"request": request, "error": "Email already registered"}
        )
    
    # Create user
    user_create = schemas.UserCreate(username=username, email=email, password=password)
    crud.create_user(db, user_create)
    
    return RedirectResponse(url="/login", status_code=303)

@app.get("/login", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
async def login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db)
):
    user = auth.authenticate_user(db, username, password)
    if not user:
        return RedirectResponse(url="/login-failed", status_code=303)
    
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    
    response = RedirectResponse(url="/todos", status_code=303)
    response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
    return response

@app.get("/login-failed", response_class=HTMLResponse)
async def login_failed(request: Request):
    return templates.TemplateResponse("login_failed.html", {"request": request})

@app.get("/todos", response_class=HTMLResponse)
async def todos_page(
    request: Request,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    icon_filter: str = '',
    current_user: models.User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    todos = crud.get_todos(db, current_user.id, sort_by=sort_by, sort_order=sort_order, icon=icon_filter)
    return templates.TemplateResponse(
        "todos.html", 
        {
            "request": request, 
            "todos": todos, 
            "user": current_user,
            "sort_by": sort_by,
            "sort_order": sort_order,
            "icon_filter": icon_filter,
            "now": date.today().isoformat()
        }
    )

@app.get("/calendar", response_class=HTMLResponse)
async def calendar_page(
    request: Request,
    current_user: models.User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    todos = crud.get_todos(db, current_user.id)
    # Convert to dicts using Pydantic schema and convert datetime fields to strings
    def serialize_todo(todo_dict):
        todo = deepcopy(todo_dict)
        for key in ['created_at', 'updated_at']:
            if todo.get(key) is not None:
                todo[key] = str(todo[key])
        # Convert PriorityEnum to string
        if todo.get('priority') is not None:
            todo['priority'] = str(todo['priority'])
        return todo
    todos_data = [serialize_todo(schemas.Todo.model_validate(todo).model_dump()) for todo in todos]
    return templates.TemplateResponse(
        "calendar.html", 
        {
            "request": request, 
            "todos": todos_data,  # Pass the serializable list
            "user": current_user
        }
    )

@app.get("/archive", response_class=HTMLResponse)
async def archive_page(
    request: Request,
    sort_by: str = "created_at",
    sort_order: str = "desc",
    current_user: models.User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    todos = crud.get_archived_todos(db, current_user.id, sort_by=sort_by, sort_order=sort_order)
    return templates.TemplateResponse(
        "archive.html", 
        {
            "request": request, 
            "todos": todos, 
            "user": current_user,
            "sort_by": sort_by,
            "sort_order": sort_order
        }
    )

@app.post("/archive/completed")
async def archive_completed(
    current_user: models.User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    archived_count = crud.archive_completed_todos(db, current_user.id)
    return RedirectResponse(url="/todos", status_code=303)

@app.post("/todos/{todo_id}/unarchive")
async def unarchive_todo(
    todo_id: int,
    current_user: models.User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    todo = crud.unarchive_todo(db, todo_id, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return RedirectResponse(url="/archive", status_code=303)

@app.post("/todos")
async def create_todo(
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    priority: Optional[str] = Form(None),
    deadline: Optional[str] = Form(None),
    icon: Optional[str] = Form(None),
    current_user: models.User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    todo_create = schemas.TodoCreate(
        title=title,
        description=description,
        priority=priority if priority else None,
        deadline=deadline if deadline else None,
        icon=icon if icon else None
    )
    crud.create_todo(db, todo_create, current_user.id)
    return RedirectResponse(url="/todos", status_code=303)

@app.post("/todos/{todo_id}/toggle")
async def toggle_todo(
    todo_id: int,
    current_user: models.User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    crud.toggle_todo_completion(db, todo_id, current_user.id)
    return RedirectResponse(url="/todos", status_code=303)

@app.post("/todos/{todo_id}/delete")
async def delete_todo(
    todo_id: int,
    current_user: models.User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    crud.delete_todo(db, todo_id, current_user.id)
    return RedirectResponse(url="/todos", status_code=303)

@app.get("/todos/{todo_id}/edit", response_class=HTMLResponse)
async def edit_todo_page(
    request: Request,
    todo_id: int,
    current_user: models.User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    todo = crud.get_todo(db, todo_id, current_user.id)
    if not todo:
        raise HTTPException(status_code=404, detail="Todo not found")
    return templates.TemplateResponse(
        "edit_todo.html", 
        {"request": request, "todo": todo, "now": date.today().isoformat()}
    )

@app.post("/todos/{todo_id}/edit")
async def edit_todo(
    todo_id: int,
    request: Request,
    title: str = Form(...),
    description: str = Form(""),
    priority: Optional[str] = Form(None),
    deadline: Optional[str] = Form(None),
    icon: Optional[str] = Form(None),
    current_user: models.User = Depends(get_current_user_from_cookie),
    db: Session = Depends(get_db)
):
    todo_update = schemas.TodoUpdate(
        title=title,
        description=description,
        priority=priority if priority else None,
        deadline=deadline if deadline else None,
        icon=icon if icon else None
    )
    crud.update_todo(db, todo_id, todo_update, current_user.id)
    return RedirectResponse(url="/todos", status_code=303)

@app.get("/logout")
async def logout():
    response = RedirectResponse(url="/", status_code=303)
    response.delete_cookie("access_token")
    return response

# ============================================================================
# ZAPIER API ENDPOINTS
# ============================================================================

def get_daily_summary_data(user_id: int) -> Dict[str, Any]:
    """Get summary data for a user's tasks due today and earlier"""
    db = SessionLocal()
    try:
        today = date.today()
        
        # Get all tasks due today or earlier (not archived)
        tasks = db.query(models.Todo).filter(
            and_(
                models.Todo.user_id == user_id,
                models.Todo.archived == False,
                models.Todo.deadline.isnot(None),
                func.date(models.Todo.deadline) <= today
            )
        ).all()
        
        # Calculate statistics
        total_tasks = len(tasks)
        completed_tasks = sum(1 for task in tasks if task.completed)
        completion_rate = round((completed_tasks / total_tasks * 100) if total_tasks > 0 else 0, 1)
        
        # Prepare task data
        task_data = []
        for task in tasks:
            task_dict = {
                'id': task.id,
                'title': task.title,
                'description': task.description or '',
                'completed': task.completed,
                'priority': task.priority.value if task.priority else None,
                'deadline': task.deadline,
                'icon': task.icon,
                'overdue': False
            }
            
            # Check if overdue
            if task.deadline and not task.completed:
                try:
                    deadline_date = datetime.strptime(task.deadline, '%Y-%m-%d').date()
                    if deadline_date < today:
                        task_dict['overdue'] = True
                except:
                    pass
            
            task_data.append(task_dict)
        
        return {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'completion_rate': completion_rate,
            'tasks': task_data
        }
        
    finally:
        db.close()

@app.get("/api/daily-summary/{user_id}", response_class=JSONResponse)
async def get_user_daily_summary(user_id: int):
    """Zapier endpoint: Get daily summary for a specific user"""
    try:
        summary_data = get_daily_summary_data(user_id)
        return {
            "success": True,
            "data": summary_data,
            "date": date.today().isoformat()
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )

@app.get("/api/daily-summary", response_class=JSONResponse)
async def get_all_users_daily_summary():
    """Zapier endpoint: Get daily summary for all users"""
    db = SessionLocal()
    try:
        # Get all users
        users = db.query(models.User).all()
        
        if not users:
            return {
                "success": True,
                "message": "No users found",
                "data": [],
                "date": date.today().isoformat()
            }
        
        # Get summary for each user
        all_summaries = []
        for user in users:
            try:
                summary_data = get_daily_summary_data(user.id)
                user_summary = {
                    "user_id": user.id,
                    "username": user.username,
                    "email": user.email,
                    "summary": summary_data
                }
                all_summaries.append(user_summary)
            except Exception as e:
                print(f"Error processing user {user.username}: {str(e)}")
        
        return {
            "success": True,
            "data": all_summaries,
            "date": date.today().isoformat(),
            "total_users": len(users)
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )
    finally:
        db.close()

@app.get("/api/users", response_class=JSONResponse)
async def get_all_users():
    """Zapier endpoint: Get all users with their emails"""
    db = SessionLocal()
    try:
        users = db.query(models.User).all()
        user_data = [
            {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "created_at": user.created_at.isoformat() if user.created_at else None
            }
            for user in users
        ]
        
        return {
            "success": True,
            "data": user_data,
            "total_users": len(users)
        }
        
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "error": str(e)
            }
        )
    finally:
        db.close()

@app.get("/api/zapier-daily-summary", response_class=JSONResponse)
async def zapier_daily_summary():
    db = SessionLocal()
    try:
        today = date.today()
        in_7_days = today + timedelta(days=7)
        users = db.query(models.User).all()
        result = []
        for user in users:
            # All todos for user
            todos = db.query(models.Todo).filter(models.Todo.user_id == user.id).all()
            total_todos = len(todos)
            completed_todos = sum(1 for t in todos if t.completed)
            completion_rate = round((completed_todos / total_todos * 100) if total_todos > 0 else 0, 1)

            # Tasks due today
            tasks_due_today = [
                {
                    'id': t.id,
                    'title': t.title,
                    'deadline': t.deadline,
                    'completed': t.completed
                }
                for t in todos
                if t.deadline == today.strftime('%Y-%m-%d')
            ]

            # Tasks due in next 7 days (excluding today)
            tasks_due_soon = [
                {
                    'id': t.id,
                    'title': t.title,
                    'deadline': t.deadline,
                    'completed': t.completed
                }
                for t in todos
                if t.deadline is not None and today < datetime.strptime(t.deadline, '%Y-%m-%d').date() <= in_7_days
            ]

            result.append({
                'user_id': user.id,
                'user_name': user.username,
                'email': user.email,
                'date': today.strftime('%Y-%m-%d'),
                'tasks_due_today': tasks_due_today,
                'tasks_due_soon': tasks_due_soon,
                'total_todos': total_todos,
                'completed_todos': completed_todos,
                'completion_rate': completion_rate
            })
        return {'success': True, 'data': result, 'date': today.strftime('%Y-%m-%d')}
    except Exception as e:
        return JSONResponse(status_code=500, content={'success': False, 'error': str(e)})
    finally:
        db.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
