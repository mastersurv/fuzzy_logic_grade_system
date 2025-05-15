import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from bot.config import BOT_TOKEN, LOG_LEVEL
from bot.database.database import init_models
from bot.utils.commands import setup_bot_commands

# Для Windows установим правильную политику событийного цикла
if sys.platform.startswith('win'):
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

# Импорт роутеров
from bot.commands.start import router as start_router
from bot.commands.grade import router as grade_router
from bot.commands.visualize import router as visualize_router
from bot.commands.history import router as history_router
from bot.commands.tests import router as tests_router
from bot.commands.stat import router as stat_router
from bot.callbacks import grade_input_router, history_router as history_cb_router, menu_router

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Создание диспетчера
dp = Dispatcher(storage=MemoryStorage())

# Регистрация роутеров
dp.include_router(start_router)
dp.include_router(grade_router)
dp.include_router(visualize_router)
dp.include_router(history_router)
dp.include_router(tests_router)
dp.include_router(stat_router)
dp.include_router(grade_input_router)
dp.include_router(history_cb_router)
dp.include_router(menu_router)

async def main():
    """Основная функция запуска бота"""
    logger.info("Инициализация базы данных...")
    await init_models()
    
    logger.info("Запуск бота...")
    bot = Bot(token=BOT_TOKEN)
    
    # Устанавливаем команды для бота (появятся в меню)
    await setup_bot_commands(bot)
    
    # Запускаем бота
    try:
        logger.info("Бот запущен")
        await dp.start_polling(bot)
    finally:
        logger.info("Бот остановлен")
        await bot.session.close()

if __name__ == "__main__":
    # Запуск бота
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Бот остановлен")
    except Exception as e:
        logger.exception(f"Ошибка при запуске бота: {e}") 