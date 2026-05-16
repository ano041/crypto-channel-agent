from aiogram import Router, types, F
from config import settings
from services.scheduler import schedule_post
from tools.validator import validate_callback_data
from utils.logger import logger

router = Router()


@router.callback_query(F.data.startswith('approve:'))
async def cb_approve(callback: types.CallbackQuery):
    """Обработка кнопки одобрения поста."""
    if callback.from_user.id not in settings.ADMIN_IDS:
        return await callback.answer('❌ Нет доступа', show_alert=True)
    
    # Валидация callback_data
    is_valid, action, post_key = validate_callback_data(callback.data)
    if not is_valid:
        logger.warning("Invalid callback data", user_id=callback.from_user.id, data=callback.data)
        return await callback.answer('❌ Неверный формат данных', show_alert=True)
    
    try:
        # Планируем публикацию (5 минут задержки по умолчанию)
        schedule_post(post_key, delay_minutes=5)
        
        await callback.answer('✅ Пост запланирован!', show_alert=True)
        await callback.message.edit_text(
            callback.message.text + '\n\n✅ Запланировано к публикации',
            parse_mode='MarkdownV2'
        )
        logger.info("Post scheduled", post_key=post_key, admin_id=callback.from_user.id)
    except Exception as e:
        logger.error("Schedule failed", post_key=post_key, error=str(e))
        await callback.answer('❌ Ошибка планирования', show_alert=True)


@router.callback_query(F.data.startswith('edit:'))
async def cb_edit(callback: types.CallbackQuery):
    """Обработка кнопки редактирования поста."""
    # Валидация callback_data
    is_valid, action, post_key = validate_callback_data(callback.data)
    if not is_valid:
        return await callback.answer('❌ Неверный формат данных', show_alert=True)
    
    await callback.answer('✏️ Редактирование в разработке', show_alert=True)
    logger.info("Edit requested", post_key=post_key, user_id=callback.from_user.id)


@router.callback_query(F.data.startswith('reject:'))
async def cb_reject(callback: types.CallbackQuery):
    """Обработка кнопки отклонения поста."""
    if callback.from_user.id not in settings.ADMIN_IDS:
        return await callback.answer('❌ Нет доступа', show_alert=True)
    
    # Валидация callback_data
    is_valid, action, post_key = validate_callback_data(callback.data)
    if not is_valid:
        return await callback.answer('❌ Неверный формат данных', show_alert=True)
    
    try:
        await callback.answer('❌ Отклонено', show_alert=True)
        await callback.message.delete()
        logger.info("Post rejected", post_key=post_key, admin_id=callback.from_user.id)
    except Exception as e:
        logger.error("Reject failed", post_key=post_key, error=str(e))