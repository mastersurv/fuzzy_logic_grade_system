# Инициализация модуля callbacks
from bot.callbacks.menu import router as menu_router
from bot.callbacks.grade_input import router as grade_input_router
from bot.callbacks.history import router as history_router

__all__ = ["menu_router", "grade_input_router", "history_router"] 