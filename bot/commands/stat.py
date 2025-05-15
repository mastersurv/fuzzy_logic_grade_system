from aiogram import Router, types
from aiogram.filters import Command
from sqlalchemy import select, func

from bot.database.database import async_session
from bot.database.models import Student, GradeResult
from bot.config import ADMIN_IDS

router = Router()

@router.message(Command("stat"))
async def cmd_stat(message: types.Message):
    """
    Обработчик команды /stat - показывает статистику использования бота
    Доступно только администраторам
    """
    # Проверяем, является ли пользователь администратором
    if message.from_user.id not in ADMIN_IDS:
        await message.answer("⛔ У вас нет доступа к этой команде.")
        return
    
    # Собираем статистику
    async with async_session() as session:
        # Общее количество пользователей
        total_users_query = select(func.count()).select_from(Student)
        total_users = await session.scalar(total_users_query)
        
        # Общее количество оценок
        total_grades_query = select(func.count()).select_from(GradeResult)
        total_grades = await session.scalar(total_grades_query)
        
        # Средние оценки по категориям
        avg_quality_query = select(func.avg(GradeResult.quality)).select_from(GradeResult)
        avg_quality = await session.scalar(avg_quality_query) or 0
        
        avg_accuracy_query = select(func.avg(GradeResult.accuracy)).select_from(GradeResult)
        avg_accuracy = await session.scalar(avg_accuracy_query) or 0
        
        avg_deadline_query = select(func.avg(GradeResult.deadline)).select_from(GradeResult)
        avg_deadline = await session.scalar(avg_deadline_query) or 0
        
        # Распределение по категориям
        category_stats_query = select(
            GradeResult.text_grade,
            func.count().label('count')
        ).group_by(GradeResult.text_grade)
        
        category_stats_result = await session.execute(category_stats_query)
        category_stats = {row[0]: row[1] for row in category_stats_result}
        
        # Формируем статистику по категориям
        poor_count = category_stats.get('Троечник', 0)
        good_count = category_stats.get('Хорошист', 0)
        excellent_count = category_stats.get('Отличник', 0)
    
    # Проверка деления на ноль
    percent_poor = 0
    percent_good = 0
    percent_excellent = 0
    
    if total_grades > 0:
        percent_poor = 100 * poor_count / total_grades
        percent_good = 100 * good_count / total_grades
        percent_excellent = 100 * excellent_count / total_grades
    
    # Формируем сообщение
    stat_text = (
        "📊 <b>Статистика использования бота</b>\n\n"
        f"👥 <b>Количество пользователей:</b> {total_users}\n"
        f"📝 <b>Количество оценок:</b> {total_grades}\n\n"
        f"📈 <b>Средние показатели:</b>\n"
        f"• Качество: {avg_quality:.2f}/10\n"
        f"• Точность: {avg_accuracy:.2f}/10\n"
        f"• Сроки: {avg_deadline:.2f}/10\n\n"
        f"🏆 <b>Распределение по категориям:</b>\n"
        f"• 🟠 Троечники: {poor_count} ({percent_poor:.1f}% от всех оценок)\n"
        f"• 🟡 Хорошисты: {good_count} ({percent_good:.1f}% от всех оценок)\n"
        f"• 🟢 Отличники: {excellent_count} ({percent_excellent:.1f}% от всех оценок)"
    )
    
    await message.answer(stat_text, parse_mode="HTML") 