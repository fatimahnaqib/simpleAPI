from fastapi import Depends,Request,HTTPException, Depends, APIRouter
import app.models as models
from app.database import engine,SessionLocal, get_db
from sqlalchemy.orm import Session
from app.calc_avg import calc_average_score
from fastapi.templating import Jinja2Templates

router = APIRouter(
    prefix="/students",
    tags=['Students']
)

templates = Jinja2Templates(directory="templates")


@router.get("/")
async def get_students(request:Request, db:Session = Depends(get_db)):

    students = query_all_students(models.Student,db)
    return templates.TemplateResponse("students.html", {"request": request,"students": students})

@router.get("/{studentName}")
async def get_student(request: Request,studentName:str, db:Session = Depends(get_db)):
    student_scores = query_specific_student(models.Student,studentName,db)
    avg_score = calc_average_score(student_scores)
    
    return templates.TemplateResponse("student_scores.html", {"request": request,"studentName": studentName,"studentScores":student_scores,"avgScore":avg_score})

def query_specific_student(table_name,studentName,db):
    return db.query(table_name).filter(table_name.studentId == studentName).all()

def query_all_students(table_name,db):
    return db.query(table_name.studentId).group_by(table_name.studentId).all()


