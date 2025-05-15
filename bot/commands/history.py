from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.handlers.states import ViewHistory
from bot.keyboards.history import get_history_keyboard
from bot.database.database import get_student_grades, get_or_create_student

router = Router()

@router.message(Command("history"))
@router.message(F.text == "📜 Показать историю оценок")
async def cmd_history(message: types.Message, state: FSMContext):
    """
    Обработчик команды /history и соответствующей кнопки меню
    """
    # Отменяем текущее состояние
    await state.clear()
    
    # Получаем студента
    student = await get_or_create_student(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    # Получаем историю оценок
    grades = await get_student_grades(student.id)
    
    if not grades:
        await message.answer(
            "У вас пока нет истории оценок. Используйте команду /grade, чтобы оценить знания студента."
        )
        return
    
    # Формируем текст с историей оценок
    history_text = "📜 <b>История оценок</b>\n\n"
    
    for i, grade in enumerate(grades, 1):
        history_text += (
            f"<b>{i}. Дата:</b> {grade.created_at.strftime('%Y-%m-%d %H:%M:%S')}\n"
            f"• Качество: {grade.quality}/10\n"
            f"• Точность: {grade.accuracy}/10\n"
            f"• Сроки: {grade.deadline}/10\n"
            f"• Итоговая оценка: {grade.numeric_grade:.2f}/10 ({grade.text_grade})\n\n"
        )
    
    # Отправляем сообщение с историей и клавиатурой
    await message.answer(
        history_text,
        parse_mode="HTML",
        reply_markup=get_history_keyboard()
    )
    
    # Устанавливаем состояние просмотра истории
    await state.set_state(ViewHistory.viewing) 