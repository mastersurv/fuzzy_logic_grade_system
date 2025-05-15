from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_history_keyboard() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для управления историей оценок
    
    :return: InlineKeyboardMarkup с кнопками для просмотра истории
    """
    builder = InlineKeyboardBuilder()
    
    # Добавляем кнопки
    builder.button(text="📄 Экспорт в CSV", callback_data="export_csv")
    builder.button(text="📄 Экспорт в JSON", callback_data="export_json")
    builder.button(text="🔄 Обновить", callback_data="refresh_history")
    builder.button(text="⬅️ Назад", callback_data="back_to_main")
    
    # Настраиваем сетку: по 2 кнопки в строке
    builder.adjust(2)
    
    return builder.as_markup() 