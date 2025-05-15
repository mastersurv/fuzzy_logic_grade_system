from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_main_menu() -> InlineKeyboardMarkup:
    """
    Создает inline-клавиатуру главного меню
    
    :return: InlineKeyboardMarkup с кнопками главного меню
    """
    builder = InlineKeyboardBuilder()
    
    # Добавляем кнопки
    builder.add(
        InlineKeyboardButton(text="🧠 Оценить знания студента", callback_data="menu:grade"),
        InlineKeyboardButton(text="📊 Визуализировать функции", callback_data="menu:visualize"),
        InlineKeyboardButton(text="📜 История оценок", callback_data="menu:history"),
        InlineKeyboardButton(text="🧪 Запустить тесты", callback_data="menu:tests"),
        InlineKeyboardButton(text="ℹ️ Помощь", callback_data="menu:help")
    )
    
    # Устанавливаем 2 кнопки в строке
    builder.adjust(2)
    
    return builder.as_markup() 