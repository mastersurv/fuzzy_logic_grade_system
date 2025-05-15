from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_cancel_keyboard() -> InlineKeyboardMarkup:
    """
    Создает клавиатуру с кнопкой отмены
    
    :return: InlineKeyboardMarkup с кнопкой отмены
    """
    builder = InlineKeyboardBuilder()
    builder.button(text="❌ Отмена", callback_data="cancel_input")
    return builder.as_markup()

def get_rating_keyboard(param_name: str) -> InlineKeyboardMarkup:
    """
    Создает клавиатуру для выбора оценки параметра
    
    :param param_name: Имя параметра (quality, accuracy, deadline)
    :return: InlineKeyboardMarkup с кнопками от 0 до 10
    """
    builder = InlineKeyboardBuilder()
    
    # Добавляем кнопки с оценками от 0 до 10
    for i in range(11):
        builder.button(text=str(i), callback_data=f"{param_name}:{i}")
    
    # Добавляем кнопку отмены
    builder.button(text="❌ Отмена", callback_data="cancel_input")
    
    # Настраиваем сетку: 6, 5 и 1 кнопка в строке
    builder.adjust(6, 5, 1)
    
    return builder.as_markup() 