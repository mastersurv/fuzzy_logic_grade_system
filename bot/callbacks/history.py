import io
import json
import csv
from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext

from bot.database.database import get_student_grades, get_or_create_student

router = Router()

@router.callback_query(F.data == "export_csv")
async def export_csv(callback: CallbackQuery, state: FSMContext):
    """Экспорт истории в CSV файл"""
    await callback.answer()
    
    # Получаем студента
    student = await get_or_create_student(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        first_name=callback.from_user.first_name,
        last_name=callback.from_user.last_name
    )
    
    # Получаем историю оценок
    grades = await get_student_grades(student.id)
    
    if not grades:
        await callback.message.answer("У вас пока нет истории оценок для экспорта.")
        return
    
    # Создаем буфер для CSV
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    
    # Записываем заголовки
    writer.writerow([
        "Дата", "Качество", "Точность", "Сроки", 
        "Числовая оценка", "Текстовая оценка"
    ])
    
    # Записываем данные
    for grade in grades:
        writer.writerow([
            grade.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            grade.quality,
            grade.accuracy,
            grade.deadline,
            grade.numeric_grade,
            grade.text_grade
        ])
    
    # Создаем файл
    csv_bytes = buffer.getvalue().encode('utf-8')
    file = BufferedInputFile(csv_bytes, filename="grades_history.csv")
    
    # Отправляем файл
    await callback.message.answer_document(
        file,
        caption="📊 История оценок в формате CSV"
    )

@router.callback_query(F.data == "export_json")
async def export_json(callback: CallbackQuery, state: FSMContext):
    """Экспорт истории в JSON файл"""
    await callback.answer()
    
    # Получаем студента
    student = await get_or_create_student(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        first_name=callback.from_user.first_name,
        last_name=callback.from_user.last_name
    )
    
    # Получаем историю оценок
    grades = await get_student_grades(student.id)
    
    if not grades:
        await callback.message.answer("У вас пока нет истории оценок для экспорта.")
        return
    
    # Создаем список данных
    data = []
    for grade in grades:
        data.append({
            "дата": grade.created_at.strftime('%Y-%m-%d %H:%M:%S'),
            "параметры": {
                "качество": grade.quality,
                "точность": grade.accuracy,
                "сроки": grade.deadline
            },
            "оценка": {
                "числовая": grade.numeric_grade,
                "текстовая": grade.text_grade
            }
        })
    
    # Сериализуем в JSON
    json_str = json.dumps(data, ensure_ascii=False, indent=4)
    
    # Создаем файл
    file = BufferedInputFile(json_str.encode('utf-8'), filename="grades_history.json")
    
    # Отправляем файл
    await callback.message.answer_document(
        file,
        caption="📊 История оценок в формате JSON"
    )

@router.callback_query(F.data == "refresh_history")
async def refresh_history(callback: CallbackQuery, state: FSMContext):
    """Обновление истории оценок"""
    await callback.answer("Обновление истории...")
    
    # Получаем студента
    student = await get_or_create_student(
        telegram_id=callback.from_user.id,
        username=callback.from_user.username,
        first_name=callback.from_user.first_name,
        last_name=callback.from_user.last_name
    )
    
    # Получаем обновленную историю оценок
    grades = await get_student_grades(student.id)
    
    if not grades:
        await callback.message.edit_text(
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
    
    # Обновляем сообщение
    from bot.keyboards.history import get_history_keyboard
    await callback.message.edit_text(
        history_text,
        parse_mode="HTML",
        reply_markup=get_history_keyboard()
    )

@router.callback_query(F.data == "back_to_main")
async def back_to_main(callback: CallbackQuery, state: FSMContext):
    """Возврат в главное меню"""
    await callback.answer()
    
    # Очищаем состояние
    await state.clear()
    
    # Возвращаемся в главное меню
    from bot.keyboards.main_menu import get_main_menu
    await callback.message.answer(
        "Выберите действие из меню:",
        reply_markup=get_main_menu()
    )
    
    # Удаляем предыдущее сообщение
    await callback.message.delete() 