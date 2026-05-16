from aiogram import Router, types, F
from config import settings
from services.scheduler import schedule_post
from utils.logger import logger

router = Router()

@router.callback_query(F.data.startswith('approve:'))
async def cb_approve(callback: types.CallbackQuery):
    if callback.from_user.id not in settings.ADMIN_IDS:
        return await callback.answer('❌ Нет доступа', show_alert=True)
    
    await callback.answer('✅ Пост запланирован!', show_alert=True)
    await callback.message.edit_text(callback.message.text + '\n\n✅ Запланировано к публикации')

@router.callback_query(F.data.startswith('edit:'))
async def cb_edit(callback: types.CallbackQuery):
    await callback.answer('✏️ Редактирование в разработке')

@router.callback_query(F.data.startswith('reject:'))
async def cb_reject(callback: types.CallbackQuery):
    await callback.answer('❌ Отклонено', show_alert=True)
    await callback.message.delete()