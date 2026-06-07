import asyncio

from fastapi import FastAPI, Request, Form
from fastapi.staticfiles import StaticFiles
from utils.templates import templates
import uvicorn
from bot import send_application
from model import Users

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/', name='home')
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/form', name='form')
def form(request: Request):
    return templates.TemplateResponse(name="forms.html", request=request)

@app.post('/form', name='submit_form')
async def submit_form(request: Request,
    phone: str = Form(...),
    name: str = Form(...),
    fullname: str = Form(...)):
    users = Users(name=name, fullname=fullname, phone=phone)
    
    if len(phone) < 18:
        return templates.TemplateResponse("forms.html", {
            "request": request,
            "error": "Неверный формат номера телефона",
            "phone": phone,
            "name": name,
            "fullname": fullname
        })

    asyncio.create_task(send_application(users.phone, users.name, users.fullname))

    return templates.TemplateResponse("success.html", {
        "request": request, 
        "phone": users.phone, 
        "name": users.name, 
        "fullname": users.fullname
    })

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
