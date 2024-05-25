from fastapi import FastAPI, Response
from fastapi.responses import HTMLResponse

from core.config import settings
from db.session import engine
from db.base import Base    

from apis.base import api_router

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

@app.get('/')
def check_bot():
    html_content = "<h2>Hello, I'm pc booking bot!</h2>"
    return HTMLResponse(content=html_content)