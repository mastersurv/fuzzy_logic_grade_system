from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql import select, insert, update, delete

from bot.config import ASYNC_DATABASE_URL
from bot.database.models import Base, Student, GradeResult

# Создаем движок базы данных
engine = create_async_engine(ASYNC_DATABASE_URL, echo=False)

# Создаем фабрику сессий
async_session = sessionmaker(
    engine, expire_on_commit=False, class_=AsyncSession
)

async def init_models():
    """Инициализация моделей"""
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

async def get_or_create_student(telegram_id, username=None, first_name=None, last_name=None):
    """Получение или создание студента по telegram_id"""
    async with async_session() as session:
        # Ищем студента
        query = select(Student).where(Student.telegram_id == telegram_id)
        result = await session.execute(query)
        student = result.scalar_one_or_none()
        
        if not student:
            # Создаем нового студента
            student = Student(
                telegram_id=telegram_id,
                username=username,
                first_name=first_name,
                last_name=last_name
            )
            session.add(student)
            await session.commit()
            await session.refresh(student)
            
        return student

async def save_grade_result(student_id, quality, accuracy, deadline, numeric_grade, text_grade):
    """Сохранение результата оценки в базу данных"""
    async with async_session() as session:
        grade_result = GradeResult(
            student_id=student_id,
            quality=quality,
            accuracy=accuracy,
            deadline=deadline,
            numeric_grade=numeric_grade,
            text_grade=text_grade
        )
        session.add(grade_result)
        await session.commit()
        await session.refresh(grade_result)
        return grade_result

async def get_student_grades(student_id, limit=10):
    """Получение истории оценок студента"""
    async with async_session() as session:
        query = (
            select(GradeResult)
            .where(GradeResult.student_id == student_id)
            .order_by(GradeResult.created_at.desc())
            .limit(limit)
        )
        result = await session.execute(query)
        return result.scalars().all() 