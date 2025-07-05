from fastapi import FastAPI, Depends, HTTPException, status, Request, Form, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import timedelta, date
import models
import schemas
import crud
import auth
from database import engine, SessionLocal
from typing import Optional
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
