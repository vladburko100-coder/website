import asyncio
from fastapi import Depends, FastAPI, Request, Form
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.sessions import SessionMiddleware
from utils.templates import templates
import uvicorn
from sqlalchemy.orm import Session
from bot import send_application
from database import engine, get_db, Base
from models import User
from auth import get_password_hash, verify_password

Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")


@app.get('/', name='home')
def home(request: Request):
    username = request.cookies.get("username")
    return templates.TemplateResponse("index.html", {"request": request, "username": username})


@app.get('/catalog', name='catalog')
def catalog(request: Request):
    username = request.cookies.get("username")
    return templates.TemplateResponse('catalog.html', {"request": request, "username": username})


@app.get('/application', name='application')
def application(request: Request):
    username = request.cookies.get("username")
    return templates.TemplateResponse("application.html", {
        "request": request,
        "username": username
    })


@app.get('/success', name='success_page')
def success_page(request: Request):
    username = request.cookies.get("username")

    user_data = request.session.pop("application_data", {})

    if not user_data:
        return RedirectResponse(url='/', status_code=303)

    return templates.TemplateResponse("success.html", {
        "request": request,
        "phone": user_data.get("phone"),
        "name": user_data.get("name"),
        "fullname": user_data.get("fullname"),
        "username": username,
    })


@app.post('/application', name='submit_form')
async def submit_form(request: Request, phone: str = Form(...), name: str = Form(...), fullname: str = Form(...)):
    username = request.cookies.get("username")    
    if len(phone) < 18:
        return templates.TemplateResponse("application.html", {
            "request": request,
            "error": "Неверный формат номера телефона",
            "phone": phone,
            "name": name,
            "fullname": fullname,
            "username": username,
        })
    else:
        await asyncio.create_task(send_application(phone, name, fullname))

        request.session["application_data"] = {
            "phone": phone,
            "name": name,
            "fullname": fullname
        }

        return RedirectResponse(url="/success", status_code=303)


@app.get('/register', name='register')
def register(request: Request):
    return templates.TemplateResponse(name="register.html", request=request)


@app.post('/register', name='register_user')
def register_user(request: Request, email: str = Form(...), username: str = Form(...), password: str = Form(...), confirm_password: str = Form(...), db: Session = Depends(get_db)):
    if password != confirm_password:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Пароли не совпадают",
            "username": username
        })

    new_user = db.query(User).filter(User.email == email).first()
    if new_user:
        return templates.TemplateResponse("register.html", {
            "request": request,
            "error": "Пользователь уже существует",
        })
    
    new_user = User(
        email=email,
        username=username,
        password=get_password_hash(password)
    )
    db.add(new_user)
    db.commit()

    return RedirectResponse(url="/login", status_code=303)


@app.get('/login')
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})


@app.post('/login', name='login_user')
def login_user(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):

    user = db.query(User).filter(User.email == email).first()

    if not user or not verify_password(password, user.password):
        return templates.TemplateResponse("login.html", {
            "request": request,
            "error": "Неверный email или пароль",
            "email": email
        })
    
    response = RedirectResponse(url='/', status_code=303)
    response.set_cookie(key="username", value=user.username)
    return response


@app.get("/logout")
def logout():
    response = RedirectResponse(url='/', status_code=303)
    response.delete_cookie("username")
    return response


if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
