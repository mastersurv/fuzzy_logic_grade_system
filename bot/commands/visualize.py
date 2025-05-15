from aiogram import Router, types, F
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import BufferedInputFile

from bot.fuzzy_logic_adapter import get_visualization

router = Router()

@router.message(Command("visualize"))
@router.message(F.text == "📊 Визуализировать функции принадлежности")
async def cmd_visualize(message: types.Message, state: FSMContext):
    """
    Обработчик команды /visualize и соответствующей кнопки меню
    """
    # Отменяем текущее состояние
    await state.clear()
    
    # Отправляем сообщение о подготовке визуализации
    await message.answer("Подготовка визуализации функций принадлежности...")
    
    try:
        # Получаем визуализацию
        visualization_buffer = await get_visualization()
        
        # Преобразуем BytesIO в BufferedInputFile
        visualization_file = BufferedInputFile(
            visualization_buffer.getvalue(),
            filename="visualization.png"
        )
        
        # Отправляем изображение
        await message.answer_photo(
            visualization_file,
            caption="📊 Визуализация функций принадлежности для оценки знаний студентов"
        )
    except Exception as e:
        await message.answer(f"Произошла ошибка при создании визуализации: {str(e)}") 