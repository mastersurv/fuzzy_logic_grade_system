import io
from typing import Tuple

import matplotlib.pyplot as plt

from fuzzy_logic import FuzzyGradeSystem
from bot.database.database import save_grade_result, get_or_create_student

# Создаем экземпляр системы нечеткой логики
fuzzy_system = FuzzyGradeSystem()

async def evaluate_student(quality: float, accuracy: float, deadline: float, student_name: str, telegram_id: int = None) -> Tuple[float, str]:
    """
    Оценивает знания студента и сохраняет результат в базу данных
    
    :param quality: качество выполнения работы (0-10)
    :param accuracy: точность полученного результата (0-10)
    :param deadline: соблюдение сроков (0-10)
    :param student_name: имя студента
    :param telegram_id: идентификатор пользователя в Telegram
    :return: (числовая_оценка, текстовая_оценка)
    """
    # Выполняем оценку
    numeric_grade, text_grade = fuzzy_system.evaluate(quality, accuracy, deadline)
    
    # Если telegram_id указан, сохраняем результат
    if telegram_id:
        try:
            # Получаем или создаем студента
            student = await get_or_create_student(
                telegram_id=telegram_id,
                username=student_name
            )
            
            # Сохраняем результат
            await save_grade_result(
                student_id=student.id,
                quality=quality,
                accuracy=accuracy,
                deadline=deadline,
                numeric_grade=numeric_grade,
                text_grade=text_grade
            )
        except Exception as e:
            print(f"Ошибка при сохранении результата в базу данных: {e}")
    
    return numeric_grade, text_grade

async def get_visualization() -> io.BytesIO:
    """
    Получает визуализацию функций принадлежности
    
    :return: BytesIO с изображением
    """
    # Визуализируем функции принадлежности
    fig = fuzzy_system.visualize()
    
    # Сохраняем в буфер
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    
    # Закрываем фигуру
    plt.close(fig)
    
    return buf

async def get_result_visualization(quality: float, accuracy: float, deadline: float) -> io.BytesIO:
    """
    Получает визуализацию результата оценки
    
    :param quality: качество выполнения работы (0-10)
    :param accuracy: точность полученного результата (0-10)
    :param deadline: соблюдение сроков (0-10)
    :return: BytesIO с изображением
    """
    # Визуализируем результат
    fig = fuzzy_system.visualize_result(quality, accuracy, deadline)
    
    # Сохраняем в буфер
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    
    # Закрываем фигуру
    plt.close(fig)
    
    return buf 