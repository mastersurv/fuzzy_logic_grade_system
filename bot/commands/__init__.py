# Инициализация модуля commands
from bot.commands.start import router as start_router
from bot.commands.grade import router as grade_router
from bot.commands.visualize import router as visualize_router
from bot.commands.history import router as history_router
from bot.commands.tests import router as tests_router
from bot.commands.stat import router as stat_router

__all__ = ["start_router", "grade_router", "visualize_router", "history_router", "tests_router", "stat_router"] 