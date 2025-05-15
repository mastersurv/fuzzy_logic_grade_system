from aiogram.fsm.state import StatesGroup, State

class GradeStudent(StatesGroup):
    """Группа состояний для процесса оценки студента"""
    waiting_for_name = State()
    waiting_for_quality = State()
    waiting_for_accuracy = State()
    waiting_for_deadline = State()

class ViewHistory(StatesGroup):
    """Группа состояний для просмотра истории"""
    viewing = State()
    
class Visualization(StatesGroup):
    """Группа состояний для визуализации функций принадлежности"""
    waiting_for_choice = State() 