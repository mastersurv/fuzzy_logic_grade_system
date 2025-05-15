from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from bot.keyboards.main_menu import get_main_menu
from bot.database.database import get_or_create_student

router = Router()

@router.message(Command("start"))
async def cmd_start(message: types.Message, state: FSMContext):
    """
    Обработчик команды /start - начало работы с ботом
    """
    # Отменяем текущее состояние
    await state.clear()
    
    # Получаем или создаем запись о студенте
    await get_or_create_student(
        telegram_id=message.from_user.id,
        username=message.from_user.username,
        first_name=message.from_user.first_name,
        last_name=message.from_user.last_name
    )
    
    # Приветственное сообщение
    greeting_text = (
        f"👋 Здравствуйте, {message.from_user.first_name}!\n\n"
        "Добро пожаловать в систему оценки уровня знаний студентов на основе нечеткой логики.\n\n"
        "Здесь вы можете оценить знания студентов по следующим параметрам:\n"
        "• Качество выполнения работы (0-10)\n"
        "• Точность полученного результата (0-10)\n"
        "• Соблюдение сроков (0-10)\n\n"
        "По результатам оценки система классифицирует студента как 'троечника', 'хорошиста' или 'отличника'.\n\n"
        "Выберите действие из меню ниже:"
    )
    
    # Отправляем сообщение с inline-клавиатурой
    await message.answer(greeting_text, reply_markup=get_main_menu())

@router.message(Command("help"))
async def cmd_help(message: types.Message):
    """
    Обработчик команды /help - показывает справку
    """
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
    
    await message.answer(help_text, parse_mode="HTML") 