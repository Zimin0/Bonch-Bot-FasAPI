from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse
from fastapi import FastAPI, Request, APIRouter, Depends
from starlette.exceptions import HTTPException as StarletteHTTPException
from fastapi.templating import Jinja2Templates
from fastapi.exception_handlers import http_exception_handler
from core.config import settings
from db.session import engine
from fastapi.middleware.cors import CORSMiddleware
from db.base import Base    

from apis.base import api_router

templates = Jinja2Templates(directory="templates/errors")

def create_tables():
    Base.metadata.create_all(bind=engine)

def include_router(app):   
	app.include_router(api_router)

def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    create_tables()
    include_router(app)
    return app

app = start_application()

# origins = [
#     "http://localhost:8080",
#     "http://127.0.0.1:8080",
# ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# @app.exception_handler(StarletteHTTPException)
# async def custom_http_exception_handler(request: Request, exc: StarletteHTTPException):
#     if exc.status_code == 401:
#         return templates.TemplateResponse("401.html", {"request": request}, status_code=exc.status_code)
#     return await http_exception_handler(request, exc)

@app.get('/')
def check_bot():
    html_content = "<h2>Hello, I'm pc booking bot!</h2>"
    return HTMLResponse(content=html_content)