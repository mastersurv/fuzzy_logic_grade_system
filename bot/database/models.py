from datetime import datetime
from sqlalchemy import Column, Integer, Float, String, DateTime, ForeignKey, MetaData
from sqlalchemy.ext.declarative import declarative_base

# Метаданные для базы данных
metadata = MetaData()
Base = declarative_base(metadata=metadata)

class Student(Base):
    """Модель студента"""
    __tablename__ = "students"
    
    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    registration_date = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<Student id={self.id}, telegram_id={self.telegram_id}, username={self.username}>"

class GradeResult(Base):
    """Модель результата оценки"""
    __tablename__ = "grade_results"
    
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    quality = Column(Float, nullable=False)
    accuracy = Column(Float, nullable=False)
    deadline = Column(Float, nullable=False)
    numeric_grade = Column(Float, nullable=False)
    text_grade = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.now)
    
    def __repr__(self):
        return f"<GradeResult id={self.id}, student_id={self.student_id}, " \
               f"numeric_grade={self.numeric_grade}, text_grade={self.text_grade}>" 