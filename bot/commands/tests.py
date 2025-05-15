from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.fuzzy_logic_adapter import evaluate_student

router = Router()

@router.message(Command("tests"))
@router.message(F.text == "🧪 Запустить тесты")
async def cmd_tests(message: types.Message, state: FSMContext):
    """
    Обработчик команды /tests и соответствующей кнопки меню
    """
    # Отменяем текущее состояние
    await state.clear()
    
    await message.answer("🧪 Запуск тестирования системы...")
    
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
        test_result = "✅ ПРОЙДЕН" if text_grade == test["expected"] else "❌ НЕ ПРОЙДЕН"
        
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
    await message.answer(results_text, parse_mode="HTML") 