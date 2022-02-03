from app.database import Base
from sqlalchemy import Column,Integer, String, Float

class Student(Base):
    __tablename__ = 'students'

    id = Column(Integer, primary_key=True, nullable=False)
    studentId = Column(String, nullable=False)
    exam = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)

class StudentTest(Base):
    __tablename__ = 'teststudent'

    id = Column(Integer, primary_key=True, nullable=False)
    studentId = Column(String, nullable=False)
    exam = Column(Integer, nullable=False)
    score = Column(Float, nullable=False)