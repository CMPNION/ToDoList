from fastapi import FastAPI, Depends, Request, status, Cookie, Form #framework, request, status code, cookie, form
from fastapi.responses import HTMLResponse, RedirectResponse #responses from html
from fastapi.templating import Jinja2Templates #to work in html
from sqlalchemy.orm import Session #whoisuser?
from passlib.context import CryptContext #password hashing
from . import models, database #models and database
from app.database import Base, engine #database and engine

app = FastAPI() #instance of application
templates = Jinja2Templates(directory="app/templates") #html (static)) files
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto") #crypt password
Base.metadata.create_all(bind=engine) #create tables

#getting session and db, if not exist create new, else create new trough yield
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

#define all user by session to give acess to todo
def get_user_by_session(db: Session, session_id: str):
    if session_id is None:
        return None
    return db.query(models.User).filter(models.User.id == session_id).first()

#getting new user data trough html form
@app.get("/register", response_class=HTMLResponse)
async def register(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

#register new user and set up session
@app.post("/register", response_class=HTMLResponse)
async def register_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):

    hashed_password = pwd_context.hash(password) #hash password
    db_user = models.User(username=username, password=hashed_password) #add user to db

    db.add(db_user)
    db.commit()
    db.refresh(db_user) #push and save user to db

    return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER) #redirect to login 

#setting up login page
@app.get("/login", response_class=HTMLResponse)
async def login(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

#login user and set up session
@app.post("/login", response_class=HTMLResponse)
async def login_post(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    db_user = db.query(models.User).filter(models.User.username == username).first()
    if db_user and pwd_context.verify(password, db_user.password): #check if user exist and session is valid
        response = RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)
        response.set_cookie(key="session_id", value=str(db_user.id))
        return response
    return templates.TemplateResponse(
        "login.html", {"request": request, "error": "Invalid credentials"} #login errors hatching
    )

#loging out and delete session
@app.get("/logout")
async def logout(request: Request):
    response = RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
    response.delete_cookie("session_id")
    return response

#logic for getting todo
@app.get("/todos", response_class=HTMLResponse)
async def read_todos(
    request: Request, db: Session = Depends(get_db), session_id: str = Cookie(None)
):
    if session_id is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    user = get_user_by_session(db, session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    todos = db.query(models.Todo).filter(models.Todo.owner_id == user.id).all()
    return templates.TemplateResponse(
        "todos.html", {"request": request, "todos": todos, "username": user.username}

        #AGAIN CHECK ALL FOR SESSION
    )

#logic for creating todo
@app.post("/todos", response_class=HTMLResponse)
async def create_todo(
    request: Request,
    task: str = Form(...),
    db: Session = Depends(get_db),
    session_id: str = Cookie(None),
):
    if session_id is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    user = get_user_by_session(db, session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    new_todo = models.Todo(task=task, owner_id=user.id)
    db.add(new_todo)
    db.commit()
    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)

    #SESSON AND DB AGAIN, THERE IS  JUST COPY PASTE

#Toggle todos
@app.post("/todos/{todo_id}/toggle", response_class=HTMLResponse)
async def toggle_todo(
    todo_id: int, db: Session = Depends(get_db), session_id: str = Cookie(None)
):
    if session_id is None:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)

    user = get_user_by_session(db, session_id)
    if not user:
        return RedirectResponse(url="/login", status_code=status.HTTP_303_SEE_OTHER)
#Same **** with session and db
    todo = (
        db.query(models.Todo)
        .filter(models.Todo.id == todo_id, models.Todo.owner_id == user.id)
        .first()
    )
    #Filtering todos
    if todo:
        todo.completed = not todo.completed
        db.commit()
        #db commit
    return RedirectResponse(url="/todos", status_code=status.HTTP_303_SEE_OTHER)

