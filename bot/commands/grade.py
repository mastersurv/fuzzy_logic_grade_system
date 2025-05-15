from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.handlers.states import GradeStudent
from bot.keyboards.grade_input import get_rating_keyboard, get_cancel_keyboard

router = Router()

@router.message(Command("grade"))
@router.message(F.text == "🧠 Оценить знания студента")
async def cmd_grade(message: types.Message, state: FSMContext):
    """
    Обработчик команды /grade и соответствующей кнопки меню
    """
    # Отменяем текущее состояние
    await state.clear()
    
    # Запрашиваем имя студента
    await message.answer(
        "Введите имя студента, которого хотите оценить:",
        reply_markup=get_cancel_keyboard()
    )
    
    # Устанавливаем состояние ожидания имени
    await state.set_state(GradeStudent.waiting_for_name)

@router.message(GradeStudent.waiting_for_name)
async def process_student_name(message: types.Message, state: FSMContext):
    """
    Обработка ввода имени студента
    """
    # Получаем имя студента
    student_name = message.text.strip()
    
    # Проверяем, что имя не пустое
    if not student_name:
        await message.answer("Имя не может быть пустым. Пожалуйста, введите имя студента:")
        return
    
    # Сохраняем имя в состоянии
    await state.update_data(student_name=student_name)
    
    # Переходим к запросу параметра качества
    await message.answer(
        f"Оценка для студента: {student_name}\n\n"
        f"Оцените качество выполнения работы (от 0 до 10):",
        reply_markup=get_rating_keyboard("quality")
    )
    
    # Устанавливаем состояние ожидания качества
    await state.set_state(GradeStudent.waiting_for_quality) 