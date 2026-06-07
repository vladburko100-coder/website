import asyncio

from fastapi import FastAPI, Request, Form
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from utils.templates import templates
import uvicorn
from bot import send_application

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get('/', name='home')
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get('/form', name='form')
def form(request: Request):
    return templates.TemplateResponse(name="forms.html", request=request)

@app.post('/form', name='submit_form')
async def submit_form(request: Request, phone: str = Form(...), name: str = Form(...), fullname: str = Form(..., max_length=19)):
    asyncio.create_task(send_application(phone, name, fullname))
    return templates.TemplateResponse("success.html", {
        "request": request, 
        "phone": phone, 
        "name": name, 
        "fullname": fullname
    })

if __name__ == "__main__":
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
