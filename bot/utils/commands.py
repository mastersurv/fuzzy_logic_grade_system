from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault, BotCommandScopeChat

from bot.config import ADMIN_IDS

# Список команд для обычных пользователей
USER_COMMANDS = [
    BotCommand(command="start", description="Начать работу с ботом"),
    BotCommand(command="grade", description="Оценить знания студента"),
    BotCommand(command="visualize", description="Визуализировать функции принадлежности"),
    BotCommand(command="history", description="Показать историю оценок"),
    BotCommand(command="help", description="Показать справку")
]

# Список команд для администраторов
ADMIN_COMMANDS = [
    BotCommand(command="start", description="Начать работу с ботом"),
    BotCommand(command="grade", description="Оценить знания студента"),
    BotCommand(command="visualize", description="Визуализировать функции принадлежности"),
    BotCommand(command="history", description="Показать историю оценок"),
    BotCommand(command="tests", description="Запустить тесты"),
    BotCommand(command="help", description="Показать справку"),
    BotCommand(command="stat", description="Статистика использования бота")
]

async def setup_bot_commands(bot: Bot):
    """
    Настраивает команды бота для разных категорий пользователей
    
    :param bot: Экземпляр бота
    """
    # Устанавливаем команды для обычных пользователей
    await bot.set_my_commands(USER_COMMANDS, scope=BotCommandScopeDefault())
    
    # Устанавливаем команды для администраторов
    for admin_id in ADMIN_IDS:
        await bot.set_my_commands(ADMIN_COMMANDS, scope=BotCommandScopeChat(chat_id=admin_id)) 