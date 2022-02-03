import unittest
from app.calc_avg import calc_average_score
import app.models as models
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import Base
from main.main import app
from routers.exam import query_exam_id, query_exams
from routers.student import query_all_students, query_specific_student

class ApplicationTest(unittest.TestCase):

    def setUp(self):

        SQLALCHEMY_DATABASE_URL = "postgresql://postgres:root@localhost/teststudents"

        self.engine = create_engine(
            SQLALCHEMY_DATABASE_URL
        )
        TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        Base.metadata.create_all(bind=self.engine)
        self.db = TestingSessionLocal()
        students = [
            {'studentId': 'fatimah98', 'exam': 1001, 'score': 2.0},
            {'studentId': 'fatimah98', 'exam': 1002, 'score': 3.0},
            {'studentId': 'jack12', 'exam': 1003, 'score': 9.0},
            {'studentId': 'jack12', 'exam': 1004, 'score': 8.0},
            {'studentId': 'dannica', 'exam': 1005, 'score': 7.0}
        ]

        for student in students:
            
            row = models.StudentTest(studentId=student.get('studentId'), exam=student.get('exam') , score=student.get('score'))
            self.db.add(row)
            self.db.commit()

    def tearDown(self):
        # delete data from table
        student_table = self.db.query(models.StudentTest)
        student_table.delete(synchronize_session=False)
        self.db.commit()

    def test_get_all_students(self):
        students = query_all_students(models.StudentTest,self.db)
        student_names = []
        for student in students:
            student_names.append(student[0])

        assert "fatimah98" in student_names
        assert "jack12" in student_names
        assert "dannica" in student_names
    
    def test_get_all_exams(self):
        exams = query_exams(models.StudentTest,self.db)
        all_exams = []
        for exam in exams:
            all_exams.append(exam[0])
        
        assert 1001 in all_exams
        assert 1002 in all_exams
        assert 1003 in all_exams
        assert 1004 in all_exams
        assert 1005 in all_exams
    
    def test_get_exam_id(self):
        exam = query_exam_id(models.StudentTest,self.db,1001)
        if exam:
            assert True
        else:
            assert False
        
    def test_average_score(self):
        student_scores = query_specific_student(models.StudentTest,'fatimah98',self.db)
        self.assertEqual(calc_average_score(student_scores), 2.5)