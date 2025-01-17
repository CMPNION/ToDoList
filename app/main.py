from fastapi import FastAPI, Depends, Request, status, Cookie, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from . import models, database
from app.database import Base, engine


app = FastAPI()
templates = Jinja2Templates(directory="app/templates")
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
Base.metadata.create_all(bind=engine)
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_user_by_session(db: Session, session_id: str):
    if session_id is None:
        return None
    return db.query(models.User).filter(models.User.id == session_id).first()

@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register_post(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    hashed_password = pwd_context.hash(password)
    db_user = models.User(username=username, password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login", response_class=HTMLResponse)
async def login_post(request: Request, username: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user and pwd_context.verify(password, db_user.password):
        response = RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="session_id", value=str(db_user.id))
        return response
    return templates.TemplateResponse("login.html", {"request": request, "error": "Invalid credentials"})

@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("session_id")
    return response

@app.get("/todos", response_class=HTMLResponse)
async def read_todos(request: Request, db: Session = Depends(get_db), session_id: str = Cookie(None)):
    if session_id is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    user = get_user_by_session(db, session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    todos = db.query(models.Todo).filter(models.Todo.owner_id == user.id).all()
    return templates.TemplateResponse("todos.html", {"request": request, "todos": todos, "username": user.username})

@app.post("/todos", response_class=HTMLResponse)
async def create_todo(request: Request, task: str = Form(...), db: Session = Depends(get_db), session_id: str = Cookie(None)):
    if session_id is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    user = get_user_by_session(db, session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    new_todo = models.Todo(task=task, owner_id=user.id)
    db.add(new_todo)
    db.commit()
    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)

@app.post("/todos/{todo_id}/toggle", response_class=HTMLResponse)
async def toggle_todo(todo_id: int, db: Session = Depends(get_db), session_id: str = Cookie(None)):
    if session_id is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    user = get_user_by_session(db, session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    todo = db.query(models.Todo).filter(models.Todo.id == todo_id, models.Todo.owner_id == user.id).first()
    if todo:
        todo.completed = not todo.completed
        db.commit()
    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)
