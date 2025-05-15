from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext
from aiogram.filters import StateFilter

from bot.handlers.states import GradeStudent
from bot.keyboards.grade_input import get_rating_keyboard
from bot.fuzzy_logic_adapter import evaluate_student, get_result_visualization

router = Router()

@router.callback_query(F.data.startswith("quality:"))
async def process_quality_rating(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора оценки качества выполнения работы"""
    await callback.answer()
    quality = int(callback.data.split(":")[1])
    
    # Сохраняем значение в состоянии
    await state.update_data(quality=quality)
    
    # Переходим к следующему шагу - ввод точности
    await callback.message.edit_text(
        f"✅ Качество выполнения: {quality}/10\n\n"
        f"Теперь оцените точность полученного результата (от 0 до 10):",
        reply_markup=get_rating_keyboard("accuracy")
    )
    await state.set_state(GradeStudent.waiting_for_accuracy)

@router.callback_query(StateFilter(GradeStudent.waiting_for_accuracy), F.data.startswith("accuracy:"))
async def process_accuracy_rating(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора оценки точности результата"""
    await callback.answer()
    accuracy = int(callback.data.split(":")[1])
    
    # Сохраняем значение в состоянии
    await state.update_data(accuracy=accuracy)
    
    # Получаем предыдущее значение качества
    data = await state.get_data()
    quality = data.get("quality")
    
    # Переходим к следующему шагу - ввод сроков
    await callback.message.edit_text(
        f"✅ Качество выполнения: {quality}/10\n"
        f"✅ Точность результата: {accuracy}/10\n\n"
        f"Теперь оцените соблюдение сроков (от 0 до 10):",
        reply_markup=get_rating_keyboard("deadline")
    )
    await state.set_state(GradeStudent.waiting_for_deadline)

@router.callback_query(StateFilter(GradeStudent.waiting_for_deadline), F.data.startswith("deadline:"))
async def process_deadline_rating(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора оценки соблюдения сроков"""
    await callback.answer()
    deadline = int(callback.data.split(":")[1])
    
    # Сохраняем значение в состоянии
    await state.update_data(deadline=deadline)
    
    # Получаем все значения
    data = await state.get_data()
    quality = data.get("quality")
    accuracy = data.get("accuracy")
    student_name = data.get("student_name", "Unnamed")
    
    # Получаем telegram_id пользователя
    telegram_id = callback.from_user.id
    
    # Выполняем оценку
    numeric_grade, text_grade = await evaluate_student(
        quality, 
        accuracy, 
        deadline, 
        student_name,
        telegram_id
    )
    
    # Форматируем результат
    result_text = (
        f"🎓 <b>Результат оценки для студента '{student_name}'</b>\n\n"
        f"📊 <b>Входные параметры:</b>\n"
        f"• Качество выполнения: {quality}/10\n"
        f"• Точность результата: {accuracy}/10\n"
        f"• Соблюдение сроков: {deadline}/10\n\n"
        f"📈 <b>Итоговая оценка:</b> {numeric_grade:.2f}/10\n"
        f"📝 <b>Категория:</b> {text_grade.upper()}"
    )
    
    # Отправляем результат
    await callback.message.edit_text(
        result_text,
        parse_mode="HTML"
    )
    
    try:
        # Получаем визуализацию результата
        visualization_buffer = await get_result_visualization(quality, accuracy, deadline)
        
        # Преобразуем BytesIO в BufferedInputFile
        visualization_file = BufferedInputFile(
            visualization_buffer.getvalue(),
            filename="result_visualization.png"
        )
        
        # Отправляем изображение с визуализацией
        await callback.message.answer_photo(
            visualization_file,
            caption="📊 Визуализация процесса оценки с использованием нечеткой логики"
        )
    except Exception as e:
        await callback.message.answer(f"Произошла ошибка при создании визуализации: {str(e)}")
    
    # Завершаем процесс оценки
    await state.clear()

@router.callback_query(F.data == "cancel_input")
async def cancel_input(callback: CallbackQuery, state: FSMContext):
    """Отмена ввода параметров"""
    await callback.answer("Ввод отменен")
    await callback.message.edit_text("❌ Процесс оценки отменен.")
    await state.clear() 