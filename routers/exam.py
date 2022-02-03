from fastapi import Depends,Request,HTTPException, status,Depends, APIRouter
from sqlalchemy import asc
import app.models as models
from app.database import engine,SessionLocal, get_db
from sqlalchemy.orm import Session
from app.calc_avg import calc_average_score
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/exams",
    tags=['Exams']
)

templates = Jinja2Templates(directory="templates")

@router.get("/")
async def get_exams(request: Request, db:Session = Depends(get_db)):

    exams = query_exams(models.Student,db)
    
    return templates.TemplateResponse("exam.html", {"request": request,"exams":exams})

@router.get("/{examId}")
async def get_exam_id(request: Request,examId:int, db:Session = Depends(get_db)):
    students = query_all_exam_id(models.Student,db,examId)
    student = query_exam_id(models.Student,db,examId)

    if not student:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Exam with id: {examId} was not found")
    
    avg_score = calc_average_score(students)
    
    return templates.TemplateResponse("exam_scores.html", {"request": request,"students":students, "avgScore":avg_score})

def query_exams(table_name,db):
    return db.query(table_name.exam).group_by((table_name.exam)).all()

def query_all_exam_id(table_name,db,examId):
    return db.query(table_name).filter(table_name.exam == examId).all()

def query_exam_id(table_name,db,examId):
    return db.query(table_name).filter(table_name.exam == examId).first()

