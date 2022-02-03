from fastapi import FastAPI,Request
import json
from sseclient import SSEClient
from celery import Celery
import app.models as models
from app.database import engine, SessionLocal
from routers import exam,student
from fastapi.templating import Jinja2Templates

app = FastAPI()

templates = Jinja2Templates(directory="templates")
models.Base.metadata.create_all(bind=engine)

"""Create Celery"""
CELERY_RESULT_BACKEND = 'db+postgresql://postgres:root@localhost/students'
CELERY_BROKER_URL = 'sqla+postgresql://postgres:root@localhost/students'

celery = Celery(__name__)
celery.conf.broker_url = CELERY_BROKER_URL
celery.conf.result_backend = CELERY_RESULT_BACKEND

"""Include routes"""
app.include_router(exam.router)
app.include_router(student.router)

"""Retrieve content server url and save to sqlachemy postgress database
"""
@celery.task(name="getting_live_test")
def retrive_live_score():
    
    """Retrieve streaming response using the requests library
    """
    def with_requests(url):
        import requests
        return requests.get(url, stream=True,headers = {'Accept': 'text/event-stream'})

    
    content_server_url = "http://live-test-scores.herokuapp.com/scores"
    response = with_requests(content_server_url)
    client = SSEClient(response)
    db= SessionLocal()

    for event in client.events():
        if event.event == 'score':
            row = json.loads(event.data)
            student = models.Student(studentId=row.get('studentId'), exam=row.get('exam') , score=row.get('score'))
            db.add(student)
            db.commit()


"""
Function that runs before the application starts
"""
@app.on_event("startup")
async def startup_event(): 
    retrive_live_score.delay()

@app.get('/')
def home_page():
    return "Welcome to the SIMPLE API Design"