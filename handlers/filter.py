from aiogram import types, Dispatcher
from aiogram.dispatcher import FSMContext

"""Отмена действий"""

async def reset_clear(call: types.CallbackQuery, state: FSMContext):
    await state.finish()

    return await call.message.answer("<b>☑️Действие отменено!</b>")


def register_handlers_filter(dp: Dispatcher):
    dp.register_callback_query_handler(reset_clear, text="clearreset", state="*")
