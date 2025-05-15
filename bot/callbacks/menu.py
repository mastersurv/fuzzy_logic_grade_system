from aiogram import Router, F
from aiogram.types import CallbackQuery, BufferedInputFile
from aiogram.fsm.context import FSMContext

from bot.handlers.states import GradeStudent
from bot.keyboards.grade_input import get_cancel_keyboard
from bot.keyboards.main_menu import get_main_menu
from bot.keyboards.history import get_history_keyboard
from bot.database.database import get_student_grades, get_or_create_student
from bot.handlers.states import ViewHistory
from bot.fuzzy_logic_adapter import get_visualization, evaluate_student

router = Router()

@router.callback_query(F.data.startswith("menu:"))
async def handle_menu_callback(callback: CallbackQuery, state: FSMContext):
    """Обработчик кнопок inline-меню"""
    action = callback.data.split(":")[1]
    
    # Отображаем индикатор загрузки
    await callback.answer()
    
    if action == "grade":
        # Отменяем текущее состояние
        await state.clear()
        
        # Запрашиваем имя студента
        await callback.message.answer(
            "Введите имя студента, которого хотите оценить:",
            reply_markup=get_cancel_keyboard()
        )
        
        # Устанавливаем состояние ожидания имени
        await state.set_state(GradeStudent.waiting_for_name)
        
    elif action == "visualize":
        # Отменяем текущее состояние
        await state.clear()
        
        # Отправляем сообщение о подготовке визуализации
        await callback.message.answer("Подготовка визуализации функций принадлежности...")
        
        try:
            # Получаем визуализацию
            visualization_buffer = await get_visualization()
            
            # Преобразуем BytesIO в BufferedInputFile
            visualization_file = BufferedInputFile(
                visualization_buffer.getvalue(),
                filename="visualization.png"
            )
            
            # Отправляем изображение
            await callback.message.answer_photo(
                visualization_file,
                caption="📊 Визуализация функций принадлежности для оценки знаний студентов"
            )
        except Exception as e:
            await callback.message.answer(f"Произошла ошибка при создании визуализации: {str(e)}")
        
    elif action == "history":
        # Отменяем текущее состояние
        await state.clear()
        
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
            await callback.message.answer(
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
        await callback.message.answer(
            history_text,
            parse_mode="HTML",
            reply_markup=get_history_keyboard()
        )
        
        # Устанавливаем состояние просмотра истории
        await state.set_state(ViewHistory.viewing)
        
    elif action == "tests":
        # Отменяем текущее состояние
        await state.clear()
        
        await callback.message.answer("🧪 Запуск тестирования системы...")
        
        # Тестовые данные
        test_data = [
            {"name": "Тест 1", "quality": 9, "accuracy": 9, "deadline": 10, "expected": "отличник"},
            {"name": "Тест 2", "quality": 6, "accuracy": 6, "deadline": 6, "expected": "хорошист"},
            {"name": "Тест 3", "quality": 3, "accuracy": 3, "deadline": 2, "expected": "троечник"},
            {"name": "Тест 4", "quality": 5, "accuracy": 4, "deadline": 8, "expected": "хорошист"},
            {"name": "Тест 5", "quality": 1, "accuracy": 2, "deadline": 1, "expected": "троечник"}
        ]
        
        # Выполняем тесты
        results_text = "🧪 <b>Результаты тестирования</b>\n\n"
        
        for test in test_data:
            # Оцениваем знания
            numeric_grade, text_grade = await evaluate_student(
                test["quality"], 
                test["accuracy"], 
                test["deadline"],
                f"Test Student {test['name']}"
            )
            
            # Определяем успешность теста
            test_result = "✅ ПРОЙДЕН" if text_grade.lower() == test["expected"].lower() else "❌ НЕ ПРОЙДЕН"
            
            # Добавляем результат в общий текст
            results_text += (
                f"<b>{test['name']}:</b>\n"
                f"• Параметры: качество={test['quality']}, "
                f"точность={test['accuracy']}, "
                f"сроки={test['deadline']}\n"
                f"• Ожидаемый результат: {test['expected']}\n"
                f"• Полученный результат: {text_grade} ({numeric_grade:.2f})\n"
                f"• Статус теста: {test_result}\n\n"
            )
        
        # Отправляем результаты тестов
        await callback.message.answer(results_text, parse_mode="HTML")
        
    elif action == "help":
        # Отправляем справку
        help_text = (
            "ℹ️ <b>Справка по использованию бота</b>\n\n"
            "<b>Доступные команды:</b>\n"
            "/start - Начать работу с ботом\n"
            "/grade - Оценить знания студента\n"
            "/visualize - Визуализировать функции принадлежности\n"
            "/history - Показать историю оценок\n"
            "/tests - Запустить тесты\n"
            "/help - Показать эту справку\n\n"
            "<b>Как оценить знания студента:</b>\n"
            "1. Выберите '🧠 Оценить знания студента' в меню или введите /grade\n"
            "2. Введите имя студента\n"
            "3. Оцените качество выполнения работы (0-10)\n"
            "4. Оцените точность полученного результата (0-10)\n"
            "5. Оцените соблюдение сроков (0-10)\n"
            "6. Получите результат оценки\n\n"
            "<b>Нечеткая логика:</b>\n"
            "Система использует алгоритм нечеткого вывода Мамдани для классификации студентов на основе входных параметров."
        )
        
        await callback.message.answer(help_text, parse_mode="HTML") 